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
        if (start is end) or (end and end.piece.color == self.color):
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
        dx, dy = self.get_distance(start, end)
        if dx * dy != 0:
            return False
        elif dx != 0:
            start_x, end_x = sorted([start.x, end.x])
            return not any(board.board[start.y][start_x + 1:end_x])
        else:
            start_y, end_y = sorted([start.y, end.y])
            for y in range(start_y + 1, end_y):
                if board.get_spot(start.x, y):
                    return False
        return True


class Pawn(Piece):
    display = {
        Color.BLACK: '♙',
        Color.WHITE: '♟'
    }

    direction = {
        Color.WHITE: -1,
        Color.BLACK: 1
    }

    initial = True

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot', ):
        super().can_move(board, start, end)
        dy = self.direction[self.color] * (start.y - end.y)
        dx = abs(start.x - end.x)

        if dy <= 0:
            return False

        elif end and end.piece.color != self.color:
            return abs(dx) == dy == 1

        elif self.initial:
            return 0 < dy <= 2

        return 0 < dy <= 1

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
        return dx * dy == 2


class Bishop(Piece):
    display = {
        Color.BLACK: '♗',
        Color.WHITE: '♝'
    }

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot', ):
        super().can_move(board, start, end)
        dx, dy = end.x - start.x, end.y - start.y

        if abs(dx) != abs(dy):
            return False

        x_inc = dx // abs(dx)
        y_inc = dy // abs(dy)
        x, y = start.x, start.y
        for k in range(abs(dx)):
            x += x_inc
            y += y_inc
            if board.get_spot(x, y):
                return False

        return True


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
        return (dy + dx == 1) or (dx == 1 and dy == 1)

    def moved(self, ):
        self.can_castle = False


class Queen(Piece):
    display = {
        Color.BLACK: '♛',
        Color.WHITE: '♕'
    }

    def can_move(self, board: 'game.Board', start: 'game.Spot', end: 'game.Spot'):
        super().can_move(board, start, end)
        dx, dy = end.x - start.x, end.y - start.y
        if dx * dy == 0:
            if dx != 0:
                start_x, end_x = sorted([start.x, end.x])
                return not any(board.board[start.y][start_x + 1:end_x])
            else:
                start_y, end_y = sorted([start.y, end.y])
                for y in range(start_y + 1, end_y):
                    if board.get_spot(start.x, y):
                        return False
        else:
            if abs(dx) != abs(dy):
                return False

            x_inc = dx // abs(dx)
            y_inc = dy // abs(dy)
            x, y = start.x, start.y
            for k in range(abs(dx)):
                x += x_inc
                y += y_inc
                if board.get_spot(x, y):
                    return False

        return True
