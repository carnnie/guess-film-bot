from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.reply_keyboards import create_reply_keyboard
from lexicon.lexicon_ru import LEXICON_RU


router = Router()


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    """Sends game rules and a list of commands."""

    await message.answer(LEXICON_RU["/help"])


@router.message(Command(commands=["surrender", "cancel"]))
async def warning_in_game_commands(message: Message):
    """Handler that triggers if user sends in-game command not in game"""

    await message.answer(LEXICON_RU["in_game_command"])


@router.message(Command(commands=["start", "stat", "play"]))
async def warning_not_in_game_commands(message: Message):
    """Handler that triggers if user sends not-in-game command in game"""

    keyboard = create_reply_keyboard("/cancel")
    await message.answer(LEXICON_RU["not_in_game_command"], reply_markup=keyboard)


@router.message()
async def process_other_text_answers(message: Message):
    """Handler that triggers if user sends any unexpected message"""

    await message.answer(LEXICON_RU["other"])
