from pieces import *
from pprint import pprint
import numpy as np
from utils import is_chinese
        
class Game:
    def __init__(self):
        # Initialize the board with None
        self.board = np.array([[None for _ in range(9)] for _ in range(10)])
        
        # Initialize the dict of list to keep track of alive pieces for red and black
        self.alive_pieces = {}
        self.alive_pieces['black'] = []
        self.alive_pieces['red'] = []
        self.current_player = 'red'
        self.game_end = False
        self.winner = None

    def remove_piece(self, piece):
        self.board[piece.x][piece.y] = None
        self.alive_pieces[piece.type].remove(piece)
    
    def switch_player(self):
        if self.current_player == 'red':
            self.current_player = 'black'
        else:
            self.current_player = 'red'
    
    def reset(self):
        self.game_end = False
        self.winner = None
        self.current_player = 'red'
        self.board = np.array([[None for _ in range(9)] for _ in range(10)])
        self.alive_pieces['red'] = []
        self.alive_pieces['black'] = []
        # Add Black pieces
        self.add_piece(Rook(0, 0, 'black'))
        self.add_piece(Knight(0, 1, 'black'))
        self.add_piece(Elephant(0, 2, 'black'))
        self.add_piece(Guard(0, 3, 'black'))
        self.add_piece(King(0, 4, 'black'))
        self.add_piece(Guard(0, 5, 'black'))
        self.add_piece(Elephant(0, 6, 'black'))
        self.add_piece(Knight(0, 7, 'black'))
        self.add_piece(Rook(0, 8, 'black'))
        self.add_piece(Cannon(2, 1, 'black'))
        self.add_piece(Cannon(2, 7, 'black'))
        self.add_piece(Pawn(3, 0, 'black'))
        self.add_piece(Pawn(3, 2, 'black'))
        self.add_piece(Pawn(3, 4, 'black'))
        self.add_piece(Pawn(3, 6, 'black'))
        self.add_piece(Pawn(3, 8, 'black'))

        # Add Red pieces
        self.add_piece(Rook(9, 0, 'red'))
        self.add_piece(Knight(9, 1, 'red'))
        self.add_piece(Elephant(9, 2, 'red'))
        self.add_piece(Guard(9, 3, 'red'))
        self.add_piece(King(9, 4, 'red'))
        self.add_piece(Guard(9, 5, 'red'))
        self.add_piece(Elephant(9, 6, 'red'))
        self.add_piece(Knight(9, 7, 'red'))
        self.add_piece(Rook(9, 8, 'red'))
        self.add_piece(Cannon(7, 1, 'red'))
        self.add_piece(Cannon(7, 7, 'red'))
        self.add_piece(Pawn(6, 0, 'red'))
        self.add_piece(Pawn(6, 2, 'red'))
        self.add_piece(Pawn(6, 4, 'red'))
        self.add_piece(Pawn(6, 6, 'red'))
        self.add_piece(Pawn(6, 8, 'red'))

        self.update_potential_moves()
        self.update_king_protecting_moves()
    
    def step(self, action):
        if self.game_end:
            return
        # action format: [[startx, starty], [vec_x, vec_y]]
        startx, starty = action[0]
        i, j = action[1]
        piece = self.get_piece(startx, starty)
        if piece is None:
            return
        
        if piece.type != self.current_player:
            return
        
        if [i, j] not in piece.king_protecting_moves:
            return
        
        self.move_piece(piece, piece.x + i, piece.y + j)
        self.update_potential_moves()
        self.update_king_protecting_moves()
        self.switch_player()
        if self.is_check_mate(self.current_player):
            self.game_end = True
            self.winner = self.opponent(self.current_player)

    def is_check_mate(self, stype):
        for piece in self.alive_pieces[stype]:
            if len(piece.king_protecting_moves) > 0:
                return False
        return True

    def out_of_bound(self, x, y):
        return x < 0 or x >= 10 or y < 0 or y >= 9

    def update_potential_moves(self, stypes = ['red', 'black']):
        for stype in stypes:
            assert stype == 'red' or stype == 'black'
            for piece in self.alive_pieces[stype]:
                piece.update_potential_moves(self.board)

    def update_king_protecting_moves(self, stypes = ['red', 'black']):
        for stype in stypes:
            assert stype == 'red' or stype == 'black'
            for piece in self.alive_pieces[stype]:
                piece.update_king_protecting_moves(self)

    def add_piece(self, piece: GenericPiece):
        # Add the piece to the board and alive_pieces
        x, y = piece.x, piece.y
        self.board[x][y] = piece
        self.alive_pieces[piece.type].append(piece)

    def get_str_board(self, display=False):
        board = np.array([['.' for _ in range(9)] for _ in range(10)])
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is not None:
                    board[i][j] = str(piece)
        if display:
            pprint(board)
        return board

    def render(self, board = None, display = True):
        if board is None:
            board = self.get_str_board()
        result = '  '
        for j in range(len(board[0])):
            result += str(j) + '  '
        result += '\n'

        for i, row in enumerate(board):
            result += str(i) + ' '
            for ele in row:
                if not is_chinese(ele):
                    result += ele + '  '
                else:
                    result += ele + ' '
            result += '\n'
        if display:
            print(result, end='\n' * 5)
        result += self.current_player
        return result

    def visualize_potential_moves(self, piece: GenericPiece):
        board = self.get_str_board()
        for move in piece.potential_moves:
            x, y = piece.x + move[0], piece.y + move[1]
            if self.out_of_bound(x, y):
                continue
            if board[x][y] == '.':
                board[x][y] = 'o'
            else:
                board[x][y] = 'x'
        self.render(board)

    def move_piece(self, piece: GenericPiece, x: int, y: int):
        assert piece in self.alive_pieces[piece.type]
        assert self.out_of_bound(x, y)
        self.board[piece.x][piece.y] = None
        piece.x = x
        piece.y = y
        if self.board[x][y] is not None:
            dead_piece = self.board[x][y]
            self.remove_piece(dead_piece)
        self.board[piece.x][piece.y] = piece

    # names include ['rook', 'cannon', 'knight', 'elephant', 'guard', 'pawn', 'king']
    def find_piece(self, name, stypes = ['red', 'black']):
        result = []
        for stype in stypes:
            assert stype == 'red' or stype == 'black'
            for piece in self.alive_pieces[stype]:
                if name == piece.name:
                    result.append(piece)
        return result
    
    def get_piece(self, x, y):
        return self.board[x][y]
    

    def opponent(self, stype):
        if stype == 'red':
            return 'black'
        return 'red'
    
    def is_king_exposed(self, stype):
        target_king = self.find_piece(name='king', stypes=[stype])[0]
        for piece in self.alive_pieces[self.opponent(stype)]:
            for i, j in piece.potential_moves:
                xx, yy = piece.x + i, piece.y + j
                if xx == target_king.x and yy == target_king.y:
                    return True
        return False



# game = Game()
# game.reset()
# game.update_potential_moves()

# # game.remove_piece(game.get_piece(3, 4))
# game.remove_piece(game.get_piece(0, 2))
# game.update_potential_moves()

# game.visualize_potential_moves(game.get_piece(0, 1))