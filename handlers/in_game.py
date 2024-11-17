from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message

from game.game import GuessFilm
from fsm.states import in_game_state
from lexicon.lexicon_ru import LEXICON_RU


router = Router()
router.message.filter(StateFilter(in_game_state))


@router.message(Command(commands="surrender"))
async def process_surrender_command(message: Message, game: GuessFilm, state: FSMContext):
    """Process the surrender command for the film guessing game.

    This function processes the surrender command from the user during a round
    of the game. If the user is currently in a game, the function retrieves
    the correct film from the game memory, sends it to the user,
    and updates the user's statistics in the database.
    """

    player = game.get_player(message.from_user.id)

    film = game.surrender(player)
    await message.answer(film.explain())
    await state.clear()


@router.message(Command(commands="cancel"))
async def process_cancel_command(message: Message, game: GuessFilm, state: FSMContext):
    """Process the cancel command for the film guessing game.

    This function processes the cancel command from the user during a round of
    the game. If the user is currently in a game, the function cancels the
    current game and sends a message to the user indicating that the user
    have left the game.
    """

    player = game.get_player(message.from_user.id)

    game.cancel(player)
    await message.answer("Вы вышли из игры. Если захотите сыграть снова - напишите об этом. /play")
    await state.clear()


@router.message(F.text)
async def process_film_answer(message: Message, game: GuessFilm, state: FSMContext):
    """Process a user's answer to a film in the current game.

    Validates an answer. Gets a result from the game and sends a result message
    to the user. The result message has either gussed film infomation or
    hints for guessing.
    """

    answer = message.text
    player = game.get_player(message.from_user.id)

    msg, film = game.guess(player, answer)

    if film:
        await message.answer(LEXICON_RU[msg])
        await message.answer(film.explain())
        await state.clear()
    else:
        await message.answer(msg)
