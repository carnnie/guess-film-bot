from aiogram.fsm.state import State, StatesGroup

class FSMFillForm(StatesGroup):
    in_game_state = State()
