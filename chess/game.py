from typing import Optional, List

from pieces import *
from utils import *


class Spot:
    def __init__(self, x: int, y: int, piece: Optional[Piece] = None):
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
    def __init__(self, turn=True, color=Color.WHITE):
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
        x, y = move[0], move[-1]  # type: str, str

        x: int = LETTER_TO_INT[x.upper()]
        y: int = int(y) - 1
        return x, y

    def get_valid_move(
            self,
            board: 'Board',
    ) -> Optional[Tuple[Spot, Spot]]:
        # @TODO: Improve
        valid = False
        while not valid:
            try:
                start = self.ask_for_move(select=True)
                if start is None:
                    y = input('Are you sure to forfeit: [Y/y]: ')
                    if y.lower() == 'y':
                        return None
                end = self.ask_for_move()
                start, end = board.get_spot(*start), board.get_spot(*end)
                piece: Piece = start.piece
                valid = board.current_player.color == piece.color and piece.can_move(board, start, end)
            except:
                pass

        return start, end

    def __bool__(self, ):
        return self.turn

    def __str__(self, ):
        return self.color.name.lower() + ' Player'

    def __repr__(self, ):
        return str(self)


class Board:
    def __init__(self, player_1: Player, player_2: Player, ):
        self.board: 'List[List[Spot]]' = []
        self.player_1 = player_1
        self.player_2 = player_2
        self.setup_players()
        self.setup()
        self.status = GameStatus.ACTIVE
        self.current_player = self.player_1 or self.player_2

    def get_spot(self, x, y) -> 'Optional[Spot]':
        return self.board[y][x]

    def setup_players(self, ):

        if self.player_1.color == Color.WHITE:
            self.player_1.turn = True
            self.player_2.color = Color.BLACK
            self.player_2.turn = False
        else:
            self.player_2.color = Color.White
            self.player_2.turn = True
            self.player_1.color = Color.BLACK
            self.player_1.turn = False

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

    def change_turn(self, ):
        self.player_1.turn = not self.player_1.turn
        self.player_2.turn = not self.player_2.turn
        self.current_player = self.player_1 or self.player_2

    @staticmethod
    def make_move(start: Spot, end: Spot):
        piece = start.piece
        start.piece = None
        end.piece = piece
        piece.moved()

    def game(self, ):
        while self.status == GameStatus.ACTIVE:
            move = self.current_player.get_valid_move(
                board=self
            )

            if move is None:
                self.status = GameStatus.FORFEIT
                break

            self.make_move(*move)
            print(self)
            self.change_turn()

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


if __name__ == '__main__':
    b = Board(Player(), Player())
    print(b)
    b.game()
