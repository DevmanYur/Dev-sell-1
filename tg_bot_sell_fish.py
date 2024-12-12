import os
import logging
from functools import partial
from pprint import pprint

import redis
import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler

from _0_functions import get_callback_data, get_menu_parts_keyboard
from _10_order_Or import get_order_name
from _1_start import bot_start
from _3_all_menu_AM import get_all_menu
from _4_part_menu_MP import get_menu_part
from _5_cart_C_Ci import get_cart
from _6_product_P_S import get_product
from _7_new_product_New import get_new_product

logger = logging.getLogger(__name__)


_database = None


def get_database_connection(database_settings):
    global _database
    database_host, database_port, database_password = database_settings
    if _database is None:
        _database = redis.Redis(host=database_host, port=database_port, password=database_password)
    return _database


def handle_users_reply(update, context, strapi_settings=None, database_settings =None):
    simvol = '🍗 🍲 🍴 🥗 🥞 🫖'
    db = get_database_connection(database_settings)
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id).decode("utf-8")
    states_functions = {
        'START': partial(bot_start, strapi_settings = strapi_settings),
        'Выбор после start': partial(choice_from_start, strapi_settings = strapi_settings),
        'Выбор после всего меню': partial(choice_from_all_menu, strapi_settings=strapi_settings),
        'Выбор после Меню раздел': partial(choice_from_menu_part, strapi_settings=strapi_settings),
        'Выбор после Корзины': partial(choice_from_cart, strapi_settings = strapi_settings),
        'Выбор после Продукта' : partial(choice_from_product, strapi_settings = strapi_settings),
        'Выбор после всего Новинки' : partial(choice_from_new_product, strapi_settings = strapi_settings),
        "Выбор после Имя": partial(choice_from_order_name, strapi_settings = strapi_settings),
        "Выбор после коммент" : partial(choice_from_comment, strapi_settings = strapi_settings),
    }
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



def choice_from_start(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')

    if  action =='New':
        return get_new_product(update, context, strapi_settings=strapi_settings)

    if  action =='MP':
        return get_menu_part(update, context, strapi_settings=strapi_settings)

    if  action =='AB':
        print('AB')
        # return get_all_menu(update, context, strapi_settings=strapi_settings)

    if action =='C':
        return get_cart(update, context, strapi_settings=strapi_settings)


def choice_from_all_menu(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action == 'New':
        return get_new_product(update, context, strapi_settings=strapi_settings)

    if  action =='MP':
        return get_menu_part(update, context, strapi_settings=strapi_settings)

    if action == 'AB':
        print('AB')
        # return get_all_menu(update, context, strapi_settings=strapi_settings)

    if action == 'AM':
        return get_all_menu(update, context, strapi_settings=strapi_settings)

    if action == 'C':
        return get_cart(update, context, strapi_settings=strapi_settings)



def choice_from_menu_part(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action == 'P':
        return get_product(update, context, strapi_settings=strapi_settings)

    if  action =='MP':
        return get_menu_part(update, context, strapi_settings=strapi_settings)

    if action == 'AM':
        return get_all_menu(update, context, strapi_settings=strapi_settings)

    if action == 'C':
        return get_cart(update, context, strapi_settings=strapi_settings)





def choice_from_product(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action == 'S':
        return get_product(update, context, strapi_settings=strapi_settings)

    if action == 'AM':
        return get_all_menu(update, context, strapi_settings=strapi_settings)

    if action == 'MP':
        return get_menu_part(update, context, strapi_settings=strapi_settings)

    if action == 'C':
        return get_cart(update, context, strapi_settings=strapi_settings)



def choice_from_cart(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action =='Ci':
        return get_cart(update, context, strapi_settings=strapi_settings)

    if action == 'AM':
        return get_all_menu(update, context, strapi_settings=strapi_settings)

    if action == 'Or':
        return get_order_name(update, context, strapi_settings=strapi_settings)



def choice_from_new_product(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')

    if action == 'New':
        return get_new_product(update, context, strapi_settings=strapi_settings)
    if action == 'P':
        return get_product(update, context, strapi_settings=strapi_settings)
    if action == 'AM':
        return get_all_menu(update, context, strapi_settings=strapi_settings)
    if action == 'C':
        return get_cart(update, context, strapi_settings=strapi_settings)


def choice_from_order_name(update, context, strapi_settings=None):
    text = 'Напишите, пожалуйста, комм'
    update.message.reply_text(text=text)

    # context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id-1)
    return "Выбор после коммент"

def choice_from_comment(update, context, strapi_settings=None):
    text0 = 'Ваш зказа...'
    update.message.reply_text(text=text0)

    text1 = (f'Скопируйте сообщение, которое выше\n'
             f'и отправьте его в чат\n'
             f'\n'
             f'Спасибо!\n'
             f'Ваша Ладушка!💕')
    update.message.reply_text(text=text1)

    text2 = (f'Чтобы оформить новый заказ, нажмите /start ')
    update.message.reply_text(text=text2)

    # context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    # context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id - 1)
    return ""

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()

    strapi_token = os.getenv("STRAPI_TOKEN")
    strapi_host = os.getenv("STRAPI_HOST")
    strapi_port = os.getenv("STRAPI_PORT")
    strapi_headers = {'Authorization': f'Bearer {strapi_token}'}

    try:
        menu_parts_payload = {'sort': 'Sortirovka'}
        menu_parts_url = f'{strapi_host}{strapi_port}/api/menu-parts'
        menu_parts_response = requests.get(menu_parts_url, params=menu_parts_payload, headers=strapi_headers)
        menu_parts_response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    data_menu_parts = menu_parts_response.json()['data']

    strapi_settings = [strapi_host, strapi_port, strapi_headers, data_menu_parts]

    database_host = os.getenv("REDIS_HOST")
    database_port = os.getenv("REDIS_PORT")
    database_password = os.getenv("REDIS_PASSWORD")
    database_settings = [database_host, database_port, database_password]

    get_handle_users_reply = partial(handle_users_reply,
                                     strapi_settings = strapi_settings,
                                     database_settings = database_settings)

    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(get_handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, get_handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', get_handle_users_reply))
    updater.start_polling()
    updater.idle()
