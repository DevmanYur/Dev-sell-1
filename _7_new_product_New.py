import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from _0_functions import get_cart_keyboard, get_all_menu_keyboard, get_callback_data, get_new_product_keyboard


def get_new_product(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts, dostavkas_parts = strapi_settings
    menu_text = '🌞'
    keyboard = []
    novinki_payload = {'filters[Novinka][$eq]': 'True',
                       'populate': 'menu_part'}
    novinki_url = f'{strapi_host}{strapi_port}/api/products'
    novinki_response = requests.get(novinki_url, headers=strapi_headers, params=novinki_payload)
    novinki_response.raise_for_status()
    novinki = novinki_response.json()['data']
    if novinki == []:
        line_new_product_keyboard = []
        line_new_product_keyboard.append(get_new_product_keyboard(cart_id, 'здесь пока пусто'))
        keyboard.append(line_new_product_keyboard)
    else:
        line_new_product_keyboard = []
        line_new_product_keyboard.append(get_new_product_keyboard(cart_id, '🌞 новинки'))
        keyboard.append(line_new_product_keyboard)
        for novinka in novinki:
            novinka_keyboard = []
            novinka_menu_part_edinstvennoe_cislo = novinka['menu_part']['Edinstvennoe_cislo']
            novinka_product_title = novinka['title']
            novinka_product_id = novinka['documentId']
            novinka_title = f'{novinka_menu_part_edinstvennoe_cislo} - {novinka_product_title}'
            novinka_callback_data = get_callback_data(cart_id=cart_id, product_id=novinka_product_id, action='P')
            novinka_keyboard.append(InlineKeyboardButton(novinka_title, callback_data=novinka_callback_data))
            keyboard.append(novinka_keyboard)
    footer_keyboard = []
    footer_keyboard.append(get_all_menu_keyboard(cart_id, 'меню'))
    footer_keyboard.append(get_cart_keyboard(cart_id, 'корзина'))
    keyboard.append(footer_keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=query.message.chat_id, text=menu_text, reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после всего Новинки'
