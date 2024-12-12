import html
import json
import logging
import os
from pprint import pprint
import requests
import telegram
from dotenv import load_dotenv
from io import BytesIO

from telegram import InlineKeyboardButton
from telegram.ext import Updater

from tg_bot_sell_fish import get_callback_data

load_dotenv()


def f1():
    ####555
    strapi_tokenq55 = os.getenv("STRAPI_TOKEN")
    headersq55 = {'Authorization': f'Bearer {strapi_tokenq55}'}
    response055 = requests.get(f'http://localhost:1337/api/products/zn17dtr0wv00kq32i0y8b3n1?populate=picture',
                               headers=headersq55)
    productq55 = response055.json()

    url_picq55 = productq55['data']['picture']['formats']['thumbnail']['url']

    name_photo55 = productq55['data']['picture']['formats']['thumbnail']['name']
    # name_photo = 'ddqq'
    response2255 = requests.get(f'http://localhost:1337{url_picq55}')
    response2255.raise_for_status()

    image_data2255 = BytesIO(response2255.content)
    img55 = Image.open(image_data2255)
    ####555
    img55.save('img3.png')


def f2():
    x = 'POST http://localhost:1337/api/restaurants'

    strapi_tokenq66 = os.getenv("STRAPI_TOKEN")
    headersq66 = {'Authorization': f'Bearer {strapi_tokenq66}'}
    response066 = requests.get(f'http://localhost:1337/api/carts', headers=headersq66)
    productq66 = response066.json()
    pprint(productq66)


def f3():
    strapi_tokenq667 = os.getenv("STRAPI_TOKEN")
    headersq667 = {'Authorization': f'Bearer {strapi_tokenq667}'}

    tg_id = '710011'
    tg_id_for_strapi = f'tg_id_{tg_id}'
    print(tg_id_for_strapi)

    data = {'data': {'tg_id': tg_id_for_strapi}}

    response0667 = requests.post(f'http://localhost:1337/api/carts', headers=headersq667, json=data)
    productq667 = response0667.json()
    pprint(productq667)


'''
{'data': [{'createdAt': '2024-11-21T13:29:51.740Z',
           'documentId': 'yyl0wssrpdz3oku2xidfnof9',
           'id': 2,
           'publishedAt': '2024-11-21T13:29:52.839Z',
           'tg_id': '1001',
           'updatedAt': '2024-11-21T13:29:52.823Z'}}

           {'data': ['tg_id': '10011'}}

'''


def f4():
    'GET /api/users?filters[username][$eq]=John'
    strapi_tokenq66 = os.getenv("STRAPI_TOKEN")
    headersq66 = {'Authorization': f'Bearer {strapi_tokenq66}'}
    tg_id = '710011'
    tg_id_for_strapi = f'tg_id_{tg_id}'
    response066 = requests.get(f'http://localhost:1337/api/carts?filters[tg_id][$eq]={tg_id_for_strapi}',
                               headers=headersq66)
    productq66 = response066.json()

    if productq66['data']:
        print("Блок А")
        print("здесь что то есть")
        print('documentId :', productq66['data'][0]['tg_id'])
        print('documentId :', productq66['data'][0]['documentId'])
    else:
        print("Блок Б")
        print("здесь пусто")
        print("создаем новый ")

        strapi_tokenq667 = os.getenv("STRAPI_TOKEN")
        headersq667 = {'Authorization': f'Bearer {strapi_tokenq667}'}

        data = {'data': {'tg_id': tg_id_for_strapi}}

        response0667 = requests.post(f'http://localhost:1337/api/carts', headers=headersq667, json=data)
        productq667 = response0667.json()
        print("Теперь: ")
        pprint(productq667)


def f5():
    strapi_tokenq66 = os.getenv("STRAPI_TOKEN")
    headersq66 = {'Authorization': f'Bearer {strapi_tokenq66}'}
    tg_id = '710011'
    tg_id_for_strapi = f'tg_id_{tg_id}'
    vremenno = '1001'
    response066 = requests.get(f'http://localhost:1337/api/carts?filters[tg_id][$eq]={vremenno}',
                               headers=headersq66)
    productq66 = response066.json()
    print("Блок А")
    print("здесь что то есть")
    print('tg_id :', productq66['data'][0]['tg_id'])
    print('documentId :', productq66['data'][0]['documentId'])

    print("===========")
    documentId_ = productq66['data'][0]['documentId']

    response = requests.get(f'http://localhost:1337/api/carts/{documentId_}?populate[cartitems][populate][0]=product',
                            headers=headersq66)
    productq667 = response.json()
    pprint(productq667)
    '?populate=cartitems'


def f6():
    strapi_tokenq667 = os.getenv("STRAPI_TOKEN")
    headersq667 = {'Authorization': f'Bearer {strapi_tokenq667}'}

    data = {'data': {'quantity': 200,
                     'product': 'ylokeva71vdpe8xxs57nxdnv',
                     'cart': 'efsb9hcihq106x3jj5s9ut2r'

                     }}
    response0667 = requests.post(f'http://localhost:1337/api/cartitems', headers=headersq667, json=data)
    productq667 = response0667.json()
    pprint(productq667)

    gg = '''{
  data: {
    categories: {
      set: ['z0y2x4w6v8u1t3s5r7q9onm', 'j9k8l7m6n5o4p3q2r1s0tuv4'],
    }
  }
}

    '''


'''
/api/books
?
sort[0]=title:asc
&
filters[title][$eq]=hello
&
populate[author][fields][0]=firstName
&
populate[author][fields][1]=lastName
&
fields[0]=title
&
pagination[pageSize]=10
&
pagination[page]=1
&
status=published
&
locale=en

populate[0]=relation-name
&
populate[1]=another-relation-name
&
populate[2]=yet-another-relation-name

GET /api/articles?
populate[category][populate][0]=restaurants

cart_id = 't2ojovli96gdsak5sl9dv205' 

product_id = 'zj4b4o2vs8dyk6k5xcl88dec'


, action, count
t2ojovli96gdsak5sl9dv205 zj4b4o2vs8dyk6k5xcl88dec S 2 _ _
'''


def f7():
    strapi_tokenq667 = os.getenv("STRAPI_TOKEN")
    headersq667 = {'Authorization': f'Bearer {strapi_tokenq667}'}
    response0667 = requests.get(
        f'http://localhost:1337/api/cartitems/ihudrhuxqbyo8z9rbeiw09ku?populate=product&populate=cart',
        headers=headersq667)
    productq667 = response0667.json()
    pprint(productq667)


'''
{'data': {'cart': {'createdAt': '2024-11-21T13:29:51.740Z',
                   'documentId': 'yyl0wssrpdz3oku2xidfnof9',
                   'id': 2,
                   'publishedAt': '2024-11-21T13:29:52.839Z',
                   'tg_id': '1001',
                   'updatedAt': '2024-11-21T13:29:52.823Z'},
          'createdAt': '2024-11-21T13:30:39.847Z',
          'documentId': 'ihudrhuxqbyo8z9rbeiw09ku',
          'id': 2,
          'product': {'createdAt': '2024-11-12T07:11:08.174Z',
                      'description': 'Вес: 80-110 гр/штука Кол-во: 9-11 штук в '
                                     '1 кг.',
                      'documentId': 'ylokeva71vdpe8xxs57nxdnv',
                      'id': 8,
                      'price': 3800,
                      'publishedAt': '2024-11-12T07:11:08.189Z',
                      'title': 'Живые раки (отборные)',
                      'updatedAt': '2024-11-12T07:11:08.174Z'},
          'publishedAt': '2024-11-21T13:30:40.987Z',
          'quantity': 1,
          'updatedAt': '2024-11-21T13:30:40.977Z'},
 'meta': {}}
'''


def post_cartitems(cart, product, quantity):
    strapi_tokenq667 = os.getenv("STRAPI_TOKEN")
    headersq667 = {'Authorization': f'Bearer {strapi_tokenq667}'}

    data = {'data': {'quantity': quantity,
                     'product': product,
                     'cart': cart
                     }}
    response0667 = requests.post(f'http://localhost:1337/api/cartitems', headers=headersq667, json=data)
    productq667 = response0667.json()


def f8():
    load_dotenv()

    strapi_tokenq = os.getenv("STRAPI_TOKEN")
    headers = {'Authorization': f'Bearer {strapi_tokenq}'}

    cart_id = 'iezhajtnx24ckph2y74y5xxo'

    response = requests.get(
        f'http://localhost:1337/api/carts/{cart_id}?populate[cartitems][populate][0]=product', headers=headers)

    cartitems = response.json()
    total = 0
    head_text = (f'Моя корзина:\n'
                 f'-----------\n\n')
    body_text = ''

    footer_text = (f'-----------\n\n'
                   f'Итого {total}')

    for cartitem in cartitems['data']['cartitems']:
        print(cartitem['documentId'])
        title = cartitem['product']['title']
        price = cartitem['product']['price']
        quantity = cartitem['quantity']
        pre_total = price * quantity
        total = total + pre_total
        text_product = (f'● {title}\n'
                        f'Цена за кг: {price}\n'
                        f'Кол-во: {quantity}\n'
                        f'Подитог: {pre_total}\n\n')
        body_text = body_text + text_product

    text = head_text + body_text + footer_text

    pprint(text)

    # tg_id = '710011'
    # tg_id_for_strapi = f'tg_id_{tg_id}'
    # vremenno = '1001'
    # response066 = requests.get(f'http://localhost:1337/api/carts?filters[tg_id][$eq]={vremenno}',
    #                            headers=headersq66)


def f9():
    load_dotenv()
    strapi_tokenq = os.getenv("STRAPI_TOKEN")
    headers = {'Authorization': f'Bearer {strapi_tokenq}'}

    cart_id = 'ljpwh8c237ohammcj7uam7dg'

    product_id = 'zj4b4o2vs8dyk6k5xcl88dec'

    response = requests.get(f'http://localhost:1337/api/cartitems?'
                            f'populate=*'
                            f''
                            f'&'
                            f'filters[cart][documentId][$eq]={cart_id}'
                            f'&'
                            f'filters[product][documentId][$eq]={product_id}', headers=headers)

    cartitem = response.json()

    if cartitem['data'] == []:
        print("Не нашел")
        print(cartitem['data'])
    if cartitem['data'] != []:
        print("Нашел")
        pprint(cartitem['data'][-1])

    # pprint(cartitem['data'])
    # pprint(cartitem['data'][0]['documentId'])
    # cartitem_documentId = cartitem['data'][0]['documentId']
    # print(cartitem_documentId)


'''
ljpwh8c237ohammcj7uam7dg zj4b4o2vs8dyk6k5xcl88dec S 2 _ _
пусто
ljpwh8c237ohammcj7uam7dg ylokeva71vdpe8xxs57nxdnv
'''
'''
{'data': [{'cart': {'createdAt': '2024-11-21T13:29:51.740Z',
                    'documentId': 'yyl0wssrpdz3oku2xidfnof9',
                    'id': 2,
                    'publishedAt': '2024-11-21T13:29:52.839Z',
                    'tg_id': '1001',
                    'updatedAt': '2024-11-21T13:29:52.823Z'},
           'createdAt': '2024-11-21T13:30:39.847Z',
           'documentId': 'ihudrhuxqbyo8z9rbeiw09ku',
           'id': 2,
           'product': {'createdAt': '2024-11-12T07:11:08.174Z',
                       'description': 'Вес: 80-110 гр/штука Кол-во: 9-11 штук '
                                      'в 1 кг.',
                       'documentId': 'ylokeva71vdpe8xxs57nxdnv',
                       'id': 8,
                       'price': 3800,
                       'publishedAt': '2024-11-12T07:11:08.189Z',
                       'title': 'Живые раки (отборные)',
                       'updatedAt': '2024-11-12T07:11:08.174Z'},
           'publishedAt': '2024-11-21T13:30:40.987Z',
           'quantity': 1,
           'updatedAt': '2024-11-21T13:30:40.977Z'},

'''
import io
from io import BytesIO
from pprint import pprint

import requests

# with open(filename, 'wb') as file:
#     file.write(response.content)


def f10(strapi_settings):
    strapi_host, strapi_port, strapi_headers = strapi_settings

    cart_id = ''
    product_id= ''
    action= ''
    count= ''
    cartitem_id= ''
    order_status= ''

    products_url = f'{strapi_host}{strapi_port}/api/info'
    response = requests.get(products_url, headers=strapi_headers)
    response.raise_for_status()

    info_open_close = response.json()
    Open_Close = info_open_close['data']['Open_Close']
    Open_privetstvie = info_open_close['data']['Open_privetstvie']
    Close_privetstvie = info_open_close['data']['Close_privetstvie']

    if Open_Close :
        print(Open_privetstvie)
    else:
        print(Close_privetstvie)



def f11(strapi_settings):
    strapi_host, strapi_port, strapi_headers = strapi_settings

    cart_id = ''
    product_id = ''
    action = ''
    count = ''
    cartitem_id = ''
    order_status = ''

    # products_url = f'{strapi_host}{strapi_port}/api/menu-parts'
    # response = requests.get(products_url, headers=strapi_headers)
    # response.raise_for_status()

    menu_part_id = 'nm2uggzzhte2cstrvzd3s41n'

    payload = {'populate': 'products'}
    menu_part_url = f'{strapi_host}{strapi_port}/api/menu-parts/{menu_part_id}/'
    response = requests.get(menu_part_url, headers=strapi_headers, params=payload)
    response.raise_for_status()

    pprint(response.json())

    menu_parts = response.json()

    '''
    {'data': [{'Menu_part': 'Блины',
           'createdAt': '2024-12-02T20:28:25.767Z',
           'documentId': 'l9yk345fh56nuwsmyz8lfzg5',
           'id': 3,
           'publishedAt': '2024-12-08T11:08:08.048Z',
           'updatedAt': '2024-12-08T11:08:08.032Z'},
          {'Menu_part': 'Супы',
           'createdAt': '2024-12-08T11:13:14.397Z',
           'documentId': 'nm2uggzzhte2cstrvzd3s41n',
           'id': 7,
           'publishedAt': '2024-12-08T11:13:14.410Z',
           'updatedAt': '2024-12-08T11:13:14.397Z'},
    '''


def f12(strapi_settings):
    strapi_host, strapi_port, strapi_headers = strapi_settings

    cart_id = ''
    product_id = ''
    action = ''
    count = ''
    cartitem_id = ''
    order_status = ''

    # products_url = f'{strapi_host}{strapi_port}/api/menu-parts'
    # response = requests.get(products_url, headers=strapi_headers)
    # response.raise_for_status()
    # populate[categories][sort][0]=name



    payload = {'sort': 'Sortirovka',
               'populate': 'products'
               }
    menu_part_url = f'{strapi_host}{strapi_port}/api/menu-parts'
    response = requests.get(menu_part_url, headers=strapi_headers, params=payload)
    response.raise_for_status()

    pprint(response.json())

    menu_parts = response.json()

    print(response.url)



def f13(strapi_settings):
    strapi_host, strapi_port, strapi_headers = strapi_settings

    novinka_payload = {'filters[Novinka][$eq]': 'True',
                       'populate': 'menu_part'}
    novinka_url = f'{strapi_host}{strapi_port}/api/products'
    novinka_response = requests.get(novinka_url, headers=strapi_headers, params=novinka_payload)
    novinka_response.raise_for_status()
    novinki = novinka_response.json()['data']

    if novinki == []:
        print("Новинки нет")

    else:
        knopka_text = 'Новинка'

        for novinka in novinki:
            menu_part = novinka['menu_part']['Menu_part']
            product_title = novinka['title']
            product_id = novinka['documentId']
            print( menu_part, product_title, product_id)

    # >> > lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # >> > list(zip(lst[::2], lst[1::2]))




def f14(strapi_settings):
    strapi_host, strapi_port, strapi_headers = strapi_settings

    novinka_url = f'{strapi_host}{strapi_port}/api/products'
    novinka_response = requests.get(novinka_url, headers=strapi_headers)
    novinka_response.raise_for_status()
    novinki = novinka_response.json()['data']

    # pprint(novinki)

    novinki_11 = [10,20,30,40,50,60,70,80, 90]

    print(len(novinki_11))

    xxx = list(map(list, zip(novinki_11[::2], novinki_11[1::2])))

    fff = []
    for dd in xxx:
        fff.append(dd)


    if len(novinki_11)%2 > 0:
        novinki_11[-1]
        print(novinki_11[-1])

        eee = [novinki_11[-1]]
        fff.append(eee)




    pprint(fff)



def f15():
    cart_id = 1
    menu_part_id = 'xzplclrpkpmeb0u7ivdaa6bb'
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
        last_product_title = [products[-1]['title']]
        print(last_product_title)
        last_product_id = [products[-1]['documentId']]
        print(last_product_id)
        last_callback_data = get_callback_data(cart_id=cart_id, product_id=last_product_id, action='P')
        keyboard_group.append(InlineKeyboardButton(last_product_title, callback_data=last_callback_data))
        keyboard.append(keyboard_group)


    pprint(keyboard)




def f16(strapi_settings):
    strapi_host, strapi_port, strapi_headers = strapi_settings

    # novinka_payload = {'filters[Novinka][$eq]': 'True',
    #                    'populate': 'menu_part'}
    # novinka_url = f'{strapi_host}{strapi_port}/api/products'
    # novinka_response = requests.get(novinka_url, headers=strapi_headers, params=novinka_payload)
    # novinka_response.raise_for_status()
    # novinki = novinka_response.json()['data']
    #
    # tg_id_for_strapi = f'tg_id_{tg_id}'
    # carts_url = f'{strapi_host}{strapi_port}/api/carts'
    # payload = {'data': {'tg_id': tg_id_for_strapi}}
    # response = requests.post(carts_url, headers=strapi_headers, json=payload)
    # response.raise_for_status()

    # payload = {'data': {'tg_id': tg_id_for_strapi}}

    tg_id = 'tg_id_1076073346'

    past_cart_payload = {'filters[tg_id]': f'{tg_id}',
               'sort': 'id:desc',
               'pagination[pageSize]':1}

    past_carts_url = f'{strapi_host}{strapi_port}/api/carts'
    past_cart_response = requests.get(past_carts_url, headers=strapi_headers, params=past_cart_payload)
    past_cart_response.raise_for_status()
    past_cart = past_cart_response.json()['data'][0]
    past_cart_id = past_cart['documentId']






if __name__ == '__main__':
    load_dotenv()

    strapi_token = os.getenv("STRAPI_TOKEN")
    strapi_host = os.getenv("STRAPI_HOST")
    strapi_port = os.getenv("STRAPI_PORT")
    strapi_headers = {'Authorization': f'Bearer {strapi_token}'}
    strapi_settings = [strapi_host, strapi_port, strapi_headers]

    f16(strapi_settings)

