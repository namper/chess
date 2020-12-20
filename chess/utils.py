from enum import Enum

LETTERS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
NUMBERS = (0, 1, 2, 3, 4, 5, 6, 7)

LETTER_TO_INT = dict(zip(LETTERS, NUMBERS))


class Color(Enum):
    WHITE = 'WHITE'
    BLACK = 'BLACK'


class State(Enum):
    ALIVE = 'ALIVE'
    DEAD = 'BLACK'


class GameStatus(Enum):
    ACTIVE = 'Active'
    BLACK_WIN = 'BLACK_WIN'
    WHITE_WIN = 'WHITE_WIN'
    FORFEIT = 'FORFEIT'
    STALEMATE = 'STALEMATE'
    RESIGNATION = 'RESIGNATION'
