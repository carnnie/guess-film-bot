import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import State
from aiogram.fsm.storage.memory import MemoryStorage
from pymongo.database import Database

from config.config import BOT_TOKEN
from database.dao import PlayerDao
from database.database import get_database
from game.game import GuessFilm
from handlers import in_game, not_in_game, other
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info('Starting bot')

    storage = MemoryStorage()

    bot: Bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher(storage=storage)

    database: Database = get_database()
    game: GuessFilm = GuessFilm(database)

    dp.workflow_data.update({'game': game})

    dp.include_router(in_game.router)
    dp.include_router(not_in_game.router)
    dp.include_router(other.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    await game.players_dao.save_many(game.players.values())

if __name__ == "__main__":
    asyncio.run(main())
