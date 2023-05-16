from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Регистрация')
kb.add(button1)

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button2 = KeyboardButton(text='Начать занятие')
button4 = KeyboardButton(text='Отправить рассылку')
admin_kb.add(button2)
admin_kb.add(button4)


add_data_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Добавить данные')
add_data_kb.add(button3)

cancel_button = KeyboardButton('Отменить')
cancel_keyboard = ReplyKeyboardMarkup([[cancel_button]], resize_keyboard=True)

def get_group_kb(groups):
    group_kb = InlineKeyboardMarkup(row_width=1)
    for group in groups:
        group_kb.add(InlineKeyboardButton(group['name'], callback_data=f"group_{group['id']}"))
    return group_kb


def get_coach_kb(coaches):
    coach_kb = InlineKeyboardMarkup(row_width=1)
    for coach_type, coaches_list in coaches.items():
        if coach_type == "base_coach" and coaches_list:
            first_name = coaches_list["first_name"]
            last_name = coaches_list["last_name"] or ""
            text = f"{first_name} {last_name}"
            callback_data = f'coach_id_{coaches_list["id"]}'
            button = InlineKeyboardButton(text, callback_data=callback_data)
            coach_kb.add(button)
        elif coach_type == "other_coaches" and coaches_list:
            for coach in coaches_list:
                first_name = coach["first_name"]
                last_name = coach["last_name"] or ""
                text = f"{first_name} {last_name}"
                callback_data = f'coach_id_{coach["id"]}'
                button = InlineKeyboardButton(text, callback_data=callback_data)
                coach_kb.add(button)
    return coach_kb


def get_cancel_kb():
    cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_kb.add(KeyboardButton('Отмена'))
    return cancel_kb


def invite_button(telegram_id: str) -> InlineKeyboardMarkup:
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    expiration_text = expiration_time.strftime('%Y-%m-%d %H:%M:%S')
    button = InlineKeyboardButton(
        text="Присоединиться к тренировке",
        callback_data=f"invite_{telegram_id}_{expiration_text}"
    )
    markup = InlineKeyboardMarkup()
    markup.add(button)
    return markup
