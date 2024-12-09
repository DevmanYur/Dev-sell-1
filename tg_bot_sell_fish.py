import os
import logging
from functools import partial

import redis
import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler


logger = logging.getLogger(__name__)


_database = None


def get_database_connection(database_settings):
    global _database
    database_host, database_port, database_password = database_settings
    if _database is None:
        _database = redis.Redis(host=database_host, port=database_port, password=database_password)
    return _database


def get_callback_data(cart_id='_', product_id ='_', action='_', count='_', cartitem_id='_', order_status='_', menu_part_id ='_'):
    callback_data = f'{cart_id}&{product_id}&{action}&{count}&{cartitem_id}&{order_status}&{menu_part_id}'
    return callback_data


def handle_users_reply(update, context, strapi_settings=None, database_settings =None):
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
        'START': partial(start, strapi_settings = strapi_settings),
        'Выбор после start': partial(choice_from_start, strapi_settings = strapi_settings),
        'Выбор после Меню': partial(choice_from_menu, strapi_settings = strapi_settings),
        'Выбор после Меню раздел': partial(choice_from_menu_part, strapi_settings=strapi_settings),
        'Выбор после Корзины': partial(choice_from_cart, strapi_settings = strapi_settings),
        'Выбор после Продукта' : partial(choice_from_product, strapi_settings = strapi_settings),
        "Выбор после e-mail" : partial(choice_from_email, strapi_settings = strapi_settings),
        "Выбор после телефона" : partial(choice_from_phone, strapi_settings = strapi_settings),
    }
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context, strapi_settings=None):
    strapi_host, strapi_port, strapi_headers = strapi_settings

    try:
        products_url = f'{strapi_host}{strapi_port}/api/info'
        response = requests.get(products_url, headers=strapi_headers)
        response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    info_open_close = response.json()
    Open_Close = info_open_close['data']['Open_Close']
    Open_privetstvie = info_open_close['data']['Open_privetstvie']
    Close_privetstvie = info_open_close['data']['Close_privetstvie']

    if Open_Close:
        text = Open_privetstvie
        tg_id = update.message.chat_id

        try:
            tg_id_for_strapi = f'tg_id_{tg_id}'
            carts_url = f'{strapi_host}{strapi_port}/api/carts'
            payload = {'data': {'tg_id': tg_id_for_strapi}}
            response = requests.post(carts_url, headers=strapi_headers, json=payload)
            response.raise_for_status()
        except Exception as err:
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        cart = response.json()
        new_cart_id = cart['data']['documentId']
        menu_callback_data = get_callback_data(cart_id=new_cart_id, action='M')
        cart_callback_data = get_callback_data(cart_id=new_cart_id, action='C')
        keyboard = []
        keyboard.append([InlineKeyboardButton("Меню", callback_data=menu_callback_data)])
        keyboard.append([InlineKeyboardButton("Корзина", callback_data=cart_callback_data)])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text=text, reply_markup=reply_markup)
        return "Выбор после start"

    else:
        update.message.reply_text(Close_privetstvie)


def choice_from_start(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if  action =='M':
        return get_menu(update, context, strapi_settings=strapi_settings)

    if action =='C':
        return get_cart(update, context, strapi_settings=strapi_settings)


def choice_from_menu(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action == 'MP':
        return get_menu_part(update, context, strapi_settings=strapi_settings)

    if action == 'C':
        return get_cart(update, context, strapi_settings=strapi_settings)


def choice_from_menu_part(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action == 'P':
        return get_product(update, context, strapi_settings=strapi_settings)

    if action == 'C':
        return get_cart(update, context, strapi_settings=strapi_settings)


def choice_from_cart(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action =='Ci':
        return get_cart(update, context, strapi_settings=strapi_settings)

    if action =='M':
        return get_menu(update, context, strapi_settings=strapi_settings)

    if action =='Or':
        return  get_order(update, context, strapi_settings=strapi_settings)


def choice_from_product(update, context, strapi_settings=None):
    user_reply = update.callback_query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    if action == 'S':
        return get_product(update, context, strapi_settings=strapi_settings)

    if action == 'M':
        return get_menu(update, context, strapi_settings=strapi_settings)

    if action == 'C':
        return get_cart(update, context, strapi_settings=strapi_settings)


def choice_from_email(update, context, strapi_settings=None):
    text = 'Введите телефон'
    update.message.reply_text(text=text)
    return "Выбор после телефона"


def choice_from_phone(update, context, strapi_settings=None):
    text = 'Заказ оформлен'
    update.message.reply_text(text=text)
    return ''


def get_menu(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    cart_callback_data = get_callback_data(cart_id=cart_id, action='C')
    strapi_host, strapi_port, strapi_headers = strapi_settings
    try:
        payload = {'sort': 'Sortirovka'}
        products_url = f'{strapi_host}{strapi_port}/api/menu-parts'
        response = requests.get(products_url, params=payload , headers=strapi_headers)
        response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    menu_parts = response.json()['data']



    try :
        novinka_payload = {'filters[Novinka][$eq]': 'True',
                           'populate': 'menu_part'}
        novinka_url = f'{strapi_host}{strapi_port}/api/products'
        novinka_response = requests.get(novinka_url, headers=strapi_headers, params=novinka_payload)
        novinka_response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    novinki = novinka_response.json()['data']

    keyboard = []
    keyboard_group = []
    keyboard_line_1 = []
    keyboard_line_2 = []
    keyboard_line_3 = []

    if novinki == []:
        print("Новинки нет")
        for menu_part in menu_parts:
            title = menu_part['Menu_part']
            menu_part_id = menu_part['documentId']
            callback_data = get_callback_data(cart_id=cart_id, action='MP', menu_part_id = menu_part_id)
            keyboard_group.append(InlineKeyboardButton(title, callback_data=callback_data))
        keyboard.append(keyboard_group)
        keyboard.append([InlineKeyboardButton("Корзина", callback_data=cart_callback_data)])
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=query.message.chat_id, text="Меню",reply_markup=reply_markup)
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        return 'Выбор после Меню'

    else:
        nov_knopka_text = '🌞новинка'
        nov_callback_data = get_callback_data(cart_id=cart_id, action='New')
        keyboard_group.append(InlineKeyboardButton(nov_knopka_text, callback_data=nov_callback_data))

        for menu_part in menu_parts:
            title = menu_part['Menu_part']
            menu_part_id = menu_part['documentId']
            callback_data = get_callback_data(cart_id=cart_id, action='MP', menu_part_id = menu_part_id)
            keyboard_group.append(InlineKeyboardButton(title, callback_data=callback_data))
        keyboard.append(keyboard_group)
        keyboard.append([InlineKeyboardButton("Корзина", callback_data=cart_callback_data)])
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=query.message.chat_id, text="Меню",reply_markup=reply_markup)
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        return 'Выбор после Меню'




def get_cart(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers = strapi_settings
    if action == 'Ci':
        try:
            cartitems_url = f'{strapi_host}{strapi_port}/api/cartitems/{cartitem_id}'
            response = requests.delete(cartitems_url, headers=strapi_headers)
            response.raise_for_status()
        except Exception as err:
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    try:
        payload = {'populate[cartitems][populate][0]': 'product'}
        carts_url = f'{strapi_host}{strapi_port}/api/carts/{cart_id}/'
        response = requests.get(carts_url, headers=strapi_headers, params=payload)
        response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    cart = response.json()
    total = 0
    head_text = (f'Моя корзина:\n'
                 f'-----------\n\n')
    body_text = ''

    keyboard = []
    for cartitem in cart['data']['cartitems']:
        cartitem_id = cartitem['documentId']
        title = cartitem['product']['title']
        price = cartitem['product']['price']
        quantity = cartitem['quantity']
        pre_total = price * quantity
        total = total + pre_total
        text_product = (f'● {title}\n'
                        f'Цена за кг: {price}\n'
                        f'Кол-во: {quantity}\n'
                        f'Подитог: {pre_total}\n\n')
        body_text = body_text + text_product

        callback_data = get_callback_data(cart_id=cart_id, action='Ci', cartitem_id=cartitem_id)
        keyboard_group = []
        keyboard_group.append(InlineKeyboardButton(f'Удалить {title}', callback_data=callback_data))
        keyboard.append(keyboard_group)
    footer_text = (f'-----------\n\n'
                   f'Итого {total}')
    cart_description = head_text + body_text + footer_text
    menu_callback_data = get_callback_data(cart_id=cart_id, action='M')
    order_callback_data = get_callback_data(cart_id=cart_id, action='Or')
    keyboard.append([InlineKeyboardButton("Меню", callback_data=menu_callback_data)])
    keyboard.append([InlineKeyboardButton('Оформить заказ', callback_data=order_callback_data)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text=cart_description,reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Корзины'


def get_order(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    text = 'Пришлите, пожалуйста, ваш e-mail'
    context.bot.send_message(chat_id=query.message.chat_id, text=text)
    return "Выбор после e-mail"


def get_product(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    print(user_reply)
    print(len(user_reply))
    strapi_host, strapi_port, strapi_headers = strapi_settings
    if action == 'S':
        try:
            cartitems_url = f'{strapi_host}{strapi_port}/api/cartitems/'
            payload = {'filters[cart][documentId][$eq]': f'{cart_id}',
                       'filters[product][documentId][$eq]': f'{product_id}'}
            response = requests.get(cartitems_url, headers=strapi_headers, params=payload)
            response.raise_for_status()

        except Exception as err:
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        cartitem = response.json()

        if cartitem['data'] == []:
            try:
                cartitem_property = {'data': {'quantity': count,
                                              'product': product_id,
                                              'cart': cart_id}}
                cartitems_url = f'{strapi_host}{strapi_port}/api/cartitems'
                response = requests.post(cartitems_url, headers=strapi_headers, json=cartitem_property)
                response.raise_for_status()
            except Exception as err:
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        if cartitem['data'] != []:
            cartitem_doc_id = cartitem['data'][0]['documentId']
            before_quantity = cartitem['data'][0]['quantity']
            after_quantity = int(before_quantity) + int(count)

            try:
                cartitem_property = {'data': {'quantity': after_quantity}}
                cartitems_url = f'{strapi_host}{strapi_port}/api/cartitems/{cartitem_doc_id}'
                response = requests.put(cartitems_url, headers=strapi_headers, json=cartitem_property)
                response.raise_for_status()
            except Exception as err:
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    try:
        product_url = f'{strapi_host}{strapi_port}/api/products/{product_id}'
        response = requests.get(product_url, headers=strapi_headers)
        response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        
    product = response.json()
    title = product['data']['title']
    price = product['data']['price']
    description = product['data']['description']

    text = (f'{title}\n'
            f'\n'
            f'Цена {price}\n'
            f'\n'
            f'{description}\n'
            f'\n')

    count_kg = [1,2,3]

    keyboard = []
    keyboard_group = []
    for count in count_kg:
        callback_data = get_callback_data(cart_id = cart_id, product_id = product_id , action = 'S', count = str(count))
        keyboard_group.append(InlineKeyboardButton(f'+ {count}', callback_data=callback_data))
    keyboard.append(keyboard_group)
    menu_callback_data = get_callback_data(cart_id=cart_id, action='M')
    cart_callback_data = get_callback_data(cart_id=cart_id, action='C')

    keyboard.append([InlineKeyboardButton("Меню", callback_data=menu_callback_data)])
    keyboard.append([InlineKeyboardButton("Корзина", callback_data=cart_callback_data)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=query.message.chat_id, text=text,reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Продукта'



def get_menu_part(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    cart_callback_data = get_callback_data(cart_id=cart_id, action='C')
    strapi_host, strapi_port, strapi_headers = strapi_settings

    try:
        payload = {'populate': 'products'}
        menu_part_url = f'{strapi_host}{strapi_port}/api/menu-parts/{menu_part_id}/'
        response = requests.get(menu_part_url, headers=strapi_headers, params=payload)
        response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    menu_part = response.json()['data']

    products = menu_part['products']
    keyboard = []
    for product in products:
        title = product['title']
        product_id = product['documentId']
        callback_data = get_callback_data(cart_id=cart_id, product_id=product_id, action='P')
        keyboard_group = []
        keyboard_group.append(InlineKeyboardButton(title, callback_data=callback_data))
        keyboard.append(keyboard_group)
    keyboard.append([InlineKeyboardButton("Корзина", callback_data=cart_callback_data)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = menu_part['Menu_part']
    context.bot.send_message(chat_id=query.message.chat_id, text=text,reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Меню раздел'




if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()

    strapi_token = os.getenv("STRAPI_TOKEN")
    strapi_host = os.getenv("STRAPI_HOST")
    strapi_port = os.getenv("STRAPI_PORT")
    strapi_headers = {'Authorization': f'Bearer {strapi_token}'}
    strapi_settings = [strapi_host, strapi_port, strapi_headers]

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
