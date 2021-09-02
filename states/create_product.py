from aiogram.dispatcher.filters import state


class Product(state.StatesGroup):
    P1 = state.State()
    P2 = state.State()
    P3 = state.State()
    P4 = state.State()
