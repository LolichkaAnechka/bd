from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


btnSearch = KeyboardButton('🔎')
btnFace = KeyboardButton('❤️')
btnBack = KeyboardButton('🔙')
btnShazam = KeyboardButton('Shazam!')
btnLyrics = KeyboardButton("Search by Lyrics")

btnAddReceipt = KeyboardButton("Add new recipe")
btnAddReceipt_search = KeyboardButton("Search by tags")
btnAddReceipt_search_by_title = KeyboardButton("Search by title")

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnAddReceipt, btnAddReceipt_search, btnAddReceipt_search_by_title)
menu2 = ReplyKeyboardMarkup(resize_keyboard = True).add(btnBack)

inline_btn_1 = InlineKeyboardButton('Dietary', callback_data='dietary')
inline_btn_2 = InlineKeyboardButton('Vegan', callback_data='vegan')
inline_btn_3 = InlineKeyboardButton('Gluten free ', callback_data='gluten')

inline_btn_finish = InlineKeyboardButton('Post Receipt', callback_data='finish')
inline_finish_keyboard = InlineKeyboardMarkup(row_width=2).add(inline_btn_finish)

inline_search_keybord = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2, inline_btn_3)