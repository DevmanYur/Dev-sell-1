from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from _0_functions import get_menu_parts_keyboard, get_footer_keyboard, get_callback_data


def get_all_menu(update, context, strapi_settings=None):
    query = update.callback_query
    query.answer()
    user_reply = query.data
    cart_id, product_id, action, count, cartitem_id, order_status, menu_part_id = user_reply.split('&')
    strapi_host, strapi_port, strapi_headers, data_menu_parts = strapi_settings

    keyboard =[]


    menu_parts_line_1, menu_parts_line_2 = get_menu_parts_keyboard(strapi_settings, cart_id)
    keyboard.append(menu_parts_line_1)
    keyboard.append(menu_parts_line_2)

    footer_keyboard = get_footer_keyboard(cart_id)
    keyboard.append(footer_keyboard)


    reply_markup = InlineKeyboardMarkup(keyboard)

    menu_text = 'Меню'
    context.bot.send_message(chat_id=query.message.chat_id, text=menu_text, reply_markup=reply_markup)
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    return 'Выбор после Корзины'