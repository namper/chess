from typing import NewType, Tuple, Optional, TYPE_CHECKING
from base import Piece
from utils import Color, State, GameStatus, LETTER_TO_INT, skip_errors

class Rook(Piece):
    display = {
        Color.BLACK: '♖',
        Color.WHITE: '♜'
    }

    def can_move(self, board: 'Board', start: 'Spot', end: 'Spot'):
        super().can_move(board, start, end)
        dist_x, dist_y = self.get_distance(start, end)
        return dist_x * dist_y == 0
        


class Pawn(Piece):
    initial = True
    display = {
        Color.BLACK: '♙',
        Color.WHITE: '♟'
    }
    
    def can_move(self, board: 'Board', start: 'Spot', end: 'Spot'):
        super().can_move(board, start, end)
        dy, dx = abs(start.x - end.x), start.y - end.y
        # print(dx, dy)

        if dy < 0:
            return False

        elif end and end.piece.color != self.color:
            return dx == dy == 1

        elif dx != 0:
            return False

        elif not self.initial:
            return 0 < dy < 1

        else:
            return 0 < dy <= 2
    
    def moved(self, ):
        self.initial = False



class Knight(Piece):
    display = {
        Color.BLACK: '♘',
        Color.WHITE: '♞'
    }
    
    
    def can_move(self, board: 'Board', start: 'Spot', end: 'Spot',):
        super().can_move(board, start, end)
        dx, dy = abs(start.x - end.y), abs(start.y - end.y)
        return dx * dy == 2


class Bishop(Piece):
    display = {
        Color.BLACK: '♗',
        Color.WHITE: '♝'
    }
    
    def can_move(self, board: 'Board', start: 'Spot', end: 'Spot'):
        super().can_move(board, start, end)
        dx, dy = abs(start.x - end.y), abs(start.y - end.y)
        return dx == dy



class King(Piece):
    display = {
        Color.BLACK: '♔',
        Color.WHITE: '♚'
    }
    castled = False
    can_castle = True

    
    def can_move(self, board: 'Board', start: 'Spot', end: 'Spot'):
        super(board, start, end)
        dx, dy = self.get_distance(start, end)
        return dx + dy == 1
    

class Queen(Piece):
    display = {
        Color.BLACK: '♛',
        Color.WHITE: '♕'
    }
    
    def can_move(self, board: 'Board', start: 'Spot', end: 'Spot'):
        super(board, start, end)
        dx, dy = self.get_distance(start, end)
        return dx * dy == 0 or dx == dy



class Spot:
    def __init__(self, x: int, y: int, piece: Optional[Piece] = None):
        self.x = x
        self.y = y
        self.piece = piece

    def __str__(self,):
        if self:
            return str(self.piece)
        return ' '
    
    def __repr__(self, ):
        return str(self)

    def __bool__(self,):
        return self.piece is not None



class Player:
    def __init__(self, turn = True, color = Color.WHITE):
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
        letter, integer = move[0], move[-1]
        letter = LETTER_TO_INT[letter.upper()]
        integer = int(integer) - 1
        return letter, integer


    def get_valid_move(
        self,
        board: 'Board',
        ) -> Optional[Tuple[Spot, Spot]]:
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
                valid = board.current_player.color == piece.color and piece.can_move(self, start, end)
            except:
                pass
        return start, end

    def __bool__(self, ):
        return self.turn

    def __str__(self,):
        return self.color.name.lower() + ' Player'
    
    def __repr__(self,):
        return str(self)



class Board:
    def __init__(self, player_1: Player, player_2: Player, ):
        self.setup_players(player_1, player_2)                
        self.setup()
        self.status = GameStatus.ACTIVE

    def get_spot(self, x, y):
        return self.board[y][x]

    def setup_players(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2

        if self.player_1.color == Color.WHITE:
            self.player_1.turn = True
            self.player_2.color = Color.BLACK
            self.player_2.turn = False
        else:
            self.player_2.color = Color.White
            self.player_2.turn = True
            self.player_1.color = Color.BLACK
            self.player_1.turn = False
        
        self.current_player = self.player_1 or self.player_2

    def setup(self):
        self.board = [[None]*8]*8

        self.board[0] = [
            Spot(0, 0, Rook(Color.WHITE)),
            Spot(0, 1, Knight(Color.WHITE)),
            Spot(0, 2, Bishop(Color.WHITE)),
            Spot(0, 3, Queen(Color.WHITE)),
            Spot(0, 4, King(Color.WHITE)),
            Spot(0, 5, Bishop(Color.WHITE)),
            Spot(0, 6, Knight(Color.WHITE)),
            Spot(0, 7, Rook(Color.WHITE))
        ]
        self.board[1] = [
            Spot(1, 0, Pawn(Color.WHITE)),
            Spot(1, 0, Pawn(Color.WHITE)),
            Spot(1, 2, Pawn(Color.WHITE)),
            Spot(1, 3, Pawn(Color.WHITE)),
            Spot(1, 4, Pawn(Color.WHITE)),
            Spot(1, 5, Pawn(Color.WHITE)),
            Spot(1, 6, Pawn(Color.WHITE)),
            Spot(1, 7, Pawn(Color.WHITE)),
        ]

        self.board[7] = [
            Spot(7, 0, Rook(Color.BLACK)),
            Spot(7, 1, Knight(Color.BLACK)),
            Spot(7, 2, Bishop(Color.BLACK)),
            Spot(7, 3, Queen(Color.BLACK)),
            Spot(7, 4, King(Color.BLACK)),
            Spot(7, 5, Bishop(Color.BLACK)),
            Spot(7, 6, Knight(Color.BLACK)),
            Spot(7, 7, Rook(Color.BLACK))
        ]
        self.board[6] = [
            Spot(6, 0, Pawn(Color.BLACK)),
            Spot(6, 0, Pawn(Color.BLACK)),
            Spot(6, 2, Pawn(Color.BLACK)),
            Spot(6, 3, Pawn(Color.BLACK)),
            Spot(6, 4, Pawn(Color.BLACK)),
            Spot(6, 5, Pawn(Color.BLACK)),
            Spot(6, 6, Pawn(Color.BLACK)),
            Spot(6, 7, Pawn(Color.BLACK)),
        ]

        for i in range(2, 6):
            self.board[i] = [
                Spot(i, j) for j in range(0, 8)
            ]

    def change_turn(self,):
        self.player_1.turn = not self.player_1.turn
        self.player_2.turn = not self.player_2.turn
        self.current_player = self.player_1 or self.player_2

    def make_move(self, start: Spot, end: Spot):
        piece = start.piece
        start.piece = None
        end.piece = piece
        piece.moved()

    def game(self,):
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

    def __repr__(self,):
        return str(self)

    def __str__(self):
        board = "   ---------------------------------------"
        for y in range(7, -1, -1):
            board += f'\n {y+1}|'
            for x in range(0, 8):
                board += f' [{self.board[y][x]}] '
        board += "\n   ---------------------------------------\n"
        board += '     A    B    C    D    E    F    G    H'
        return board


if __name__ == '__main__':
    b = Board(Player(), Player())
    print(b)
    b.game()