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


def get_order_name(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    text = 'Пришлите, пожалуйста, ваше имя'
    context.bot.send_message(chat_id=query.message.chat_id, text=text)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return "Выбор после Имя"




