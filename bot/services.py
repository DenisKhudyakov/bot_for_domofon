import aiohttp, asyncio

from bot.config import TELEPHONE, SECRET_KEY

BASE_URL = "https://domo-dev.profintel.ru/tg-bot"


HEADERS = {
  'x-api-key': SECRET_KEY
}


def connection(func):
    """Декоратор для создания сессии"""
    async def wrapper(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await func(session, *args, **kwargs)

    return wrapper


@connection
async def fetch_json(session, url, headers=None, params=None, method='GET'):
    """
    Функция извлечения данных POST запроса
    :param session:
    :param url:
    :param headers:
    :param data:
    :return:
    """
    if method == 'POST':
        async with session.post(url, headers=headers, json=params) as response:
            print(response.status)
            return await response.json()
    elif method == 'GET':
        async with session.get(url, headers=headers, json=params) as response:
            print(response.status)
            return await response.json()


async def get_id():
    """
    Функция получение номера ID жильца в системе по его номеру телефона
    :return:
    """
    data = {
        'phone': TELEPHONE,
    }
    url_for_id = BASE_URL + '/check-tenant'
    response = await fetch_json(url=url_for_id, headers=HEADERS, params=data, method='POST')
    return response.get('tenant_id')


async def get_float():
    """
    Получение списка квартир, в которых состоит жилец
    :param tenant_id: ID жильца
    :return:
    """
    tenant_id = await get_id()
    if not tenant_id:
        raise ValueError("Не удалось получить tenant_id.")

    print(f"Получен tenant_id: {tenant_id}")

    url_for_apartment = BASE_URL + f'/domo.apartment?tenant_id={tenant_id}'
    response = await fetch_json(url=url_for_apartment, headers=HEADERS, method='GET')
    return response[0]['id']


async def get_photo():
    """Получение фото по ID домофона"""
    domofon_id = await get_domofon_id()
    data_domofon_foto = {
        "intercoms_id": [domofon_id],
        "media_type": ["JPEG"]
    }
    tenant_id = await get_id()
    url_for_photo = BASE_URL + f'/domo.domofon/urlsOnType?tenant_id={tenant_id}'
    response = await fetch_json(url=url_for_photo, headers=HEADERS, params=data_domofon_foto, method='POST')
    return response[0]['jpeg']


async def get_domofon_id():
    """
    Получение ID домофона
    :return:
    """
    tenant_id = await get_id()
    apartment_id = await get_float()
    url_for_domofon_id = BASE_URL + f'/domo.apartment/{apartment_id}/domofon?tenant_id={tenant_id}'
    response = await fetch_json(url=url_for_domofon_id, headers=HEADERS, method='GET')
    return response[0]['id']


async def open_the_door():
    tenant_id = await get_id()
    domofon_id = await get_domofon_id()
    data = {
      "door_id": 0
    }
    url = BASE_URL + f'/domo.domofon/{domofon_id}/open?tenant_id={tenant_id}'
    return await fetch_json(url=url, headers=HEADERS,params=data, method='POST')


if __name__ == '__main__':
    print(asyncio.run(get_photo()))
