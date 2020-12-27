from typing import Optional, List

from pieces import *
from utils import *


class Spot:
    def __init__(self, y: int, x: int, piece: 'Optional[Piece]' = None):
        self.x = x
        self.y = y
        self.piece = piece

    def __str__(self, ):
        if self:
            return str(self.piece)
        return ' '

    def __repr__(self, ):
        return str(self)

    def __bool__(self, ):
        return self.piece is not None


class Player:
    def __init__(self, color=Color.WHITE, turn=False):
        self.color = color
        self.turn = turn

    @staticmethod
    def ask_for_move(select: bool = False) -> [int, int]:
        text = 'Make Move: '
        if select:
            text = 'Select Figure: '
        move = input(text)
        if move == 'X':
            return None

        return LETTER_TO_INT[move[0].upper()], int(move[1:]) - 1

    def __bool__(self, ):
        return self.turn

    def __str__(self, ):
        return self.color.name.lower() + ' Player'

    def __repr__(self, ):
        return str(self)


class Board:
    def __init__(self, ):
        self.board: 'List[List[Spot]]' = []
        self.setup()

    def get_spot(self, x, y) -> 'Optional[Spot]':
        return self.board[y][x]

    def setup(self):
        self.board.append([
            Spot(0, 0, Rook(Color.WHITE)),
            Spot(0, 1, Knight(Color.WHITE)),
            Spot(0, 2, Bishop(Color.WHITE)),
            Spot(0, 3, Queen(Color.WHITE)),
            Spot(0, 4, King(Color.WHITE)),
            Spot(0, 5, Bishop(Color.WHITE)),
            Spot(0, 6, Knight(Color.WHITE)),
            Spot(0, 7, Rook(Color.WHITE))
        ])
        self.board.append([
            Spot(1, 0, Pawn(Color.WHITE)),
            Spot(1, 0, Pawn(Color.WHITE)),
            Spot(1, 2, Pawn(Color.WHITE)),
            Spot(1, 3, Pawn(Color.WHITE)),
            Spot(1, 4, Pawn(Color.WHITE)),
            Spot(1, 5, Pawn(Color.WHITE)),
            Spot(1, 6, Pawn(Color.WHITE)),
            Spot(1, 7, Pawn(Color.WHITE)),
        ])

        for i in range(2, 6):
            self.board.append([
                Spot(i, j) for j in range(0, 8)
            ])

        self.board.append([
            Spot(6, 0, Pawn(Color.BLACK)),
            Spot(6, 0, Pawn(Color.BLACK)),
            Spot(6, 2, Pawn(Color.BLACK)),
            Spot(6, 3, Pawn(Color.BLACK)),
            Spot(6, 4, Pawn(Color.BLACK)),
            Spot(6, 5, Pawn(Color.BLACK)),
            Spot(6, 6, Pawn(Color.BLACK)),
            Spot(6, 7, Pawn(Color.BLACK)),
        ])

        self.board.append([
            Spot(7, 0, Rook(Color.BLACK)),
            Spot(7, 1, Knight(Color.BLACK)),
            Spot(7, 2, Bishop(Color.BLACK)),
            Spot(7, 3, Queen(Color.BLACK)),
            Spot(7, 4, King(Color.BLACK)),
            Spot(7, 5, Bishop(Color.BLACK)),
            Spot(7, 6, Knight(Color.BLACK)),
            Spot(7, 7, Rook(Color.BLACK))
        ])

    def __repr__(self, ):
        return str(self)

    def __str__(self):
        board = "   ---------------------------------------"
        for y in range(7, -1, -1):
            board += f'\n {y + 1}|'
            for x in range(0, 8):
                board += f' [{self.board[y][x]}] '
        board += "\n   ---------------------------------------\n"
        board += '     A    B    C    D    E    F    G    H'
        return board


class Game:
    def __init__(self):
        self.board = Board()
        self.player_1 = Player(Color.WHITE, True)
        self.player_2 = Player(Color.BLACK, False)
        self.current_player = self.player_1 or self.player_2
        self.status = GameStatus.ACTIVE

    def update_turn(self):
        self.player_1.turn = not self.player_1
        self.player_2.turn = not self.player_2
        self.current_player = self.player_1 or self.player_2

    @staticmethod
    def make_move(start: Spot, end: Spot):
        piece = start.piece
        start.piece = None
        end.piece = piece
        piece.moved()

    def run(self, ):
        print(self.board)
        while self.status == GameStatus.ACTIVE:
            move = self.get_valid_move()
            if move is None:
                self.status = GameStatus.FORFEIT
                break
            self.make_move(*move)
            print(self.board)
            self.update_turn()

    def get_valid_move(self) -> Optional[Tuple[Spot, Spot]]:
        while 1:
            try:
                start = self.current_player.ask_for_move(select=True)
                if start is None:
                    y = input('Are you sure to forfeit: [Y/y]: ')
                    if y.lower() == 'y':
                        return None
                end = self.current_player.ask_for_move()

                start, end = self.board.get_spot(*start), self.board.get_spot(*end)
                valid = self.current_player.color == start.piece.color and start.piece.can_move(self.board, start, end)
                if valid:
                    return start, end
            except (IndexError, KeyError, ValueError):
                pass


if __name__ == '__main__':
    game = Game()
    game.run()
