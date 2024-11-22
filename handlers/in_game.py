from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from game.game import GuessFilm
from fsm.states import FSMFillForm
from keyboards.reply_keyboards import create_reply_keyboard
from lexicon.lexicon_ru import LEXICON_RU


router = Router()
router.message.filter(StateFilter(FSMFillForm.in_game_state))


@router.message(Command(commands="surrender"))
async def process_surrender_command(message: Message, game: GuessFilm, state: FSMContext):
    """Process the surrender command for the film guessing game.

    This function processes the surrender command from the user during a round
    of the game. If the user is currently in a game, the function retrieves
    the correct film from the game memory, sends it to the user,
    and updates the user's statistics in the database.
    """

    player = game.get_player(message.from_user.id)
    keyboard = create_reply_keyboard("/play", "/stat")

    film = game.surrender(player)
    await message.answer(film.explain(), reply_markup=keyboard)
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
    keyboard = create_reply_keyboard("/play", "/stat")

    game.cancel(player)
    await message.answer(
        LEXICON_RU["/cancel"],
        reply_markup=keyboard,
    )
    await state.clear()


@router.message(~Command(commands=["start", "stat", "play", "help"]))
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
        await message.answer(film.explain(), reply_markup=create_reply_keyboard("/play", "/stat"))
        await state.clear()
    else:
        await message.answer(msg)
