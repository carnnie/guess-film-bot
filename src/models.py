from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Player:
    """Class representing a player object.

    Properties:
        _id: Player's unique identifier.
        current_film: Id of current film in the game. If None player is not in the game.
        guessed_films: List of films ids which player already guessed.
        attempts: Number of attempts player made to guess current film.
        score: Total score of player.
        in_game: Indicates if player is in the game.

    """
    _id: int
    current_film: Optional[int] = None
    guessed_films: List[int] = field(default_factory=list)
    attempts: int = 0
    score: int = 0

    @property
    def in_game(self) -> bool:
        return isinstance(self.current_film, int)


@dataclass
class Film:
    _id: int
    name: str
    year: int
    genre: str
    description: Optional[str] = None
    image_path: Optional[str] = None
