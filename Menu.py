from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


btnSearch = KeyboardButton('🔎')
btnFace = KeyboardButton('❤️')
btnBack = KeyboardButton('🔙')
btnShazam = KeyboardButton('Shazam!')
btnLyrics = KeyboardButton("Search by Lyrics")

btnAddReceipt = KeyboardButton("Add new receipt")
btnAddReceipt_search = KeyboardButton("Search for receipt")
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnAddReceipt, btnAddReceipt_search)
menu2 = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack)

inline_btn_1 = InlineKeyboardButton('Dietary', callback_data='dietary')
inline_btn_2 = InlineKeyboardButton('Vegan', callback_data='vegan')
inline_btn_3 = InlineKeyboardButton('Gluten free ', callback_data='gluten')


inline_search_keybord = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2, inline_btn_3)