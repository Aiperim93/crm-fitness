import os
import aiohttp
from aiogram import types
from aiogram.dispatcher import Dispatcher
from tg_data import bot, logger, get_admin, API_TOKEN


async def massmailing(message: types.Message):
    admin = await get_admin()
    if message.from_user.id == admin:
        url = os.environ.get('MASS_MAILING_API')
        headers = {
            'Authorization': API_TOKEN
        }
        try:
            text = message.text.replace('/massmailing', '').strip()
            if not text:
                await bot.send_message(message.from_user.id, 'Сообщение не может быть пустым')
                return

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        users: list = await response.json()
                        for user in users:
                            if user['telegram_id']:
                                try:
                                    await bot.send_message(user['telegram_id'], text)
                                except Exception as e:
                                    error_message = f"Не удалось отправить сообщение пользователю {user['telegram_id']}. Ошибка: {e}"
                                    logger.exception(error_message)
                                    await bot.send_message(message.from_user.id, error_message)
                        await bot.send_message(message.from_user.id, 'Сообщение успешно отправлено')
                    else:
                        error_message = 'Ошибка при запросе к API'
                        logger.exception(error_message)
                        await bot.send_message(message.from_user.id, error_message)
                        raise ConnectionError(error_message)
        except (ValueError, ConnectionError) as err:
            logger.exception(err)
            await bot.send_message(message.from_user.id, f"Произошла ошибка: {err}")
        except Exception as e:
            logger.exception(e)
            await bot.send_message(message.from_user.id, 'Произошла ошибка при выполнении команды')
    else:
        await bot.send_message(message.from_user.id, f'Вы не являетесь администратором.')


async def sendallactiveclients(message: types.Message):
    admin = await get_admin()
    if message.from_user.id == admin:
        url = os.environ.get('SEND_ALL_ACTIVE_CLIENTS_API')
        headers = {
            'Authorization': API_TOKEN
        }

        try:
            text: str = message.text.replace('/sendallactiveclients', '').strip()
            if not text:
                await bot.send_message(message.from_user.id, 'Сообщение не может быть пустым')
                return
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        users: list = await response.json()
                        for user in users:
                            if user['telegram_id']:
                                try:
                                    await bot.send_message(user['telegram_id'], text)
                                except Exception as e:
                                    error_message = f"Не удалось отправить сообщение пользователю {user['telegram_id']}. Ошибка: {e}"
                                    logger.exception(error_message)
                                    await bot.send_message(message.from_user.id, error_message)
                        await bot.send_message(message.from_user.id, 'Сообщение успешно отправлено')
                    else:
                        error_message = 'Ошибка при запросе к API'
                        logger.exception(error_message)
                        await bot.send_message(message.from_user.id, error_message)
                        raise ConnectionError(error_message)
        except (ValueError, ConnectionError) as err:
            logger.exception(err)
            await bot.send_message(message.from_user.id, f"Произошла ошибка: {err}")
        except Exception as e:
            logger.exception(e)
            await bot.send_message(message.from_user.id, 'Произошла ошибка при выполнении команды')
    else:
        await bot.send_message(message.from_user.id, f'Вы не являетесь администратором.')


def register_handlers_mailing(dp: Dispatcher):
    dp.register_message_handler(sendallactiveclients, commands=['sendallactiveclients'])
    dp.register_message_handler(massmailing, commands=['massmailing'])
