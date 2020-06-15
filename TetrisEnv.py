import pygame
import random
import os

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 600

PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30

TL_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TL_y = SCREEN_HEIGHT - PLAY_HEIGHT

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
    '''Create array grid given which positions are locked'''

    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
            # Set locked positions
                grid[i][j] = locked_pos[(j,i)]
    return grid

def convert_shape_format(shape):
    '''Convert shape array to grid positions (x,y)'''

    positions = []
    s_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(s_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    '''Check if shape is valid in grid'''

    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def get_shape():
    '''Get random piece'''

    return Piece(5, 0, random.choice(shapes))

def clear_rows(grid, locked, shape):
    '''Clear rows given grid, locked positions and fallen piece'''

    shape.sort(key=lambda x: (x[1], x[0]))

    x_gap = -1
    y_values = set()

    for x, y in shape:
        row = grid[y]
        if (0, 0, 0) not in row:
            y_values.add(y)
            if x_gap is -1:
                x_gap = x
    
    to_remove = []
    for x, y in locked.keys():
        if y in y_values:
            to_remove.append((x, y))
    
    for key in to_remove:
        del locked[key]
    
    for clear_y in y_values:
        for x, y in sorted(list(locked), key=lambda x: x[1])[::-1]:
            if y < clear_y:
                locked[(x, y + 1)] = locked.pop((x, y))

    return len(y_values), x_gap

def check_lost(positions):
    '''Check if player lost'''

    for _, y in positions:
        if y < 1:
            return True
    return False

def draw_next_shape(shape, surface):
    ''''Draw the next shape in queue'''

    sx = TL_X + PLAY_WIDTH + 10
    sy = TL_y + PLAY_HEIGHT/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_held_piece(shape, surface):
    '''Draw the held piece'''

    sx = TL_X - 160
    sy = TL_y + PLAY_HEIGHT/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_junk_line_queue(queue, surface):
    '''Draw the junk line queue next to the playing grid'''

    x = TL_X - (5 + BLOCK_SIZE)
    y = TL_y + (PLAY_HEIGHT - BLOCK_SIZE)

    for i, group in enumerate(queue):
        time = group['time']
        lines = group['lines']

        color = (128, 128, 128)
        if i is 0:
            color = (255, 165, 0)
            if time < 2000:
                color = (255, 0, 0)

        for line in lines:
            pygame.draw.rect(surface, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 0)
            y -= 5 + BLOCK_SIZE

def draw_window(grid, surface):
    surface.fill((0, 0, 0))

    sx = TL_X + PLAY_WIDTH + 50
    sy = TL_y + PLAY_HEIGHT/2 - 100

    sx = TL_X - 200
    sy = TL_y + 200

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TL_X + j*BLOCK_SIZE, TL_y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.draw.rect(surface, (255, 0, 0), (TL_X, TL_y, PLAY_WIDTH, PLAY_HEIGHT), 5)

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

class SingleplayerEnvironment(object):
    def __init__(self, id, seed, game_size, init_screen=True):
        random.seed(seed)
        self._seed = seed

        # Setup environment
        self._id = id
        self._score = 0
        self._action_queue = []
        self._game_size = game_size

        if init_screen:
            self._screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), 32)

        # Setup game states
        self._clock = pygame.time.Clock()
        self._change_piece = False
        self._can_hold = True
        self._alive = True

        # Setup game space
        self._locked_positions = {}
        self._grid = create_grid(self._locked_positions)
        self._current_piece = get_shape()
        self._next_piece = get_shape()
        self._held_piece = None

        # Setup attack states
        self._target = 1 if id is 0 else 0
        self._send_lines = []
        self._junk_lines_queue = []

        # Setup game data
        self._pieces = 0
        self._frame = 0
        self._fall_time = 0
        self._fall_speed = 0.27
        self._level_time = 0
    
    def step(self, action):
        self._action_queue.append(action)
    
    def is_alive(self):
        return self._alive
    
    def get_attack_data(self):
        lines = self._send_lines
        self._send_lines = []
        return lines, self._target
    
    def set_junk_lines(self, lines):
        if len(lines) > 0:
            self._junk_lines_queue.append({'time': 4000, 'lines': lines})
    
    def next_piece(self):
        self._current_piece = self._next_piece
        random.seed(self._seed)
        self._seed += 1
        self._next_piece = get_shape()
        self._pieces += 1
    
    def render(self):
        draw_window(self._grid, self._screen)
        draw_junk_line_queue(self._junk_lines_queue, self._screen)
        draw_next_shape(self._next_piece, self._screen)
        if self._held_piece:
            draw_held_piece(self._held_piece, self._screen)
        pygame.display.update()
    
    def get_frame(self):
        return pygame.surfarray.array3d(self._screen)
    
    def tick(self):
        # Update grid and game data
        self._grid = create_grid(self._locked_positions)

        passed_time = self._clock.get_rawtime()
        self._fall_time += passed_time
        self._level_time += passed_time
        self._clock.tick()

        if len(self._junk_lines_queue) > 0:
            self._junk_lines_queue[0]['time'] -= passed_time

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
        if len(self._action_queue) > 0:
            action = self._action_queue[0]
            # Move left
            if action == 0:
                self._current_piece.x -= 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.x += 1
            # Move right
            elif action == 1:
                self._current_piece.x += 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.x -= 1
            # Move down
            elif action == 2:
                self._current_piece.y += 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.y -= 1
            # Fast drop
            elif action == 3:
                while valid_space(self._current_piece, self._grid):
                    self._current_piece.y += 1
                    self._change_piece = True
                self._current_piece.y -= 1
            # Rotate left
            elif action == 4:
                self._current_piece.rotation += 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.rotation -= 1
            # Rotate right
            elif action == 5:
                self._current_piece.rotation -= 1
                if not(valid_space(self._current_piece, self._grid)):
                    self._current_piece.rotation += 1
            # Hold
            elif action == 6 and self._can_hold:
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

        # Add new current piece position to grid
        shape_pos = convert_shape_format(self._current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                self._grid[y][x] = self._current_piece.color
        
        # Current piece has hit bottom
        if self._change_piece:
            for pos in shape_pos:
                self._locked_positions[pos] = self._current_piece.color
            cleared, x_gap = clear_rows(self._grid, self._locked_positions, shape_pos)

            # Remove from junkline queue
            junk_lines_removed = 0
            for i, group in enumerate(self._junk_lines_queue):
                time = group['time']
                lines = group['lines']

                for line in lines:
                    self._junk_lines_queue[i]['lines'].remove(line)
                    if len (self._junk_lines_queue[i]['lines']) < 1:
                        del self._junk_lines_queue[i]
                    junk_lines_removed += 1

                    if junk_lines_removed > cleared - 1:
                        break
                if junk_lines_removed > cleared - 1:
                    break
            self._send_lines = [x_gap] * (cleared - junk_lines_removed)

            # Handle junk lines
            if len(self._junk_lines_queue) > 0:
                time = self._junk_lines_queue[0]['time']
                lines = self.set_junk_lines[0]['lines']

                if time < 1:
                    new_locked_pos = {}
                    n_lines = len(lines)

                    # Move all blocks up
                    for x, y in self._locked_positions.keys():
                        new_locked_pos[(x, y-n_lines)] = self._locked_positions[(x, y)]

                    # Add junk lines to grid
                    for i, line in enumerate(lines):
                        for x in range(10):
                            if x is not line:
                                new_locked_pos[(x, 20 - (i + 1))] = (255, 255, 255)
                    self._locked_positions = new_locked_pos
                    del self._junk_lines_queue[0]

            # Update game states
            self._change_piece = False
            self._can_hold = True
            self.next_piece()

        if check_lost(self._locked_positions):
            self._alive = False
        self._frame += 1

class MultiplayerEnvironment():
    def __init__(self, num_games=99):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        self._games = [SingleplayerEnvironment(n, 3210, num_games) for n in range(num_games)]
    
    def start(self):
        pygame.display.set_mode((1,1))

        run, frame_n = 0, True
        while len(self._games) > 0 and run:
            for i, game in enumerate(self._games):
                if not game.is_alive():
                    self._games.remove(game)

                game.tick()
                game.render()

                frame = game.get_frame()[::-1]
            frame_n += 1