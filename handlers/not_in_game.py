from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from database.models import Player
from game.game import GuessFilm
from fsm.states import FSMFillForm
from keyboards.reply_keyboards import create_reply_keyboard
from lexicon.lexicon_ru import LEXICON_RU


router = Router()
router.message.filter(StateFilter(default_state))


@router.message(CommandStart())
async def process_start_command(message: Message, game: GuessFilm):
    """Process the start command for the film guessing game.

    This function processes the start command from the user, sends a welcome
    message and information about the game, and creates a new player in
    the database.
    """
    
    keyboard = create_reply_keyboard('/play', '/stat')
    await message.answer(LEXICON_RU["/start"], reply_markup=keyboard)

    player = Player(_id=message.from_user.id)
    game.players_dao.create(player)


@router.message(Command(commands="play"))
async def process_play_command(message: Message, game: GuessFilm, state: FSMContext):
    """Process the play command for the film guessing game.

    This function starts a new round of the game. The function retrieves
    the next film from the game memory and sends it to the user for guessing.
    """

    film = game.play(message.from_user.id)

    await message.answer_photo(photo=film.get_image_file(), reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMFillForm.in_game_state)


@router.message(Command(commands="stat"))
async def process_stat_command(message: Message, game: GuessFilm):
    """Handles the stat command, which retrieves the statistics of the player.

    The statistics include:

        Score: the number of points the player has accumulated.
        Number of guessed films: the number of films that the player has
                                  successfully guessed.
    """
    player = game.get_player(message.from_user.id)
    guessed_films_num = len(player.guessed_films)

    await message.answer(
        f"Очки: {player.score}\n"
        f"Угаданных фильмов: {guessed_films_num}\n"
    )
