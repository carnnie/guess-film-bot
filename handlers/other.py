from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command(commands=["start", "help", "stat"]))
async def warning_not_in_game_commands(message: Message):
    await message.answer("Данная команда доступна только вне игры. Мы сейчас играем. Хотите выйти?")


@router.message(Command(commands=["surrender", "cancel"]))
async def warning_in_game_commands(message: Message):
    await message.answer(
        "Данная команда доступна только в игре. Мы сейчас с вами не играем. Хотите сыграть?"
    )


@router.message()
async def process_other_text_answers(message: Message):
    await message.answer("Я играю только по правилам, введите /help, чтобы узнать правила.")
