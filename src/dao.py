from typing import Tuple, Optional, Dict
from pymongo.database import Database

from src.models import Player


class ObjectDoesNotExist(Exception):
    """Raises when a document is not exists in the database."""

    pass


class PlayerDao:
    data_source: Database
    collection_name: str = "Players"

    def __init__(self, data_source: Database) -> None:
        self.data_source = data_source[self.collection_name]

    def create(self, player: Player) -> Tuple[Player, bool]:
        player_db: Optional[Dict] = self.data_source.find_one({"_id": player._id})
        created = player_db is None

        if player_db:
            player = Player(**player_db)
        else:
            self.data_source.insert_one(
                {
                    "_id": player._id,
                    "current_film": player.current_film,
                    "guessed_films": player.guessed_films,
                    "attempts": player.attempts,
                    "score": player.score,
                }
            )
        return player, created
