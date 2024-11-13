from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from pymongo.database import Database

from src.config import BOT_TOKEN
from src.dao import PlayerDao
from src.database import get_database
from src.models import Player


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавай сыграем в игру "Угадай фильм по кадру"?\n\n'
        "Чтобы получить правила игры и список доступных "
        "команд - отправьте команду /help"
    )

    player = Player(_id=message.from_user.id)
    players.create(player)


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        "Правила игры:\n\nЯ называю вам историческое событие, "
        "а вам нужно назвать в каком году оно произошло.\n\n"
        "Пример ответа: 1998\n\n"
        "Доступные команды:\n"
        "/play - начать играть\n"
        "/sur - сдаться\n"
        "/cancel - отменить игру\n"
        "/stat - посмотреть статистику\n"
        "/help - правила игры и список команд\n\nДавай сыграем?"
    )


if __name__ == "__main__":
    database: Database = get_database()
    players: PlayerDao = PlayerDao(database)
    dp.run_polling(bot)
