from aiogram import Bot, types
from aiogram.types import callback_query
from aiohttp.client import request
from config import BOT_TOKEN, PATH
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from receipt import Recipe, Ingredient, Instruction, Search, Tag
import Menu as nav
from app.dialogs import msg
import database

class States(StatesGroup):
    BASE = State()
    ADD_TITLE = State()
    ADD_DESCRIPTION = State()
    ADD_INGREDIENTS = State()
    ADD_INSTRUCTIONS = State()
    ADD_IMAGE = State()
    ADD_TAGS = State()
    ADD_FINISH = State()
    SEARCH_TITLE = State ()
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
        await States.ADD_TITLE.set()
    if message.text == 'Search by tags':
        await bot.send_message(message.from_user.id, "Send tags for the searched dish")
        await States.TAGS.set()
    if message.text == 'Search by title':
        await bot.send_message(message.from_user.id, 'Send the title to search')
        await States.SEARCH_TITLE.set()

@dp.message_handler(state = States.TAGS)
async def search_tags(message: types.Message):
    if message.text:
        print(message.text, len(message.text))
        result = database.search_tags(message.text)
        print(result)
        for recipe in result:
            await bot.send_message(message.from_user.id, text = database.recipeToString(recipe))
        await States.BASE.set()
    
@dp.message_handler(state = States.SEARCH_TITLE)
async def search_title(message: types.Message):
    if message.text:
        result = database.search_title(message.text)
        for recipe in result:
            await bot.send_message(message.from_user.id, text = database.recipeToString(recipe))
        await States.BASE.set()
        # ids = search_by(message.text)
        # init_dict = dict()
        # result = dict()
        # init_dict['id'] = result['recipe'][0]
        # init_dict['title'] = result['recipe'][1]
        # init_dict['description'] = result['recipe'][2]
        # init_dict ['ingredients'] = list()
        # init_dict['instructions'] = list()
        # for i in result['ingredients']:
        #     init_dict ['ingredients'].append(Ingredient(i[0], i[1], i[2], i[3]))
        # init_dict['instructions'] = result['instructions'][0]
        # init_dict['id'] = result['recipe'][0]

        # Recipe()
        # recipe = Recipe()

@dp.message_handler(state = States.ADD_TITLE)
async def add_name(message: types.Message, state: FSMContext):
    if message.text:
        async with state.proxy() as receipt_data:
            receipt_data['user_id'] = message.from_user.id
            receipt_data['title'] = message.text
        await States.ADD_DESCRIPTION.set()
    await bot.send_message(message.from_user.id , "Title added!")
    await bot.send_message(message.from_user.id , "Now send the description for your recipe")


@dp.message_handler(state = States.ADD_DESCRIPTION)
async def add_desc(message: types.Message, state: FSMContext):
    if message.text: 
        async with state.proxy() as receipt_data:          
            receipt_data['description'] = message.text
    await bot.send_message(message.from_user.id , "Descr added!")
    await bot.send_message(message.from_user.id , "Now send the ingredients needed for your recipe in format: \n Ingredient quantity unit - Ingredient quantity unit - ...")
    await States.ADD_INGREDIENTS.set()


@dp.message_handler(state = States.ADD_INGREDIENTS)
async def add_ingredients(message: types.Message, state: FSMContext):
    if message.text:
        ingred_list = list()
        x = 0
        for ingredient in message.text.split(' - '):
            x += 1 
            a = ingredient.split(' ')
            ingred_list.append(Ingredient(x, int(a[1]), a[0], a[2]))
        async with state.proxy() as receipt_data:          
            receipt_data['ingredients'] = ingred_list

    await bot.send_message(message.from_user.id , "Ingred added")
    await bot.send_message(message.from_user.id , "Now send the instructions for your recipe in format:\n FIRST STEP - SECOND STEP - ...")
    await States.ADD_INSTRUCTIONS.set()
    

@dp.message_handler(state = States.ADD_INSTRUCTIONS)
async def add_instructions(message: types.Message, state: FSMContext):
    if message.text:
        x=0
        instr_list = list()
        for instruction in message.text.split('-'):
            x+=1
            instr_list.append(Instruction(x, instruction))
        async with state.proxy() as receipt_data:          
            receipt_data['instructions'] = instr_list
    await bot.send_message(message.from_user.id , "Instructions added")
    await bot.send_message(message.from_user.id , "Now send the tags of the dish your recipe about")
    await States.ADD_TAGS.set()

@dp.message_handler(state = States.ADD_TAGS)
async def add_tags(message: types.Message, state: FSMContext):
    if message.text:
        tags_list = list()
        for tag in message.text.split('-'):
            tags_list.append(Tag(tag))
        async with state.proxy() as receipt_data:          
            receipt_data['tags'] = tags_list
    await bot.send_message(message.from_user.id , "Instructions added")
    await bot.send_message(message.from_user.id , "Now send the photo of the dish your recipe about")
    await States.ADD_IMAGE.set()


@dp.message_handler(state = States.ADD_IMAGE, content_types=['photo'])
async def no_image(message: types.Message, state: FSMContext):
    if message.photo:
        file_path = await bot.download_file_by_id(message.photo[-1].file_id, destination_dir=PATH)
        with open (file_path.name, "rb") as image:
            binary_photo = image.read()
            async with state.proxy() as receipt_data:          
                receipt_data['image'] = binary_photo
        await bot.send_message(message.from_user.id , "Photo added!", reply_markup=nav.mainMenu)
        await States.ADD_FINISH.set()
        await bot.send_message(message.from_user.id, "Receipt finished", reply_markup=nav.inline_finish_keyboard)



@dp.message_handler(state = States.ADD_IMAGE)
async def add_image(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Image skiped", reply_markup=nav.mainMenu)
    async with state.proxy() as receipt_data:          
        receipt_data['image'] = None
    await bot.send_message(message.from_user.id, "Receipt finished ", reply_markup=nav.inline_finish_keyboard)
    await States.ADD_FINISH.set()




@dp.callback_query_handler(lambda c: c.data == 'finish', state = States.ADD_FINISH)
async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    dict_ = await state.get_data()
    new_receipt = Recipe(dict_, database.get_recipes_count())
    # new_receipt.title = dict_['title']
    # new_receipt.description = dict_['description']
    # new_receipt.ingredients = dict_['ingredients']
    # new_receipt.instructions = dict_['instructions']
    # new_receipt.user_id = dict_['user_id']
    # new_receipt.image = dict_['image']
    await callback_query.message.edit_reply_markup(reply_markup={})
    connection = database.connect()
    print(new_receipt.id)
    database.db_api.RecipeRepository.insert(connection, new_receipt)
    for ingredient in new_receipt.ingredients:
        database.db_api.IngredientRepository.insert(connection, ingredient, new_receipt.id)

    for instruction in new_receipt.instructions:
        database.db_api.InstructionRepository.insert(connection, instruction, new_receipt.id)

    for tag in new_receipt.tags:
        database.db_api.TagsRepository.insert(connection, tag, new_receipt.id)
    await States.BASE.set()


        

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()