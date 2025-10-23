import random
import os
import pygame
import sys

GAME_PATH = os.path.dirname(__file__)
ASSET_FILE = os.path.join(GAME_PATH, 'assets')
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
        self.BLACK_BOX = set()
        self.X_BOX = set()
        self.CLICKED_BOX = set()
        self.box_size = 30
        self.allow_click = True
        self.grid_start_x = 50
        self.grid_start_y = 50
        self.row_num_start_x = self.grid_start_x + 10 + self.height * self.box_size
        self.row_num_start_y = 50
        self.column_num_start_x = self.grid_start_x + 5
        self.column_num_start_y = self.grid_start_y + 10 + self.width * self.box_size
        self.WINDOW_HEIGHT = max(700, self.height * self.box_size + 300)
        self.WINDOW_WIDTH = max(700, self.width * self.box_size + 300)
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.sprite_x = pygame.image.load(os.path.join(ASSET_FILE, 'x.png')).convert_alpha()
        self.sprite_x = pygame.transform.scale(self.sprite_x, (self.box_size, self.box_size))
        pygame.init()
        pygame.font.init()
        self.FONT = pygame.font.SysFont("Arial", 20)
        pygame.display.set_caption(WINDOW_TITLE)
        RUNNING = True
        
        self.screen_setup()
        self.game_setup()
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.allow_click: # Mouse click detected
                    box_position = self.get_position(event.pos)
                    if event.button == 1: # Left mouse button click
                        self.place_x_box(box_position)
                    elif event.button == 3: # Right mouse button click
                        self.place_black_box(box_position)
            pygame.display.flip()
            if self.win():
                print("You win!")
                self.game_won()
            if self.LIVES == 0:
                self.game_over()
        if not RUNNING:
            self.quit()
    
    def game_setup(self):
        # Board initialization
        for i in range(self.height):
            row = []
            weight = random.random()
            for j in range(self.width):
                entry = random.choices(['X', ' '], weights=[weight, 1 - weight])[0]
                row.append(entry)
                if entry == 'X':
                    self.X_BOX.add((i,j))
                else:
                    self.BLACK_BOX.add((i,j))
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
        for i in range(self.width):
            text = ""
            for n in self.COLUMN_NUMBERS[i]:
                text += str(n) + "  "
            render_text = self.FONT.render(text, True, BLACK)
            self.screen.blit(render_text, (self.row_num_start_x, self.row_num_start_y + self.box_size * i))
        pygame.display.flip()
        
        for i in range(self.height):
            text = []
            vertical_text_render = []
            for n in self.ROW_NUMBERS[i]:
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
        self.update_lives(0)

    def win(self):
        return len(self.CLICKED_BOX) == self.width * self.height

    def game_over(self):
        self.allow_click = False
        text_rect = pygame.Rect(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2,0, 0)
        pygame.draw.rect(self.screen, WHITE, text_rect)
        text_render = pygame.font.SysFont("Arial", 100).render("YOU LOSE", True, (255, 0, 0)) # A big red text only used once.
        text_surface = text_render.get_rect(center=text_rect.center)
        self.screen.blit(text_render, text_surface)

    def game_won(self):
        self.allow_click = False
        text_rect = pygame.Rect(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2,0, 0)
        pygame.draw.rect(self.screen, WHITE, text_rect)
        text_render = pygame.font.SysFont("Arial", 100).render("YOU WIN", True, (0, 50, 255))
        text_surface = text_render.get_rect(center=text_rect.center)
        self.screen.blit(text_render, text_surface)

    def draw_cell(self, pos):
        return pygame.Rect(
            self.grid_start_x + pos[0] * self.box_size,
            self.grid_start_y + pos[1] * self.box_size,
            self.box_size,
            self.box_size
        )
    
    def update_lives(self, amount):
        self.LIVES += amount
        text = f"Lives: {self.LIVES}"
        text_rect = pygame.Rect(self.WINDOW_WIDTH - 70, self.WINDOW_HEIGHT- 70, 70, 70)
        pygame.draw.rect(self.screen, WHITE, text_rect)
        text_render = self.FONT.render(text, True, BLACK)
        text_surface = text_render.get_rect(center=text_rect.center)
        self.screen.blit(text_render, text_surface)

    def place_x_box(self, pos):
        if not pos:
            return
        if pos in self.CLICKED_BOX:
            return
        x, y = pos
        if pos in self.X_BOX:
            self.screen.blit(self.sprite_x, (self.grid_start_x + x * self.box_size, self.grid_start_y + y * self.box_size))
            pygame.display.flip()
        else:
            self.place_black_box(pos)
            self.update_lives(-1)
        self.CLICKED_BOX.add(pos)
    
    def place_black_box(self, pos):
        if not pos:
            return
        if pos in self.CLICKED_BOX:
            return
        x, y = pos
        if pos in self.BLACK_BOX:
            clicked_box = self.draw_cell(pos)
            pygame.draw.rect(self.screen, BLACK, clicked_box)
            pygame.display.flip()
        else:
            self.place_x_box(pos)
            self.update_lives(-1)
        self.CLICKED_BOX.add(pos)

    def get_position(self, click_pos):
        x,y  = click_pos
        if self.grid_start_x <= x <= self.grid_start_x + self.box_size * self.width and self.grid_start_y <= y <= self.grid_start_y + self.box_size * self.height:
            x = (x - self.grid_start_x) // self.box_size 
            y = (y - self.grid_start_y) // self.box_size 
            return (x, y)
        return None
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        Nonogram(15, 15, 3) # The default configuration for a Nonogram game is 15x15 with 3 lives
    elif len(sys.argv) == 4:
        Nonogram(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
    else:
        print("Invalid arguments")