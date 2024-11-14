from typing import Dict

from src.dao import FilmDao, PlayerDao
from src.models import Film, Player


class GuessFilm:
    """Implementation of a guess film game.

    Properties:
        films: A dictionary mapping from film id to `Film` instance.
        players_dao: An instance of `PlayerDao` for accessing the player data
                     in the database.
        players: A dictionary mapping from player id to `Player` instance;
                 stores cached players.

    """

    films: Dict[int, Film]
    players: Dict[int, Player]
    players_dao: PlayerDao

    def __init__(self, database):
        films_dao = FilmDao(database)
        self.films = {film._id: film for film in films_dao.all()}

        if not self.films:
            raise ValueError("Can't start game without films.")

        self.players_dao = PlayerDao(database)
        self.players = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """Saves all cached players to the database on exit."""
        self.players_dao.save_many(self.players.values())
