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
from _10_order_Or import get_dostavka
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
        "Выбор после коммент_1" : partial(choice_from_comment_1, strapi_settings = strapi_settings),
        "Выбор после Доставка" : partial(choice_from_dostavka, strapi_settings = strapi_settings),
        "Выбор после Время": partial(choice_from_time, strapi_settings = strapi_settings),
        "Выбор после да нет": partial(choice_from_da_net, strapi_settings = strapi_settings),
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
        return get_dostavka(update, context, strapi_settings=strapi_settings)



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



def choice_from_dostavka(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts, dostavkas_parts = strapi_settings


    dostavka_id = order_status


    dostavka_property = {'data': {'carts': {'connect': [f'{cart_id}']}}}
    dostavka_url = f'{strapi_host}{strapi_port}/api/dostavkas/{dostavka_id}'
    dostavka_response = requests.put(dostavka_url, headers=strapi_headers, json=dostavka_property)
    dostavka_response.raise_for_status()

    keyboard = []

    da_callback_data = get_callback_data(cart_id=cart_id, action='Da')
    keyboard.append([InlineKeyboardButton('Добавить время доставки, имя, комментарии', callback_data=da_callback_data)])

    net_callback_data = get_callback_data(cart_id=cart_id, action='Net')
    keyboard.append([InlineKeyboardButton('Не добавлять', callback_data=net_callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    menu_text = '💬'
    context.bot.send_message(chat_id=query.message.chat_id, text=menu_text, reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

    return "Выбор после да нет"

def choice_from_da_net(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')

    if action == 'Da':
        return get_coomment_da(update, context, strapi_settings=strapi_settings)
    if action == 'Net':
        return get_coomment_net_choice_from_comment_2(update, context, strapi_settings=strapi_settings)



def get_coomment_da(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts, dostavkas_parts = strapi_settings

    text = 'Напишите, пожалуйста, время к которому подготовить заказ'
    context.bot.send_message(chat_id=query.message.chat_id, text=text)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return "Выбор после Время"



def choice_from_time(update, context, strapi_settings=None):

    time_reply_name = update.message.text
    chat_id_name = update.message.chat_id
    tg_id_for_strapi = f'tg_id_{chat_id_name}'
    past_cart_payload = {'filters[tg_id]': f'{tg_id_for_strapi}',
                         'sort': 'id:desc',
                         'pagination[pageSize]': 1}

    past_carts_url = f'{strapi_host}{strapi_port}/api/carts'
    past_cart_response = requests.get(past_carts_url, headers=strapi_headers, params=past_cart_payload)
    past_cart_response.raise_for_status()
    past_cart = past_cart_response.json()['data'][0]
    past_cart_id = past_cart['documentId']

    cart_time_property = {'data': {'Time': f'{time_reply_name}'}}
    cart_time_url = f'{strapi_host}{strapi_port}/api/carts/{past_cart_id}'
    cart_time_response = requests.put(cart_time_url, headers=strapi_headers, json=cart_time_property)
    cart_time_response.raise_for_status()

    text = 'Пришлите, пожалуйста, ваше имя'
    update.message.reply_text(text=text)

    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id - 1)


    return "Выбор после Имя"


def choice_from_order_name(update, context, strapi_settings=None):
    user_reply_name = update.message.text
    chat_id_name = update.message.chat_id
    tg_id_for_strapi = f'tg_id_{chat_id_name}'
    past_cart_payload = {'filters[tg_id]': f'{tg_id_for_strapi}',
                         'sort': 'id:desc',
                         'pagination[pageSize]': 1}

    past_carts_url = f'{strapi_host}{strapi_port}/api/carts'
    past_cart_response = requests.get(past_carts_url, headers=strapi_headers, params=past_cart_payload)
    past_cart_response.raise_for_status()
    past_cart = past_cart_response.json()['data'][0]
    past_cart_id = past_cart['documentId']

    cart_name_property = {'data': {'Name': f'{user_reply_name}'}}
    cart_name_url = f'{strapi_host}{strapi_port}/api/carts/{past_cart_id}'
    cart_name_response = requests.put(cart_name_url, headers=strapi_headers, json=cart_name_property)
    cart_name_response.raise_for_status()

    text = 'Напишите, пожалуйста, комм'
    update.message.reply_text(text=text)

    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id-1)
    return "Выбор после коммент_1"



def choice_from_comment_1(update, context, strapi_settings=None):
    strapi_host, strapi_port, strapi_headers, data_menu_parts, dostavkas_parts = strapi_settings
    try:
        products_url = f'{strapi_host}{strapi_port}/api/info'
        info_response = requests.get(products_url, headers=strapi_headers)
        info_response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    info_open_close = info_response.json()
    Open_Close = info_open_close['data']['Open_Close']
    Open_privetstvie = info_open_close['data']['Open_privetstvie']
    Close_privetstvie = info_open_close['data']['Close_privetstvie']

    if Open_Close:

        user_reply_name = update.message.text
        chat_id_name = update.message.chat_id
        tg_id_for_strapi = f'tg_id_{chat_id_name}'
        past_cart_payload = {'filters[tg_id]': f'{tg_id_for_strapi}',
                             'sort': 'id:desc',
                             'pagination[pageSize]': 1}

        past_carts_url = f'{strapi_host}{strapi_port}/api/carts'
        past_cart_response = requests.get(past_carts_url, headers=strapi_headers, params=past_cart_payload)
        past_cart_response.raise_for_status()
        past_cart = past_cart_response.json()['data'][0]
        past_cart_id = past_cart['documentId']

        cart_comment_payload = {'populate[cartitems][populate][0]': 'product'}
        cart_comment_property = {'data': {'Comment': f'{user_reply_name}'}}
        cart_comment_url = f'{strapi_host}{strapi_port}/api/carts/{past_cart_id}'
        cart_comment_response = requests.put(cart_comment_url, headers=strapi_headers, json=cart_comment_property, params=cart_comment_payload)
        cart_comment_response.raise_for_status()

        cart = cart_comment_response.json()

        zakaz_nomer = cart['data']['id']
        total = 0
        head_text = (f'-----------\n'
                     f'Заказ номер - *** {zakaz_nomer} ***\n'
                     f'-----------\n')
        body_text = ''

        for cartitem in cart['data']['cartitems']:
            cartitem_id = cartitem['documentId']
            title = cartitem['product']['title']
            price = cartitem['product']['price']
            quantity = cartitem['quantity']
            pre_total = price * quantity
            total = total + pre_total
            text_product = (f'● {title}\n'
                            f'Цена за ед.: {price}\n'
                            f'Кол-во: {quantity}\n'
                            f'Подитог: {pre_total}\n\n')
            body_text = body_text + text_product

        footer_text = (f'-----------\n\n'
                       f'Итого {total}')
        cart_description = head_text + body_text + footer_text

        update.message.reply_text(text=cart_description)

        text1 = (f'Скопируйте сообщение, которое выше\n'
                 f'и отправьте его в чат\n'
                 f'\n'
                 f'Спасибо!\n'
                 f'Ваша Ладушка!💕')
        update.message.reply_text(text=text1)

        text2 = (f'Чтобы оформить новый заказ, нажмите /start ')
        update.message.reply_text(text=text2)

        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id - 1)
        return ""

    else:
        update.message.reply_text(Close_privetstvie)



def get_coomment_net_choice_from_comment_2(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts, dostavkas_parts = strapi_settings
    try:
        products_url = f'{strapi_host}{strapi_port}/api/info'
        info_response = requests.get(products_url, headers=strapi_headers)
        info_response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    info_open_close = info_response.json()
    Open_Close = info_open_close['data']['Open_Close']
    Open_privetstvie = info_open_close['data']['Open_privetstvie']
    Close_privetstvie = info_open_close['data']['Close_privetstvie']

    print('info_open_close', info_open_close)

    if Open_Close:

        try:
            payload = {'populate[cartitems][populate][0]': 'product'}
            carts_url = f'{strapi_host}{strapi_port}/api/carts/{cart_id}/'
            response = requests.get(carts_url, headers=strapi_headers, params=payload)
            response.raise_for_status()
        except Exception as err:
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        cart = response.json()

        pprint(cart)

        zakaz_nomer = cart['data']['id']
        total = 0
        head_text = (f'-----------\n'
                     f'Заказ номер - *** {zakaz_nomer} ***\n'
                     f'-----------\n')
        body_text = ''

        for cartitem in cart['data']['cartitems']:
            cartitem_id = cartitem['documentId']
            title = cartitem['product']['title']
            price = cartitem['product']['price']
            quantity = cartitem['quantity']
            pre_total = price * quantity
            total = total + pre_total
            text_product = (f'● {title}\n'
                            f'Цена за ед.: {price}\n'
                            f'Кол-во: {quantity}\n'
                            f'Подитог: {pre_total}\n\n')
            body_text = body_text + text_product

        footer_text = (f'-----------\n\n'
                       f'Итого {total}')
        cart_description = head_text + body_text + footer_text

        query.message.reply_text(text=cart_description)

        text1 = (f'Скопируйте сообщение, которое выше\n'
                 f'и отправьте его в чат\n'
                 f'\n'
                 f'Спасибо!\n'
                 f'Ваша Ладушка!💕')
        query.message.reply_text(text=text1)

        text2 = (f'Чтобы оформить новый заказ, нажмите /start ')
        query.message.reply_text(text=text2)

        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id - 1)
        return ""

    else:
        update.message.reply_text(Close_privetstvie)



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


    try:
        dostavkas_payload = {'sort': 'Sortirovka'}
        dostavkas_url = f'{strapi_host}{strapi_port}/api/dostavkas'
        dostavkas_response = requests.get(dostavkas_url, params=dostavkas_payload, headers=strapi_headers)
        dostavkas_response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dostavkas_parts = dostavkas_response.json()['data']

    strapi_settings = [strapi_host, strapi_port, strapi_headers, data_menu_parts, dostavkas_parts]

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
