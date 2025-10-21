import random
import os
import pygame
import sys

GAME_PATH = os.path.dirname(__file__)
ASSET_FILE = os.path.join(GAME_PATH, 'assets')
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700
WINDOW_TITLE = "Lanx's Nonogram"

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BACKGROUND = (244, 244, 244)

class Nonogram:
    def __init__(self, width, height, lives):
        self.BOARD = []
        self.width = width
        self.height = height
        self.ROW_NUMBERS = []
        self.COLUMN_NUMBERS = []
        self.LIVES = lives
        self.allow_click = True
        self.grid_start_x = 50
        self.grid_start_y = 50
        self.row_num_start_x = 510
        self.row_num_start_y = 50
        self.column_num_start_x = self.grid_start_x + 5
        self.column_num_start_y = 510
        self.box_size = 30
    
        pygame.init()
        pygame.font.init()
        self.FONT = pygame.font.SysFont("Arial", 20)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        RUNNING = True
        self.screen_setup()
        self.game_setup()

        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse click detected
                    if event.button == 1: # Left mouse button click
                        print("Left mouse button")
                    elif event.button == 3: # Right mouse button click
                        print("Right mouse button")
            pygame.display.flip()
        if not RUNNING:
            self.quit()


    def game_setup(self):
        # Board initialization
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(random.choice(['X', ' ']))
            self.BOARD.append(row)

        # Number Clue initialization
        for row in self.BOARD:
            num = []
            i = 0
            for entry in row:
                if entry == 'X':
                    i += 1
                else:
                    if i != 0:
                        num.append(i)
                        i = 0
            if i != 0:
                num.append(i)
            self.ROW_NUMBERS.append(num)
        for col in range(self.width):
            num = []
            i = 0
            for row in range(self.height):
                if self.BOARD[row][col] == 'X':
                    i+=1
                else:
                    if i != 0:
                        num.append(i)
                        i = 0
            if i != 0:
                num.append(i)
            self.COLUMN_NUMBERS.append(num)
        # Placing numbers 
        for i in range(self.height):
            text = ""
            for n in self.ROW_NUMBERS[i]:
                text += str(n) + " "
            render_text = self.FONT.render(text, True, BLACK)
            self.screen.blit(render_text, (self.row_num_start_x, self.row_num_start_y + self.box_size * i))
        pygame.display.flip()
        
        for i in range(self.width):
            text = []
            vertical_text_render = []
            for n in self.COLUMN_NUMBERS[i]:
                text.append(str(n))
                vertical_text_render.append(self.FONT.render(str(n), True, BLACK))

            for j, line_surface in enumerate(vertical_text_render):
                self.screen.blit(line_surface, (self.column_num_start_x + self.box_size * i, self.column_num_start_y + j * 22))

    def screen_setup(self):
        self.screen.fill(BACKGROUND)
        for i in range(self.height):
            for j in range(self.width):
                cell = self.draw_cell((i, j))
                pygame.draw.rect(self.screen, GRAY, cell)
                pygame.draw.rect(self.screen, BLACK, cell, 1)

    def draw_cell(self, pos):
        return pygame.Rect(
            self.grid_start_x + pos[0] * self.box_size,
            self.grid_start_y + pos[1] * self.box_size,
            self.box_size,
            self.box_size
        )
    
if __name__ == "__main__":
    Nonogram(15, 15, 3)