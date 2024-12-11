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
from _1_start import bot_start
from _4_part_menu_MP import get_menu_part
from _5_cart_C_Ci import get_cart

logger = logging.getLogger(__name__)



def get_product(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts = strapi_settings


    # Now
    try:
        now_cartitems_url = f'{strapi_host}{strapi_port}/api/cartitems/'
        now_payload = {'filters[cart][documentId][$eq]': f'{cart_id}',
                   'filters[product][documentId][$eq]': f'{product_id}'}
        now_response = requests.get(now_cartitems_url, headers=strapi_headers, params=now_payload)
        now_response.raise_for_status()

    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    now_cartitem = now_response.json()

    if now_cartitem['data'] == []:
        now_quantity = 0

    if now_cartitem['data'] != []:
        now_quantity = now_cartitem['data'][0]['quantity']
    # Now


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

        pprint(cartitem)

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

            now_quantity = count

        if cartitem['data'] != []:
            cartitem_doc_id = cartitem['data'][0]['documentId']
            before_quantity = cartitem['data'][0]['quantity']

            after_quantity = int(before_quantity) + int(count)
            now_quantity = after_quantity

            try:
                cartitem_property = {'data': {'quantity': after_quantity}}
                cartitems_url = f'{strapi_host}{strapi_port}/api/cartitems/{cartitem_doc_id}'
                response = requests.put(cartitems_url, headers=strapi_headers, json=cartitem_property)
                response.raise_for_status()
            except Exception as err:
                logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



    try:
        payload = {'populate': 'menu_part'}
        product_url = f'{strapi_host}{strapi_port}/api/products/{product_id}'
        response = requests.get(product_url, headers=strapi_headers,  params=payload)
        response.raise_for_status()
    except Exception as err:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    product = response.json()


    menu_part_edinstvennoe_cislo = product['data']['menu_part']['Edinstvennoe_cislo']
    title = product['data']['title']
    price = product['data']['price']


    description = product['data']['description']

    text = (f'{menu_part_edinstvennoe_cislo} - {title}\n'
            f'\n'
            f'Цена {price}\n'
            f'\n'
            f'{description}\n'
            f'\n'
            f'в корзине {now_quantity}')

    count_kg = [1 ,2 ,3]

    keyboard = []

    keyboard_group_lone_1 = []

    callback_1_data = get_callback_data(cart_id = cart_id, product_id = product_id , action = 'S', count = str(count_kg[0]))
    keyboard_group_lone_1.append(InlineKeyboardButton(f'+ {count_kg[0]}', callback_data=callback_1_data))

    callback_1_data = get_callback_data(cart_id=cart_id, product_id=product_id, action='S', count=str(count_kg[1]))
    keyboard_group_lone_1.append(InlineKeyboardButton(f'+ {count_kg[1]}', callback_data=callback_1_data))

    callback_1_data = get_callback_data(cart_id=cart_id, product_id=product_id, action='S', count=str(count_kg[2]))
    keyboard_group_lone_1.append(InlineKeyboardButton(f'+ {count_kg[2]}', callback_data=callback_1_data))
    keyboard.append(keyboard_group_lone_1)


    menu_part_title = product['data']['menu_part']['Menu_part']
    menu_part_id = product['data']['menu_part']['documentId']




    print(menu_part_title)
    print(menu_part_id)
    menu_part_callback_data = get_callback_data(cart_id=cart_id, action='MP', menu_part_id=menu_part_id)
    keyboard.append([InlineKeyboardButton(f'посмотреть другие {menu_part_title}', callback_data=menu_part_callback_data)])


    footer_keyboard = get_footer_keyboard(cart_id)
    keyboard.append(footer_keyboard)


    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=query.message.chat_id, text=text ,reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Продукта'
