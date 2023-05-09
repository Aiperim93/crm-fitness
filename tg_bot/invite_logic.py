from typing import List
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from keyboards import get_group_kb, invite_button, get_coach_kb, get_cancel_kb
from validators import is_valid_link
import datetime
from aiogram import exceptions as aiogram_exceptions
from fsm import StartTrainingState
from tg_data import *


async def get_groups():
    url: str = f"{os.environ.get('GET_GROUP_LIST_API')}"
    headers = {
        'Authorization': API_TOKEN
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                groups = await response.json()
                return groups


async def get_active_clients_in_group(group_id):
    url: str = f"{os.environ.get('GET_CLIENTS_IN_GROUP_API')}{group_id}/?active=True"
    headers = {
        'Authorization': API_TOKEN
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                clients = (await response.json())
                return clients


async def link_invalid(message: types.Message, state: FSMContext):
    if message.text.lower().replace('/', '') == 'cancel':
        await state.finish()
        await message.reply('Операция отменена.')
        return
    return await message.reply("Некорректная ссылка, попробуйте еще раз.")


async def get_link(message: types.Message, state: FSMContext):
    link: str = message.text
    await state.update_data(link=link)
    redis_.set('google_link', link)
    await create_group_training(state)

    if message.from_user.id == await get_admin():
        await message.answer(text='Приглашения успешно отправлены!', reply_markup=admin_kb)
        data = await state.get_data()
        group_id = data['group']
        clients = await get_active_clients_in_group(group_id)
        client_list = []
        for client in clients:
            client_list.append(client['telegram_id'])
        await StartTrainingState.send_invite.set()
        await send_invite_buttons_to_clients(client_list, state)


async def get_coach_list_by_group(group_id):
    url: str = f"{os.environ.get('GET_COACH_LIST_API')}{group_id}/"
    headers = {'Authorization': API_TOKEN}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                coaches = await response.json()
                return coaches


async def create_group_training(state: FSMContext):
    url: str = os.environ.get('GROUP_TRAINING_CREATE_API')
    headers = {'Authorization': API_TOKEN}
    data = await state.get_data()
    group_id = data['group']
    coach_id = data['coach']

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data={'coach': coach_id, 'group': group_id}) as response:
            if response.status == 201:
                return


async def invite_callback(callback_query: CallbackQuery):
    user_id: int = callback_query.from_user.id
    url: str = os.environ.get('TRAINING_CREATE_API')
    headers = {'Authorization': API_TOKEN}
    data: dict = {'telegram_id': user_id}
    callback_data = callback_query.data.split('_')
    telegram_id = callback_data[1]
    expiration_text = callback_data[2]
    expiration_time = datetime.datetime.strptime(expiration_text, '%Y-%m-%d %H:%M:%S')
    if datetime.datetime.now() < expiration_time:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, data=data) as response:
                    if response.status == 201:
                        await bot.send_message(callback_query.from_user.id, text='Тренировка создана!')
                        django_link = redis_.get('google_link').decode('utf-8')
                        await bot.send_message(callback_query.from_user.id, text=f'Ссылка на занятие: {django_link}')
                        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                                            message_id=callback_query.message.message_id,
                                                            reply_markup=None)
                    else:
                        await bot.send_message(callback_query.from_user.id, text='Не удалось создать тренировку!')
        except aiohttp.ClientError as e:
            logger.exception(e)
            await bot.send_message(callback_query.from_user.id, text=f'Ошибка: {str(e)}')
        except Exception as e:
            logger.exception(e)
            await bot.send_message(callback_query.from_user.id, text=f"Error sending invite to {telegram_id}: {e}")
    else:
        await bot.answer_callback_query(callback_query.id, text="Приглашение не активно!")
    await bot.answer_callback_query(callback_query.id)


async def send_invite_buttons_to_clients(clients: List, state: FSMContext):
    await state.update_data(send_invite=True)
    for client in clients:
        invite_markup = invite_button(client)
        try:
            if redis_.get('google_link'):
                await bot.send_message(client, text='Приглашение на тренировку:', reply_markup=invite_markup)
        except aiogram_exceptions.BotBlocked as e:
            logger.exception(f"Ошибка отправки приглашения: {e}")
        except aiogram_exceptions.TelegramAPIError as e:
            logger.exception(f"Ошибка отправки приглашения: {e}")
        await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    if message.from_user.id == await get_admin():
        await message.reply('Операция отменена.', reply_markup=admin_kb)


async def coach_callback(callback_query: CallbackQuery, state: FSMContext):
    coach_id: int = int(callback_query.data.replace('coach_id_', ''))
    await state.update_data(coach=coach_id)
    data = await state.get_data()
    group_id = data['group']

    clients = await get_active_clients_in_group(group_id)
    if clients:
        await bot.send_message(text="Введите ссылку на занятие:", chat_id=await get_admin())
        await StartTrainingState.link.set()
    else:
        await bot.send_message(callback_query.from_user.id, text='В этой группе нет активных клиентов!')
        await StartTrainingState.group.set()
    await bot.answer_callback_query(callback_query.id)


async def group_callback(callback_query: CallbackQuery, state: FSMContext):
    group_id: int = int(callback_query.data.replace('group_', ''))
    await state.update_data(group=group_id)

    coaches = await get_coach_list_by_group(group_id)
    if coaches:
        coaches_list_kb = get_coach_kb(coaches)
        await bot.send_message(text='Выберите, пожалуйста, тренера:', chat_id=await get_admin(),
                             reply_markup=coaches_list_kb)
    await StartTrainingState.coach.set()
    await bot.answer_callback_query(callback_query.id)


async def start_training(message: types.Message):
    try:
        groups = await get_groups()
        if groups:
            group_list_kb = get_group_kb(groups)

            await message.answer(text='Выберите, пожалуйста, группу:',
                                 reply_markup=group_list_kb)
            await message.answer(text='Для отмены нажмите кнопку Отмена',
                                 reply_markup=get_cancel_kb())

            await StartTrainingState.group.set()
        else:
            await message.answer('Произошла ошибка при подключении к серверу!')
            raise ConnectionError("Произошла ошибка при подключении к серверу!")
    except ConnectionError as conn_err:
        logger.exception(conn_err)
        await message.answer('Ошибка подключения к серверу!')
    except Exception as e:
        logger.exception(e)
        await message.answer('Произошла ошибка при выполнении команды!')


def register_handlers_invite(dp: Dispatcher):
    dp.register_message_handler(link_invalid, lambda message: not is_valid_link(message.text),
                                state=StartTrainingState.link)
    dp.register_message_handler(get_link, state=StartTrainingState.link)
    dp.register_message_handler(send_invite_buttons_to_clients, state=StartTrainingState.send_invite)
    dp.register_callback_query_handler(invite_callback, lambda c: c.data.startswith('invite_'))
    dp.register_callback_query_handler(group_callback, lambda c: c.data.startswith('group_'), state=StartTrainingState.group)
    dp.register_callback_query_handler(coach_callback, lambda c: c.data.startswith('coach_id'), state=StartTrainingState.coach)
    dp.register_message_handler(cancel_handler, commands=['cancel'], state='*')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_training, Text('Начать занятие'))
