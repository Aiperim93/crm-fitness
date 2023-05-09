from aiogram.dispatcher.filters.state import State, StatesGroup


class StartTrainingState(StatesGroup):
    group = State()
    link = State()
    send_invite = State()
    coach = State()


class AddDataStates(StatesGroup):
    first_name: State = State()
    last_name: State = State()
    email: State = State()
    phone: State = State()
    region: State = State()
    photo: State = State()
