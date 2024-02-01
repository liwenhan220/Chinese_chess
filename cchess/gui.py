from game import Game
import pygame
import sys
from pieces import *
from pprint import pprint
import numpy as np
from utils import is_chinese

# Constants
# WIDTH, HEIGHT = 600, 667
ROWS, COLS = 10, 9
SQUARE_SIZE = 60
WIDTH, HEIGHT = SQUARE_SIZE * COLS, SQUARE_SIZE * ROWS

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
wood_color = (205, 173, 0) # This RGB value has a yellowish-brown tint



# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chinese Chess")

# Font setup with the Chinese font file ("SimHei.ttf" in this example)
font_path = "SimHei.ttf"
font_size = 36
font = pygame.font.Font(font_path, font_size)

# Game Initialization
game = Game()

def draw_board():
    screen.fill(BLUE)  # Fill the background with blue color

    # Draw horizontal lines
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 2)

    # Draw vertical lines
    for col in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), 2)

    for row in range(ROWS):
        for col in range(COLS):
            piece = game.board[row][col]
            if piece:
                draw_piece(piece, row, col)

def draw_piece(piece, row, col):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2

    pygame.draw.circle(screen, WHITE, (x, y), SQUARE_SIZE // 2)
    
    text_surface = font.render(str(piece), True, RED if piece.type == 'red' else BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def highlight_piece(piece, color):
    x = piece.y * SQUARE_SIZE + SQUARE_SIZE // 2
    y = piece.x * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.circle(screen, color, (x, y), SQUARE_SIZE // 2, 2)  # Highlight the selected piece with a circle

def main():
    game.reset()  # Reset the game initially
    selected_piece = None
    last_piece = None
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE
                if selected_piece is not None:
                    if [row-selected_piece.x, col-selected_piece.y] not in selected_piece.king_protecting_moves:
                        if game.get_piece(row, col) is not None and game.get_piece(row, col).type == game.current_player:
                            selected_piece = game.get_piece(row, col)
                        else:
                            selected_piece = None
                    else:
                        game.step([[selected_piece.x, selected_piece.y], [row - selected_piece.x, col - selected_piece.y]])
                        last_piece = selected_piece
                        selected_piece = None
                else:
                    piece = game.get_piece(row, col)
                    if piece is not None and piece.type == game.current_player:
                        selected_piece = piece
                game.render()
                if game.game_end:
                    print(f'{game.winner} won')
        
        draw_board()
        if selected_piece and selected_piece.type == game.current_player:
            for move in selected_piece.king_protecting_moves:
                x, y = selected_piece.x + move[0], selected_piece.y + move[1]
                pygame.draw.circle(screen, GREEN, (y * SQUARE_SIZE + SQUARE_SIZE // 2, x * SQUARE_SIZE + SQUARE_SIZE // 2), 8)

        if selected_piece:
            highlight_piece(selected_piece, color = GREEN)

        if last_piece:
            highlight_piece(last_piece, color = RED)
        

        pygame.display.flip()

if __name__ == "__main__":
    main()
