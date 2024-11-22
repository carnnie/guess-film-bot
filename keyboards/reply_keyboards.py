from aiogram.types import InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_reply_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    """Creates reply keyboard using the passed args.

    Args:
        buttons: Names of buttons.

    Returns:
        Keyboard with buttons passed.
    """
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(*[KeyboardButton(text=button) for button in buttons])

    return kb_builder.as_markup(resize_keyboard=True)
