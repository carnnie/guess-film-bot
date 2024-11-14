from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from pymongo.database import Database

from src.config import BOT_TOKEN
from src.dao import PlayerDao
from src.database import get_database
from src.game import GuessFilm
from src.models import Player


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
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
    players.create(player)


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    """Sends game rules and a list of commands."""

    await message.answer(
        "Правила игры:\n\nЯ присылаю кадр из фильма, "
        "а вам нужно назвать его название.\n\n"
        "Пример ответа: Форрест Гамп\n\n"
        "Доступные команды:\n"
        "/play - начать играть\n"
        "/sur - сдаться\n"
        "/cancel - отменить игру\n"
        "/stat - посмотреть статистику\n"
        "/help - правила игры и список команд\n\nДавай сыграем?"
    )

@dp.message(Command(commands='play'))
async def process_play_command(message: Message):
    pass


if __name__ == "__main__":
    database: Database = get_database()
    players: PlayerDao = PlayerDao(database)
    with GuessFilm(database) as game:
        dp.run_polling(bot)
