import pygame
import random

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                grid[i][j] = locked_pos[(j,i)]
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def clear_rows(grid, locked, shape):
    inc = 0
    for x, y in shape:
        row = grid[y]
        if (0, 0, 0) not in row:
            


    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

def draw_next_shape(shape, surface):
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

def draw_held_piece(shape, surface):
    sx = top_left_x - 200
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

def draw_chunk_line_queue(queue, surface):
    x = top_left_x - (5 + block_size)
    y = top_left_y + (play_height - block_size)

    for i, lines in enumerate(queue):
        color = (128, 128, 128)
        if i is 0:
            color = (255, 0, 0)
        elif i is 1:
            color = (255, 165, 0)

        for line in lines:
            pygame.draw.rect(surface, color, (x, y, block_size, block_size), 0)
            y -= 5 + block_size

def draw_window(grid, surface):
    surface.fill((0, 0, 0))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    sx = top_left_x - 200
    sy = top_left_y + 200

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


class Game(object):
    def __init__(self, id, seed):
        random.seed(seed)
        self._seed = seed

        # Setup environment
        self._id = id
        self._score = 0
        self._action_queue = []
        self._screen = pygame.Surface((800, 800), 32)

        # Setup game space
        self._clock = pygame.time.Clock()
        self._alive = True
        self._next_piece = None
        self._held_piece = None
        self._send_lines = []
        self._junk_lines_queue = []

        self._locked_positions = {}
        self._grid = create_grid(self._locked_positions)

        self._change_piece = False
        self._can_hold = True

        self._current_piece = get_shape()
        self._next_piece = get_shape()
        self._held_piece = None

        self._pieces = 0
        self._frame = 0
        self._fall_time = 0
        self._fall_speed = 0.27
        self._level_time = 0
    
    def step(self, action):
        self._action_queue.append(action)
    
    def is_alive(self):
        return self._alive
    
    def get_data(self):
        return self._grid, self._next_piece, self._held_piece
    
    def get_attack_data(self):
        result = self._send_lines
        self._send_lines = []
        return result
    
    def set_junk_lines(self, lines):
        self._junk_lines_queue.extend([lines])
    
    def next_piece(self):
        self._current_piece = self._next_piece
        random.seed(self._seed)
        self._seed += 1
        self._next_piece = get_shape()
        self._pieces += 1
    
    def render(self):
        draw_window(self._grid, self._screen)
        draw_chunk_line_queue(self._junk_lines_queue, self._screen)
        draw_next_shape(self._next_piece, self._screen)
        if self._held_piece:
            draw_held_piece(self._held_piece, self._screen)
        pygame.display.update()
        # pygame.image.save(self._screen, 'games/{}/{}'.format(self._id, self._frame))
    
    def get_frame(self):
        return pygame.surfarray.array3d(self._screen)
    
    def tick(self):
        self._grid = create_grid(self._locked_positions)
        self._fall_time += self._clock.get_rawtime()
        self._level_time += self._clock.get_rawtime()
        self._clock.tick()

        if self._level_time / 1000 > 5:
            self._level_time = 0
            if self._level_time > 0.12:
                self._level_time -= 0.005

        if self._fall_time / 1000 > self._fall_speed:
            self._fall_time = 0
            self._current_piece.y += 1

            # Current piece is at bottom
            if not(valid_space(self._current_piece, self._grid)) and self._current_piece.y > 0:
                self._current_piece.y -= 1
                self._change_piece = True
        
        # Handle actions
        for action in self._action_queue:
            # Move left
            if action == 0:
                self._current_piece.x -= 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.x += 1
            # Move right
            if action == 1:
                self._current_piece.x += 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.x -= 1
            # Move down
            if action == 2:
                self._current_piece.y += 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.y -= 1
            # Rotate left
            if action == 3:
                self._current_piece.rotation += 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.rotation -= 1
            # Rotate right
            if action == 4:
                self._current_piece.rotation -= 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.rotation += 1
            # Hold
            if action == 5 and self._can_hold:
                new_held_piece = self._current_piece
                if self._held_piece:
                    self._current_piece = self._held_piece
                else:
                    self.next_piece()
                self._held_piece = new_held_piece
                self._current_piece.x = 5
                self._current_piece.y = 0
                self._can_hold = False
            self._action_queue.remove(action)
        shape_pos = convert_shape_format(self._current_piece)

        # Add new current piece position to grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                self._grid[y][x] = self._current_piece.color
        
        # Current piece has hit bottom
        if self._change_piece:
            clear_rows(self._grid, self._locked_positions, shape_pos)

            # Add piece to locked pieces
            for pos in shape_pos:
                # TODO: Easy fix
                p = (pos[0], pos[1])
                self._locked_positions[p] = self._current_piece.color

            # Add junk lines to grid
            new_locked_pos = {}
            junk_lines = self._junk_lines_queue[0]
            n_lines = len(junk_lines)

            for x, y in self._locked_positions.keys():
                new_locked_pos[(x, y-n_lines)] = self._locked_positions[(x, y)]

            for i, line in enumerate(junk_lines):
                for x in range(10):
                    if x is not line:
                        new_locked_pos[(x, 20-(i + 1))] = (255, 255, 255)
            self._locked_positions = new_locked_pos
            self._junk_lines_queue.remove(junk_lines)

            # Update game states
            self._change_piece = False
            self._can_hold = True
            self.next_piece()

        if check_lost(self._locked_positions):
            self._alive = False
        self._frame += 1