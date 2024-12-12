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


def get_dostavka(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts, dostavkas_parts = strapi_settings

    dostavka_keyboard = []
    for dostavka in dostavkas_parts:
        dostavka_title = dostavka['Dostavka']
        dostavka_id = dostavka['documentId']
        dostavka_callback_data = get_callback_data(cart_id=cart_id, action='Dos', order_status=dostavka_id)
        dostavka_keyboard.append([InlineKeyboardButton(dostavka_title, callback_data=dostavka_callback_data)])


    reply_markup = InlineKeyboardMarkup(dostavka_keyboard)

    menu_text = 'Получение заказа'
    context.bot.send_message(chat_id=query.message.chat_id, text=menu_text, reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)



    return "Выбор после Доставка"






