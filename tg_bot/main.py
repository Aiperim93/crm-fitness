from aiogram.utils import executor
from tg_data import dp, register_handlers_start
from invite_logic import register_handlers_invite
from client_logic import register_handlers_clients
from mailing_logic import register_handlers_mailing
from client_logic import add_data_handlers_clients


register_handlers_start(dp)
register_handlers_invite(dp)
register_handlers_clients(dp)
register_handlers_mailing(dp)
add_data_handlers_clients(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

