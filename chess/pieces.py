from abc import ABCMeta, abstractmethod
from typing import Tuple

import game
from utils import *


class Piece(metaclass=ABCMeta):
    def __init__(self, color=Color.WHITE, state=State.ALIVE):
        self.state = state
        self.color = color

    @property
    @abstractmethod
    def display(self, ):
        pass

    @abstractmethod
    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot'):
        if end and end.piece.color == self.color:
            return False

    @staticmethod
    def get_distance(start: 'game.Spot', end: 'game.Spot') -> Tuple[int, int]:
        return abs(start.x - end.x), abs(start.y - end.y)

    def moved(self, ):
        pass

    def __str__(self, ):
        return self.display[self.color]


class Rook(Piece):
    display = {
        Color.BLACK: '♖',
        Color.WHITE: '♜'
    }

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot'):
        super().can_move(board, start, end)
        dist_x, dist_y = self.get_distance(start, end)
        return dist_x * dist_y == 0


class Pawn(Piece):
    initial = True
    display = {
        Color.BLACK: '♙',
        Color.WHITE: '♟'
    }

    direction = {
        Color.WHITE: -1,
        Color.BLACK: 1
    }

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot'):
        super().can_move(board, start, end)
        dy, dx = self.direction[self.color] * (start.x - end.x), abs(start.y - end.y)
        print(dx, dy)

        if dy < 0:
            return False

        elif end and end.piece.color != self.color:
            return abs(dx) == dy == 1

        elif dx != 0:
            return False

        elif not self.initial:
            return 0 < dy <= 1

        else:
            return 0 < dy <= 2

    def moved(self, ):
        self.initial = False


class Knight(Piece):
    display = {
        Color.BLACK: '♘',
        Color.WHITE: '♞'
    }

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot', ):
        super().can_move(board, start, end)
        dx, dy = self.get_distance(start, end)
        print(dx, dy)
        return dx * dy == 2


class Bishop(Piece):
    display = {
        Color.BLACK: '♗',
        Color.WHITE: '♝'
    }

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot', ):
        super().can_move(board, start, end)
        dx, dy = self.get_distance(start, end)
        return dx == dy


class King(Piece):
    display = {
        Color.BLACK: '♔',
        Color.WHITE: '♚'
    }
    castled = False
    can_castle = True

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot'):
        super().can_move(board, start, end)
        dx, dy = self.get_distance(start, end)
        return dx + dy == 1

    def moved(self, ):
        self.can_castle = False


class Queen(Piece):
    display = {
        Color.BLACK: '♛',
        Color.WHITE: '♕'
    }

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot'):
        super().can_move(board, start, end)
        dx, dy = self.get_distance(start, end)
        return dx * dy == 0 or dx == dy
