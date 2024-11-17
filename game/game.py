from typing import Dict, Optional, Tuple

from config.config import NUMBER_OF_ATTEMPTS
from database.dao import FilmDao, ObjectDoesNotExist, PlayerDao
from database.models import Film, Player


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

    # def __enter__(self):
    #     return self

    # def __exit__(self, exc_type, exc_value, tb):
    #     """Saves all cached players to the database on exit."""
    #     self.players_dao.save_many(self.players.values())

    def get_player(self, player_id: int) -> Player:
        """Gets a player by id from the cache if exists othervise from DB.

        Retrives a player for the cache if it exists othervise from
        the database and saves the player to the cache.

        Args:
            player_id: Player's unique identifier to retrieve.

        Returns:
            The player instance with given id.
        """
        if player := self.players.get(player_id):
            return player

        try:
            player = self.players_dao.get(player_id)
        except ObjectDoesNotExist:
            player, _ = self.players_dao.create(Player(_id=player_id))

        self.players[player._id] = player
        return player

    def _get_film_for_player(self, player: Player) -> Film:
        """Returns a not guessed film for a specifiec player.

        If all films guessed resets player's guessed films and starts over.

        Args:
            player: A player instance for picking next film.

        Returns:
            A next film for guessing.
        """

        for film in self.films.values():
            if film._id not in player.guessed_films:
                return film

        player.guessed_films = []
        return self._get_film_for_player(player)

    def _get_hint(film: Film, attempts_left: int) -> str:
        """Returns a hint for guessing film depending on number of attempts.

        If there are more then enough attempts it doesn't return a hint.

        Args:
            film: A Film instance to take info for hint.

        Returns:
            String that contains hint.
        """
        ratio = attempts_left / NUMBER_OF_ATTEMPTS
        if ratio < 0.7:
            return f'Неверно. Подсказка: жанр фильма - {film.genre}'
        elif ratio < 0.4:
            return f'Ты не угадал. Подсказка: год выхода фильма - {film.year}'
        else:
            return f'Неверно.'

    def _validate_answer(answer: str, film: Film):
        """Validates player's answer by comparison with name of current film.

        Args:
            answer: Player's answer.
            film: A Film instance to compare.

        Returns:
            Boolean representing the result of validating.
        """
        return film.name.lower().strip() == answer.lower().strip()

    def play(self, player_id: int) -> Film:
        """Starts a new game round for a given player.

        Retrieves the `Player` instance, sets the `current_film` for
        the player, reset attempts and returns the `current_film`.

        Args:
            player_id: Player's unique ID to start a new game round with.

        Returns:
            A next film for guessing.
        """
        player = self.get_player(player_id)
        film = self._get_film_for_player(player)
        player.current_film = film._id
        player.attempts = NUMBER_OF_ATTEMPTS
        self.players[player._id] = player
        return film

    def guess(self, player: Player, answer: str) -> Tuple[str, Optional[Film]]:
        """Processes a player's guess.

        Given a `Player` instance and a player's guess (`film`).
        Check the player's attempts, and returns a message indicating
        whether the guess was correct and the corresponding `Film`
        instance if the guess was correct or attempts are over.

        Args:
            player: A player instance that trying to guess.
            answer: A player's guess.

        Returns:
            Tuple - message (a hint for guessing or lose/win result),
                    the film if guessed or attempts are over, `None` othervise.
        """
        film = self.films[player.current_film]
        player.attempts -= 1

        if player.attempts < 0:
            return "lose", self.surrender(player)
        else:
            if self._validate_answer(answer, film):
                player.guessed_films.append(player.current_film)
                player.current_film = None
                player.score += 5 + player.attempts * 2
                self.players[player._id] = player
                return "win", film
            else:
                self.players[player._id] = player
                return self._get_hint(film, player.attempts), None

    def surrender(self, player: Player) -> Film:
        """Ends a game round and returns the hidden film.

        Given a `Player` instance, updates the player's score, sets the
        `current_film` for the player to `None`, and returns the
        `current_film`.

        Args:
            player: A surrendered player.

        Returns:
            The hidden film.
        """

        film = self.films[player.current_film]
        player.current_film = None
        player.score -= 5
        self.players[player._id] = player
        return film

    def cancel(self, player: Player) -> None:
        player.current_film = None
        self.players[player._id] = player
