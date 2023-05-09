import io
import os
import re
import aiohttp
from aiogram import types
from aiogram.types import PhotoSize, Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher, FSMContext
from keyboards import add_data_kb, cancel_keyboard, admin_kb
from tg_data import logger, API_TOKEN, get_admin
from fsm import AddDataStates

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')


async def register_user(message: types.Message):
    user_id: str = str(message.from_user.id)
    url: str = f"{os.environ.get('CLIENT_CHECK_API')}{user_id}"
    headers = {
        'Authorization': API_TOKEN
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    result: str = (await response.json())['result']
                    if result == 'client':
                        await message.answer('Вы уже зарегистрированы как клиент', reply_markup=add_data_kb)
                    elif result == 'client_deleted':
                        await message.answer('К сожалению, вы не можете зарегистрироваться, так как ваша учетная '
                                             'запись была удалена администратором. Пожалуйста, обратитесь к '
                                             'администратору для получения дополнительной информации и помощи. '
                                             'Спасибо за понимание.')
                    elif result == 'coach':
                        await message.answer('Вы уже зарегистрированы как тренер')
                elif response.status == 404:
                    data: dict = {'telegram_id': user_id}
                    async with session.post(os.environ.get('CLIENT_CREATE_API'), data=data) as response:
                        if response.status == 201:
                            await message.answer('Вы успешно зарегистрированы как клиент', reply_markup=add_data_kb)

                        else:
                            await message.answer('Произошла ошибка при регистрации')
                else:
                    await message.answer('Произошла ошибка при проверке наличия пользователя в базе данных')
                    raise Exception('Произошла ошибка при проверке наличия пользователя в базе данных')
        except aiohttp.ClientResponseError as e:
            await message.answer(f'Произошла ошибка при выполнении запроса: {e.status}')
        except aiohttp.ClientError as e:
            await message.answer(f'Произошла ошибка сети: {e}')
            logger.exception(e)


def register_handlers_clients(dp: Dispatcher):
    dp.register_message_handler(register_user, Text('Регистрация'))


async def start_add_data(message: Message):
    user_id: str = str(message.from_user.id)
    url: str = f"{os.environ.get('CLIENT_CHECK_API')}{user_id}"
    headers = {
        'Authorization': API_TOKEN
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                await message.answer('Введите ваше имя:')
                await message.answer(text='Для отмены нажмите кнопку Отменить',
                                     reply_markup=cancel_keyboard)
                await AddDataStates.first_name.set()
            else:
                await message.answer('К сожалению, вы не можете добавить данные, так как ваша учетная '
                                     'запись еще не создана. Пожалуйста пройдите регистрацию')


async def cancel_add_data(message: Message, state: FSMContext):
    if message.from_user.id == await get_admin():
        await message.answer('Вы отменили добавление данных', reply_markup=admin_kb)
        await state.finish()
    else:
        await message.answer('Вы отменили добавление данных', reply_markup=add_data_kb)
        await state.finish()


async def add_first_name(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await cancel_add_data(message, state)
        return

    first_name = message.text
    if not first_name.isalpha():
        await message.answer(
            'Некорректное имя. Имя должно состоять только из букв. Пожалуйста, введите корректное имя:')
        return
    async with state.proxy() as data:
        data['first_name'] = first_name
    await message.answer('Введите вашу фамилию:')
    await message.answer(text='Для отмены нажмите кнопку Отменить',
                         reply_markup=cancel_keyboard)
    await AddDataStates.last_name.set()


async def add_last_name(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await cancel_add_data(message, state)
        return

    last_name = message.text
    if not last_name.isalpha():
        await message.answer(
            'Некорректная фамилия. Фамилия должна состоять только из букв. Пожалуйста, введите корректную фамилию:')
        return
    async with state.proxy() as data:
        data['last_name'] = last_name
    await message.answer('Введите вашу почту:')
    await message.answer(text='Для отмены нажмите кнопку Отменить',
                         reply_markup=cancel_keyboard)
    await AddDataStates.email.set()


async def add_email(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await cancel_add_data(message, state)
        return

    email = message.text
    if not EMAIL_REGEX.match(email):
        await message.answer('Некорректный email. Пожалуйста, введите корректный email:')
        return
    async with state.proxy() as data:
        data['email'] = email
    await message.answer('Введите ваш номер телефона:')
    await message.answer(text='Для отмены нажмите кнопку Отменить',
                         reply_markup=cancel_keyboard)
    await AddDataStates.phone.set()


async def add_phone(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await cancel_add_data(message, state)
        return

    phone = message.text
    if not PHONE_REGEX.match(phone):
        await message.answer('Некорректный номер телефона. Пожалуйста, введите номер телефона в формате: +999999999:')
        return
    async with state.proxy() as data:
        data['phone'] = phone
    await message.answer('Введите ваш регион:')
    await message.answer(text='Для отмены нажмите кнопку Отменить',
                         reply_markup=cancel_keyboard)
    await AddDataStates.region.set()


async def add_region(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await cancel_add_data(message, state)
        return

    async with state.proxy() as data:
        data['region'] = message.text
    await message.answer('Отправьте ваше фото:')
    await message.answer(text='Для отмены нажмите кнопку Отменить',
                         reply_markup=cancel_keyboard)
    await AddDataStates.photo.set()


async def add_photo(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await cancel_add_data(message, state)
        return

    async with state.proxy() as data:
        photo: PhotoSize = message.photo[-1]
        file = io.BytesIO()
        await photo.download(file)
        file.seek(0)

    await state.finish()

    headers: dict = {
        'Authorization': API_TOKEN
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        url: str = f"{os.environ.get('CLIENT_UPDATE_API')}{message.from_user.id}/"

        form = aiohttp.FormData()
        form.add_field('first_name', data['first_name'])
        form.add_field('last_name', data['last_name'])
        form.add_field('email', data['email'])
        form.add_field('phone', data['phone'])
        form.add_field('region', data['region'])
        form.add_field("photo", file.getbuffer(), filename="client_photo.jpg")

        async with session.patch(url, data=form) as response:
            if response.status == 200:
                await message.answer('Данные успешно обновлены!')
            else:
                await message.answer(f'Ошибка: {response.status} Текст:{response.text}')


def add_data_handlers_clients(dp: Dispatcher):
    dp.register_message_handler(start_add_data, Text('Добавить данные'))
    dp.register_message_handler(cancel_add_data, Text('Отменить'), state='*')
    dp.register_message_handler(add_first_name, state=AddDataStates.first_name)
    dp.register_message_handler(add_last_name, state=AddDataStates.last_name)
    dp.register_message_handler(add_email, state=AddDataStates.email)
    dp.register_message_handler(add_phone, state=AddDataStates.phone)
    dp.register_message_handler(add_region, state=AddDataStates.region)
    dp.register_message_handler(add_photo, content_types=['photo'], state=AddDataStates.photo)
