from aiogram import Bot, types
from aiohttp.client import request
from config import BOT_TOKEN, PATH
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from receipt import Recipe, Ingredient, Instruction, Search
import Menu as nav
from app.dialogs import msg

class States(StatesGroup):
    BASE = State()
    ADD_TITLE = State()
    ADD_DESCRIPTION = State()
    ADD_INGREDIENTS = State()
    ADD_INSTRUCTIONS = State()
    ADD_IMAGE = State()
    TAGS =State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state='*', commands=['start','info'])
async def command_start(message: types.Message):
    await States.BASE.set()
    await bot.send_message(message.from_user.id , msg.start_new_user.format(message.from_user.first_name), reply_markup=nav.mainMenu)

@dp.message_handler(state=States.BASE)
async def echo_send(message: types.Message):
    if message.text == 'Add new recipe':
        await bot.send_message(message.from_user.id, "Send the title for the future recipe",reply_markup=nav.menu2)
        receipt = await adding()
        print (receipt)
        await States.ADD_TITLE.set()
    if message.text == 'Search for recipe':
        await bot.send_message(message.from_user.id, "Choose tags for the searched dish", reply_markup=nav.inline_search_keybord)
        search_request = await searching()
        print(search_request)
        await States.ADD_TITLE.set()

    
async def adding():
    new_receipt = Recipe()

    @dp.message_handler(state = States.ADD_TITLE)
    async def add_name(message: types.Message):
        if message.text:
            new_receipt.user_id = message.from_user.id
            new_receipt.title = message.text
            await States.ADD_DESCRIPTION.set()
        await bot.send_message(message.from_user.id , "Title added!")
        await bot.send_message(message.from_user.id , "Now send the description for your recipe")


    @dp.message_handler(state = States.ADD_DESCRIPTION)
    async def add_desc(message: types.Message):
        if message.text:            
            new_receipt.description = message.text
        await bot.send_message(message.from_user.id , "Descr added!")
        await bot.send_message(message.from_user.id , "Now send the ingredients needed for your recipe in format: \n Ingredient quantity unit - Ingredient quantity unit - ...")
        await States.ADD_INGREDIENTS.set()

    
    @dp.message_handler(state = States.ADD_INGREDIENTS)
    async def add_ingredients(message: types.Message):
        if message.text:
            ingred_list = list()
            x = 0
            for ingredient in message.text.split(' - '):
                x += 1 
                a = ingredient.split(' ')
                ingred_list.append(Ingredient(new_receipt.id, x, int(a[1]), a[0], a[2]))
            new_receipt.ingredients = ingred_list

        await bot.send_message(message.from_user.id , "Ingred added")
        await bot.send_message(message.from_user.id , "Now send the instructions for your recipe in format:\n FIRST STEP - SECOND STEP - ...")
        await States.ADD_INSTRUCTIONS.set()
        

    @dp.message_handler(state = States.ADD_INSTRUCTIONS)
    async def add_instructions(message: types.Message):
        if message.text:
            x=0
            instr_list = list()
            for instruction in message.text.split('-'):
                x+=1
                instr_list.append(Instruction(new_receipt.id, x, instruction))
            new_receipt.instructions = instr_list
        await bot.send_message(message.from_user.id , "Instructions added")
        await bot.send_message(message.from_user.id , "Now send the photo of the dish your recipe about")
        await States.ADD_IMAGE.set()


    @dp.message_handler(state = States.ADD_IMAGE, content_types=['photo'])
    async def add_image(message: types.Message):
        if message.photo:
            file_path = await bot.download_file_by_id(message.photo[-1].file_id, destination_dir=PATH)
            with open (file_path.name, "rb") as image:
                binary_photo = image.read()
                new_receipt.image = binary_photo
        await bot.send_message(message.from_user.id , "Photo added!", reply_markup=nav.mainMenu)
        await States.BASE.set()

    return new_receipt
    
async def searching():
    await States.TAGS.set()
    tags = list()
    request = str()

    @dp.message_handler()
    async def search_request(message: types.Message):
        if message.text:
            request = message.text
        await States.BASE.set()

    @dp.callback_query_handler(lambda c: c.data == 'dietary', state = States.TAGS)
    async def dietary(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Dietary added to search parameters")
        tags.append("Dietary")

    @dp.callback_query_handler(lambda c: c.data == 'vegan')
    async def vegan(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Vegan added to search parameters")
        tags.append("Vegan")

    @dp.callback_query_handler(lambda c: c.data == 'gluten')
    async def dietary(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Gluten added to search parameters")
        tags.append("Gluten")

    return Search (request, tags)

        

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()