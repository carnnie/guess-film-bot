import json
import os
from typing import List, Tuple, Optional, Dict
from pymongo import ReplaceOne
from pymongo.database import Database

from config.config import FILMS_FILE_PATH
from database.models import Film, Player


class ObjectDoesNotExist(Exception):
    """Raises when a document is not exists in the database."""

    pass


class PlayerDao:
    """Class for data access of `Player` records from the Database.

    Properties:
        data_source: The Database object.
        collection_name: The name of the collection in the MongoDB to access
                         `Player` records.

    """

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

    def get(self, player_id: int) -> Player:
        player = self.data_source.find_one({'_id': player_id})

        if not player:
            raise ObjectDoesNotExist(f"Player with id {player_id} does not exist.")
        
        return Player(**player)

    def save_many(self, players: List[Player]) -> None:
        if not players:
            return

        update_objects = [
            ReplaceOne(
                {"_id": player._id},
                {
                    "current_film": player.current_film,
                    "guessed_films": player.guessed_films,
                    "attempts": player.attempts,
                    "score": player.score,
                },
                upsert=True,
            )
            for player in players
        ]

        self.data_source.bulk_write(update_objects)


class FilmDao:
    """Class for data access of `Film` records from the Database.

    Properties:
        data_source: The Database object.
        collection_name: The name of the collection in the MongoDB to access
                         `Film` records.

    """

    data_source: Database
    collection_name: str = "Films"

    def __init__(self, data_source: Database) -> None:
        self.data_source = data_source[self.collection_name]

    def all(self) -> List[Film]:
        """Retrieve all historical events from the database.

        Returns:
            A list of `HistoricalEvent` objects.

        """

        if not os.path.isfile(FILMS_FILE_PATH):
            raise FileNotFoundError(f"The file with films is missing by path: {FILMS_FILE_PATH}")

        try:
            with open(FILMS_FILE_PATH, "r") as json_file:
                films = json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError(
                msg=f"The films file ({FILMS_FILE_PATH}) has bad format (not valid JSON).",
                doc=e.doc,
                pos=e.pos,
            )

        return [Film(**film) for film in films]
