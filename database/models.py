from dataclasses import dataclass, field
import os
from typing import List, Optional

from aiogram.types import FSInputFile

from config.config import BASE_PATH


@dataclass
class Player:
    """Class representing a player object.

    Properties:
        _id: Player's unique identifier.
        current_film: Id of current film in the game. If None player is not in the game.
        attempts: Number of attempts player have to guess current film.
        guessed_films: List of films ids which player already guessed.
        score: Total score of player.
        in_game: Indicates if player is in the game.

    """

    _id: int
    current_film: Optional[int] = None
    attempts: int = 0
    guessed_films: List[int] = field(default_factory=list)
    score: int = 0


@dataclass
class Film:
    _id: int
    name: str
    year: int
    genre: str
    description: Optional[str] = None
    image_path: Optional[str] = None

    def get_image_file(self) -> Optional[FSInputFile]:
        """Returns the film image file or `None` if file does not exist."""
        if self.image_path:
            path = os.path.join(BASE_PATH, self.image_path)

        return FSInputFile(path) if os.path.isfile(path) else None

    def explain(self) -> str:
        """Returns explanation for film with name, date, genre and short description."""
        return f"{self.name}, {self.year}\n\n{self.genre}.\n{self.description}"
