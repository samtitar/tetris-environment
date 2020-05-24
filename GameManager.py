import pygame
import random
import os
import matplotlib.pyplot as plt
import numpy as np

from TetrisEnv import Game, get_shape

class Manager():
    def __init__(self, num_games=99):
        self._games = [Game(n, 3210) for n in range(num_games)]
    
    def start(self):
        pygame.display.set_mode((1,1))

        fig = plt.figure()

        run = True
        frame_n = 0
        while len(self._games) > 0:
            for i, game in enumerate(self._games):
                if not game.is_alive():
                    self._games.remove(game)

                game.set_junk_lines([1, 2, 3])
                game.tick()
                game.render()

                frame = game.get_frame()[::-1]
            frame_n += 1

os.environ['SDL_VIDEODRIVER'] = 'dummy'
manager = Manager(num_games=1)
manager.start()