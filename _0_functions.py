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


logger = logging.getLogger(__name__)


def get_callback_data(cart_id='_', product_id ='_', action='_', count='_', cartitem_id='_', order_status='_', menu_part_id ='_'):
    callback_data = f'{cart_id}&{product_id}&{action}&{count}&{cartitem_id}&{order_status}&{menu_part_id}'
    return callback_data


def get_menu_parts_keyboard(strapi_settings, cart_id):

    strapi_host, strapi_port, strapi_headers, data_menu_parts = strapi_settings

    menu_parts_line_1 = []
    menu_parts_line_2 = []

    nov_knopka_text = '🌞новинки'
    nov_callback_data = get_callback_data(cart_id=cart_id, action='New')
    menu_parts_line_1.append(InlineKeyboardButton(nov_knopka_text, callback_data=nov_callback_data))

    for menu_part in data_menu_parts[0:3]:
        title = menu_part['Menu_part']
        menu_part_id = menu_part['documentId']
        callback_data = get_callback_data(cart_id=cart_id, action='MP', menu_part_id=menu_part_id)
        menu_parts_line_1.append(InlineKeyboardButton(title, callback_data=callback_data))

    for menu_part in data_menu_parts[3:]:
        title = menu_part['Menu_part']
        menu_part_id = menu_part['documentId']
        callback_data = get_callback_data(cart_id=cart_id, action='MP', menu_part_id=menu_part_id)
        menu_parts_line_2.append(InlineKeyboardButton(title, callback_data=callback_data))

    return menu_parts_line_1, menu_parts_line_2


def get_about_keyboard(cart_id):
    about_text = 'о нас'
    about_action = 'AB'
    about_callback_data = get_callback_data(cart_id=cart_id, action=about_action)
    return InlineKeyboardButton(about_text, callback_data=about_callback_data)

def get_all_menu_keyboard(cart_id):
    all_menu_text = 'меню'
    all_menu_action = 'AM'
    all_menu_callback_data = get_callback_data(cart_id=cart_id, action=all_menu_action)
    return InlineKeyboardButton(all_menu_text, callback_data=all_menu_callback_data)

def get_cart_keyboard(cart_id):
    cart_text = 'корзина'
    cart_action = 'C'
    cart_callback_data = get_callback_data(cart_id=cart_id, action=cart_action)
    return InlineKeyboardButton(cart_text, callback_data=cart_callback_data)






