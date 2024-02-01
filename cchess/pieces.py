import pdb
import numpy as np
import copy
# from game import Game
class GenericPiece:
    def __init__(self, x, y, stype = 'red'):
        assert stype == 'red' or stype == 'black'
        assert not self.out_of_bound(x, y)
        self.name = 'generic_piece'
        self.type = stype
        self.x = x
        self.y = y
        self.potential_moves = []
        self.king_protecting_moves = []
    
    def __str__(self):
        return None

    def out_of_bound(self, x, y):
        return x < 0 or x >= 10 or y < 0 or y >= 9
    
    def crossed_river(self, x, y):
        # This detects if a chess piece has crossed the river
        if self.type == 'red':
            return x < 5 or x >= 10 or y < 0 or y >= 9
        else:
            return x < 0 or x >= 5 or y < 0 or y >= 9
        
    def out_of_palace(self, x, y):
        # This checks if a piece has moved out of the palace
        if self.type == 'red':
            return y < 3 or y >= 6 or x < 7 or x >= 10
        else:
            return y < 3 or y >= 6 or x < 0 or x >= 3
    
    def update_potential_moves(self, board):
        # This board should be a 2D array of piece objects, it then finds the valid potential move under current game position
        pass

    def update_king_protecting_moves(self, game):
        # Reset king_protecting_moves to potential_moves
        self.king_protecting_moves = self.potential_moves.copy()
        # Simulate moves and check if they expose the king
        for move in self.potential_moves:
            new_x, new_y = self.x + move[0], self.y + move[1]
            env = copy.deepcopy(game)
            stype = self.type

            piece = env.get_piece(self.x, self.y)
            env.move_piece(piece, new_x, new_y)
            env.update_potential_moves()
            if env.is_king_exposed(stype=stype):
                self.king_protecting_moves.remove(move)

class Rook(GenericPiece):
    def __init__(self, x, y, stype = 'red'):
        super().__init__(x, y, stype)
        self.name = 'rook'
        for i in range(1, 10):
            self.potential_moves.append([i, 0])
            self.potential_moves.append([-i, 0])
        
        for i in range(1, 9):
            self.potential_moves.append([0, i])
            self.potential_moves.append([0, -i])
    
    def __str__(self):
        if self.type == 'red':
            return '车'
        return '車'
    
    def update_potential_moves(self, board):
        self.potential_moves = []
        #Check vertical downward moves
        for i in range(1, 10):
            xx, yy = self.x + i, self.y
            
            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break

            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if board[xx][yy].type == self.type:
                    break
                else:
                    self.potential_moves.append([i, 0])
                    break
            else:
                self.potential_moves.append([i, 0])
    
        #Check vertical upward moves
        for i in range(1, 10):
            xx, yy = self.x - i, self.y
            
            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break

            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if board[xx][yy].type == self.type:
                    break
                else:
                    self.potential_moves.append([-i, 0])
                    break
            else:
                self.potential_moves.append([-i, 0])

        # Check Horizontal rightward moves:
        for j in range(1, 9):
            xx, yy = self.x, self.y + j

            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break

            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if board[xx][yy].type == self.type:
                    break
                else:
                    self.potential_moves.append([0, j])
                    break
            else:
                self.potential_moves.append([0, j])
        
        # Check Horizontal leftward moves:
        for j in range(1, 9):
            xx, yy = self.x, self.y - j

            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break

            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if board[xx][yy].type == self.type:
                    break
                else:
                    self.potential_moves.append([0, -j])
                    break

            else:
                self.potential_moves.append([0, -j])

class Knight(GenericPiece):
    def __init__(self, x, y, stype = 'red'):
        super().__init__(x, y, stype)
        self.name = 'knight'
        for i in [-1, 1]:
            self.potential_moves.append([1 * i, 2 * i])
            self.potential_moves.append([1 * i, -2 * i])
            self.potential_moves.append([2 * i, 1 * i])
            self.potential_moves.append([2 * i, -1 * i])

    def __str__(self):
        if self.type == 'red':
            return '马'
        return '馬'
    
    def update_potential_moves(self, board):
        self.potential_moves = []

        for c in [1, -1]:
            for vec in [[c, 2 * c], [c, -2 * c], [2 * c, c], [2 * c, -c]]:
                pre_coord = [self.x, self.y]
                index = np.argmax(np.absolute(vec))
                pre_coord[index] += 1 * np.sign(vec[index])
                pre_coord = tuple(pre_coord)

                coord = (vec[0] + self.x, vec[1] + self.y)
                if (not self.out_of_bound(coord[0], coord[1])) and (board[pre_coord] is None) and (board[coord] is None or board[coord].type != self.type):
                    self.potential_moves.append(vec)

class Elephant(GenericPiece):
    def __init__(self, x, y, stype='red'):
        super().__init__(x, y, stype=stype)
        self.name = 'elephant'
        for i in [-1, 1]:
            self.potential_moves.append([-2 * i, 2 * i])
            self.potential_moves.append([2 * i, 2 * i])

    def __str__(self):
        if self.type == 'red':
            return '相'
        return '象'
    
    def update_potential_moves(self, board):
        assert not self.crossed_river(self.x, self.y)
        self.potential_moves = []
        for c in [-1, 1]:
            # upper left
            i, j = -2 * c, 2 * c
            xx, yy = self.x + i, self. y + j
            if (not self.crossed_river(xx, yy)) and (board[self.x + i//2][self.y + j//2] is None) and (board[xx][yy] is None or board[xx][yy].type != self.type):
                self.potential_moves.append([i, j])
            
            i, j = 2 * c, 2 * c
            xx, yy = self.x + i, self.y + j
            if (not self.crossed_river(xx, yy)) and (board[self.x + i//2][self.y + j//2] is None) and (board[xx][yy] is None or board[xx][yy].type != self.type):
                self.potential_moves.append([i, j])

class Cannon(GenericPiece):
    def __init__(self, x, y, stype='red'):
        super().__init__(x, y, stype)
        self.name = 'cannon'
        for i in range(1, 10):
            self.potential_moves.append([i, 0])
            self.potential_moves.append([-i, 0])
        
        for i in range(1, 9):
            self.potential_moves.append([0, i])
            self.potential_moves.append([0, -i])
    
    def __str__(self):
        if self.type == 'red':
            return '炮'
        return '砲'

    def update_potential_moves(self, board):
        self.potential_moves = []
        #Check vertical downward moves
        bridge_exist = False
        for i in range(1, 10):
            xx, yy = self.x + i, self.y
            
            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break
            
            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if bridge_exist:
                    if board[xx][yy].type == self.type:
                        break
                    else:
                        self.potential_moves.append([i, 0])
                        break
                else:
                    bridge_exist = True
            else:
                if bridge_exist:
                    continue
                else:
                    self.potential_moves.append([i, 0])

        bridge_exist = False
        #Check vertical upward moves
        for i in range(1, 10):
            xx, yy = self.x - i, self.y
            
            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break
            
            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if bridge_exist:
                    if board[xx][yy].type == self.type:
                        break
                    else:
                        self.potential_moves.append([-i, 0])
                        break
                else:
                    bridge_exist = True
            else:
                if bridge_exist:
                    continue
                else:
                    self.potential_moves.append([-i, 0])

        bridge_exist = False
        # Check Horizontal rightward moves:
        for j in range(1, 9):
            xx, yy = self.x, self.y + j

            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break
            
            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if bridge_exist:
                    if board[xx][yy].type == self.type:
                        break
                    else:
                        self.potential_moves.append([0, j])
                        break
                else:
                    bridge_exist = True
            else:
                if bridge_exist:
                    continue
                else:
                    self.potential_moves.append([0, j])
        
        bridge_exist = False
        # Check Horizontal leftward moves:
        for j in range(1, 9):
            xx, yy = self.x, self.y - j
            
            # Break if out of bound
            if self.out_of_bound(xx, yy):
                break
            
            # Break if meet same type, add one additional move if meet enemy type
            if board[xx][yy] is not None:
                if bridge_exist:
                    if board[xx][yy].type == self.type:
                        break
                    else:
                        self.potential_moves.append([0, -j])
                        break
                else:
                    bridge_exist = True
            else:
                if bridge_exist:
                    continue
                else:
                    self.potential_moves.append([0, -j])

class Guard(GenericPiece):
    def __init__(self, x, y, stype='red'):
        super().__init__(x, y, stype=stype)
        self.name = 'guard'
        for i in [-1, 1]:
            self.potential_moves.append([-i, i])
            self.potential_moves.append([i, i])
        
    def __str__(self):
        if self.type == 'red':
            return '士'
        return '仕'
    
    def update_potential_moves(self, board):
        assert not self.out_of_palace(self.x, self.y)
        self.potential_moves = []
        for c in [-1, 1]:
            for i, j in [[-c, c], [c, c]]:
                xx, yy = self.x + i, self.y + j
                if (not self.out_of_palace(xx, yy) and (board[xx][yy] is None or board[xx][yy].type != self.type)):
                    self.potential_moves.append([i, j])

class Pawn(GenericPiece):
    def __init__(self, x, y, stype='red'):
        super().__init__(x, y, stype=stype)
        self.name = 'pawn'
        if self.type == 'red':
            self.potential_moves.append([-1, 0])
            self.potential_moves.append([0, 1])
            self.potential_moves.append([0, -1])
        else:
            self.potential_moves.append([1, 0])
            self.potential_moves.append([0, 1])
            self.potential_moves.append([0, -1])

    def __str__(self):
        if self.type == 'red':
            return '兵'
        return '卒'
    
    def update_potential_moves(self, board):
        self.potential_moves = []
        if self.type == 'red':
            xx, yy = self.x - 1, self.y
            if (not self.out_of_bound(xx, yy)) and (board[xx][yy] is None or board[xx][yy].type != self.type):
                self.potential_moves.append([-1, 0])

            if self.crossed_river(self.x, self.y):
                for i, j in [[0, 1], [0, -1]]:
                    xx, yy = self.x + i, self.y + j
                    if (not self.out_of_bound(xx, yy)) and (board[xx][yy] is None or board[xx][yy].type != self.type):
                        self.potential_moves.append([i, j])
        else:
            xx, yy = self.x + 1, self.y
            if (not self.out_of_bound(xx, yy)) and (board[xx][yy] is None or board[xx][yy].type != self.type):
                self.potential_moves.append([1, 0])

            if self.crossed_river(self.x, self.y):
                for i, j in [[0, 1], [0, -1]]:
                    xx, yy = self.x + i, self.y + j
                    if (not self.out_of_bound(xx, yy)) and (board[xx][yy] is None or board[xx][yy].type != self.type):
                        self.potential_moves.append([i, j])

class King(GenericPiece):
    def __init__(self, x, y, stype='red'):
        super().__init__(x, y, stype=stype)
        self.name = 'king'
        self.potential_moves.append([1, 0])
        self.potential_moves.append([-1, 0])
        self.potential_moves.append([0, 1])
        self.potential_moves.append([0, -1])
        if self.type == 'red':
            self.potential_moves.append([-9, 0])
        else:
            self.potential_moves.append([9, 0])

    def __str__(self):
        if self.type == 'red':
            return '帅'
        return '将'
    
    def update_potential_moves(self, board):
        self.potential_moves = []
        for i, j in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
            xx, yy = self.x + i, self.y + j
            if (not self.out_of_palace(xx, yy)) and (board[xx][yy] is None or board[xx][yy].type != self.type):
                self.potential_moves.append([i, j])

        if self.type == 'red':
            index = self.x - 1
            while index >= 0:
                piece = board[index][self.y]
                if piece is not None:
                    if piece.name != 'king':
                        break
                    else:
                        self.potential_moves.append([index - self.x, 0])
                        break
                index -= 1
        else:
            index = self.x + 1
            while index < 10:
                piece = board[index][self.y]
                if piece is not None:
                    if piece.name != 'king':
                        break
                    else:
                        self.potential_moves.append([index - self.x, 0])
                        break
                index += 1

