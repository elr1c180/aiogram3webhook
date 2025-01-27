from urllib import parse
from aiogram import Router, types
import aiogram.exceptions
from asgiref.sync import sync_to_async
from config import BASE_DIR
import django
import os
import decimal
from core.models import Themes
from urllib.parse import parse_qs, urlparse
import hashlib
import sys

sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chim_admin.settings')
django.setup()

router = Router()

payment_data = {}

async def handle_payment_result(request):
    params = parse_response(request.url)
    try:
        cost = decimal.Decimal(params['OutSum'])
        order_number = int(params['InvId'])
        received_signature = params['SignatureValue']
    except KeyError:
        return "Invalid parameters"

    if check_signature(order_number, cost, received_signature, 'mZjg8Qw9G9DCJXZEu71J'):
        # здесь можно отправить сообщение пользователю, что оплата прошла успешно
        return f"OK{params['InvId']}"
    return "bad sign"

async def handle_payment_success(request):
    params = parse_response(request.url)
    try:
        cost = decimal.Decimal(params['OutSum'])
        order_number = int(params['InvId'])
        received_signature = params['SignatureValue']
    except KeyError:
        return "Invalid parameters"

    if check_signature(order_number, cost, received_signature, 'mZjg8Qw9G9DCJXZEu71J'):
        # здесь можно отправить сообщение пользователю, что оплата прошла успешно
        return "Thank you for using our service"
    return "bad sign"

def parse_response(request: str) -> dict:
    """Парсим параметры из URL-строки"""
    params = {}
    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params

def check_signature(order_number: int, received_sum: decimal, received_signature: str, password: str) -> bool:
    """Проверка сигнатуры"""
    signature = calculate_signature(received_sum, order_number, password)
    return signature.lower() == received_signature.lower()

def calculate_signature(*args) -> str:
    """Вычисление MD5-сигнатуры"""
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

@sync_to_async
def get_course_by_id(course_id: int):
    try:
        return Themes.objects.get(id=course_id)
    except Themes.DoesNotExist:
        return None

def generate_payment_link(merchant_login: str, merchant_password_1: str, cost: decimal, number: int, description: str,user_id: str,  is_test=1 ,robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx') -> str:
    """Генерация ссылки для Robokassa"""
    signature = calculate_signature(merchant_login, str(cost), str(number), merchant_password_1)
    data = {
        'MerchantLogin': merchant_login,
        'OutSum': str(cost),
        'InvId': str(number),
        'Description': description,
        'SignatureValue': signature,
        'IsTest': str(is_test),
        'user_id': user_id
    }
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'

@router.callback_query(lambda c: c.data.startswith('buy_'))
async def reviews_router(callback: types.CallbackQuery):
    await callback.message.delete()

    course_id = int(callback.data.split('_')[1])
    current_course = await get_course_by_id(course_id)
    inv_id = course_id

    payment_data[callback.message.chat.id] = inv_id
    print(payment_data)

    if not current_course:
        await callback.message.answer("Курс не найден.")
        return

    try:
        first_group = await callback.bot.get_chat_member(chat_id='-1002250903191', user_id=callback.message.chat.id)
        second_group = await callback.bot.get_chat_member(chat_id='-1002296031461', user_id=callback.message.chat.id)
        third_group = await callback.bot.get_chat_member(chat_id='-1002323253166', user_id=callback.message.chat.id)
    except aiogram.exceptions.TelegramBadRequest as e:
        await callback.message.answer(f"Ошибка доступа к чату: {str(e)}")
        return

    print(dict(first_group)['status'])
    print(dict(second_group)['status'])
    print(dict(third_group)['status'])

    if dict(first_group)['status'] != 'left' or (dict(second_group)['status'] != 'left' and dict(third_group)['status'] != 'left'):
        payment_link = generate_payment_link(
            merchant_login="chem_rsmu_bot",
            merchant_password_1="mZjg8Qw9G9DCJXZEu71J",
            cost=decimal.Decimal(current_course.price),
            number=str(course_id),
            description=current_course.description,
            user_id = str(callback.message.chat.id),
        )
        await callback.message.answer(f'Для получения доступа к курсу вам необходимо произвести <a href="{payment_link}">оплату</a>', parse_mode='html')
    else:
        await callback.message.answer('Для получения доступа к материалам необходима консультация автора. Для оплаты свяжитесь с @Dmn_lc')

def result_payment(merchant_password_2: str, request: str) -> str:
    """Обработка результата платежа"""
    param_request = parse_response(request)
    cost = decimal.Decimal(param_request['OutSum'])
    number = int(param_request['InvId'])
    signature = param_request['SignatureValue']

    if check_signature(number, cost, signature, merchant_password_2):
        return f'OK{param_request["InvId"]}'
    return "bad sign"

def check_success_payment(merchant_password_1: str, request: str) -> str:
    """Проверка успешности платежа"""
    param_request = parse_response(request)
    cost = decimal.Decimal(param_request['OutSum'])
    number = int(param_request['InvId'])
    signature = param_request['SignatureValue']

    if check_signature(number, cost, signature, merchant_password_1):
        return "Thank you for using our service"
    return "bad sign"
