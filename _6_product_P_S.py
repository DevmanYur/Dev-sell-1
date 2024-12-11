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
from _1_start import bot_start
from _4_part_menu_MP import get_menu_part
from _5_cart_C_Ci import get_cart

logger = logging.getLogger(__name__)



def get_product(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    print(user_reply)
    print(len(user_reply))
    strapi_host, strapi_port, strapi_headers, data_menu_parts = strapi_settings


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

    count_kg = [1 ,2 ,3]

    keyboard = []
    keyboard_group = []
    for count in count_kg:
        callback_data = get_callback_data(cart_id = cart_id, product_id = product_id , action = 'S', count = str(count))
        keyboard_group.append(InlineKeyboardButton(f'+ {count}', callback_data=callback_data))
    keyboard.append(keyboard_group)



    menu_parts_line_1, menu_parts_line_2 = get_menu_parts_keyboard(strapi_settings, cart_id)
    keyboard.append(menu_parts_line_1)
    keyboard.append(menu_parts_line_2)

    cart_callback_data = get_callback_data(cart_id=cart_id, action='C')
    keyboard.append([InlineKeyboardButton("Корзина", callback_data=cart_callback_data)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=query.message.chat_id, text=text ,reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Продукта'
