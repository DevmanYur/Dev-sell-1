import logging
import requests
from telegram import InlineKeyboardMarkup
from _0_functions import  get_menu_parts_keyboard
logger = logging.getLogger(__name__)


def bot_start(update, context, strapi_settings=None):
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
        keyboard = []
        menu_parts_line_1, menu_parts_line_2 = get_menu_parts_keyboard(strapi_settings, new_cart_id)
        keyboard.append(menu_parts_line_1)
        keyboard.append(menu_parts_line_2)
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text=text, reply_markup=reply_markup)
        return "Выбор после start"
    else:
        update.message.reply_text(Close_privetstvie)