from abc import ABCMeta, abstractmethod, abstractproperty
from typing import TYPE_CHECKING, Tuple
from utils import Color, State

class Piece(metaclass=ABCMeta):
    def __init__(self, color = Color.WHITE, state = State.ALIVE):
        self.state = state
        self.color = color
    
    @property
    @abstractmethod
    def display(self,):
        pass

    @abstractmethod
    def can_move(self, board: 'Board', start: 'Spot', end: 'Spot'):
        if end and end.piece.color == self.color:
            return False

    @staticmethod
    def get_distance(start: 'Spot', end: 'Spot') -> Tuple['Spot', 'Spot']:
        return abs(start.x - end.x), abs(start.y - end.y)

    def moved(self,):
        # do nothing
        pass

    def __str__(self,):
        return self.display[self.color]
