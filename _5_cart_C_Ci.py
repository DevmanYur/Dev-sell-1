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

from _0_functions import get_callback_data, get_menu_parts_keyboard, get_all_menu_keyboard, get_order_keyboard

logger = logging.getLogger(__name__)


def get_cart(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts = strapi_settings
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

    pprint(cart)
    zakaz_nomer = cart['data']['id']
    total = 0
    head_text = (f'-----------\n'
                 f'Заказ номер - *** {zakaz_nomer} ***\n'
                 f'-----------\n')
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
                        f'Цена за ед.: {price}\n'
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

    footer_keyboard = []
    footer_keyboard.append(get_all_menu_keyboard(cart_id, 'меню'))
    footer_keyboard.append(get_order_keyboard(cart_id, 'Оформить заказ'))
    keyboard.append(footer_keyboard)

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text=cart_description,reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Корзины'



