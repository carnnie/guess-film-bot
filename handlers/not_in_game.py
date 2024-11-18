from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from database.models import Player
from game.game import GuessFilm
from fsm.states import in_game_state


router = Router()
router.message.filter(StateFilter(default_state))


@router.message(CommandStart())
async def process_start_command(message: Message, game: GuessFilm):
    """Process the start command for the film guessing game.

    This function processes the start command from the user, sends a welcome
    message and information about the game, and creates a new player in
    the database.
    """

    await message.answer(
        'Привет!\nДавай сыграем в игру "Угадай фильм по кадру"?\n\n'
        "Чтобы получить правила игры и список доступных "
        "команд - отправьте команду /help"
    )

    player = Player(_id=message.from_user.id)
    game.players_dao.create(player)


@router.message(Command(commands="play"))
async def process_play_command(message: Message, game: GuessFilm, state: FSMContext):
    """Process the play command for the film guessing game.

    This function starts a new round of the game. The function retrieves
    the next film from the game memory and sends it to the user for guessing.
    """

    film = game.play(message.from_user.id)
    await message.answer_photo(photo=film.get_image_file())
    await state.set_state(in_game_state)


@router.message(Command(commands="stat"))
async def process_stat_command(message: Message, game: GuessFilm):
    player = game.get_player(message.from_user.id)
    guessed_films_num = len(player.guessed_films)

    try:
        attempts_average = round(player.attempts / guessed_films_num)
    except ZeroDivisionError:
        attempts_average = 0

    await message.answer(
        f"Очки: {player.score}\n"
        f"Общее число попыток: {player.attempts}\n"
        f"Угаданных фильмов: {guessed_films_num}\n"
        f"Среднее кол-во попыток на ответ: {attempts_average}"
    )
