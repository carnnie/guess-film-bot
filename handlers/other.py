from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command(commands="help"))
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


@router.message(Command(commands=["start", "stat"]))
async def warning_not_in_game_commands(message: Message):
    await message.answer("Данная команда доступна только вне игры. Мы сейчас играем. Хотите выйти?")


@router.message(Command(commands=["surrender", "cancel"]))
async def warning_in_game_commands(message: Message):
    await message.answer("Данная команда доступна только в игре. Мы сейчас с вами не играем. Хотите сыграть?")


@router.message()
async def process_other_text_answers(message: Message):
    await message.answer("Я играю только по правилам, введите /help, чтобы узнать правила.")
