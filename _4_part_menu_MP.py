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

from _0_functions import get_callback_data, get_menu_parts_keyboard, get_footer_keyboard

logger = logging.getLogger(__name__)




def get_menu_part(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    cart_callback_data = get_callback_data(cart_id=cart_id, action='C')
    strapi_host, strapi_port, strapi_headers, data_menu_parts = strapi_settings

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

    all_products_each = list(map(list, zip(products[::2], products[1::2])))
    for two_products_each in all_products_each:
        keyboard_group = []
        for product in two_products_each:
            title = product['title']
            product_id = product['documentId']
            callback_data = get_callback_data(cart_id=cart_id, product_id=product_id, action='P')
            keyboard_group.append(InlineKeyboardButton(title, callback_data=callback_data))
        keyboard.append(keyboard_group)

    if len(products)%2 > 0:
        keyboard_group = []
        last_product_title = products[-1]['title']
        last_product_id = products[-1]['documentId']
        last_callback_data = get_callback_data(cart_id=cart_id, product_id=last_product_id, action='P')
        keyboard_group.append(InlineKeyboardButton(last_product_title, callback_data=last_callback_data))
        keyboard.append(keyboard_group)



    footer_keyboard = get_footer_keyboard(cart_id)
    keyboard.append(footer_keyboard)


    reply_markup = InlineKeyboardMarkup(keyboard)

    text = menu_part['Menu_part']
    context.bot.send_message(chat_id=query.message.chat_id, text=text,reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Меню раздел'



