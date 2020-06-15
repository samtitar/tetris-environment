from TetrisEnv import SingleplayerEnvironment
from threading import Thread
from pathlib import Path

import pygame
import pickle
import socket
import sys

class StandaloneWrapper(SingleplayerEnvironment):
    def __init__(self, id, seed, game_size, debug=False):
        # Initialize game and screen
        super(StandaloneWrapper, self).__init__(id, seed, game_size, init_screen=False)
        self._screen = pygame.display.set_mode((650, 600))
        self._directory = 'debug/game/{}'.format(id)
        self._debug = debug

        if debug:
            Path(self._directory).mkdir(parents=True, exist_ok=True)
    
    def run(self):
        frame_n = 0

        # Update loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.step(0)
                    if event.key == pygame.K_d:
                        self.step(1)
                    if event.key == pygame.K_s:
                        self.step(2)
                    if event.key == pygame.K_w:
                        self.step(3)
                    if event.key == pygame.K_q:
                        self.step(4)
                    if event.key == pygame.K_e:
                        self.step(5)
                    if event.key == pygame.K_SPACE:
                        self.step(6)
            
            self.render()
            self.tick()

            lines, _ = self.get_attack_data()
            self.set_junk_lines(lines)

            if not self.is_alive():
                break

            if self._debug:
                im_path = self._directory + '/' + str(frame_n) + '.jpg'
                pygame.image.save(self._screen, im_path)
            frame_n += 1

class MultiplayerWrapper(StandaloneWrapper):
    def __init__(self, address, port):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        server_address = (address, port)
        print('connecting to {}:{}'.format(*server_address))
        self._client.connect(server_address)

        # Initialize game with game data from server
        response = self._client.recv(2048)
        self._game_data = pickle.loads(response)
        self._game = StandaloneWrapper(**self._game_data)

        # Wait for the game to start
        while not response == b'START':
            response = self._client.recv(2048)
        print('Starting Game')

        # Start threads for communication with the server
        in_thread = Thread(target=self.in_connection)
        out_thread = Thread(target=self.out_connection)

        in_thread.start()
        out_thread.start()

        # Run game and close connection when game is finished
        self._game.run()
        self._client.close()

    def in_connection(self):
        # Keep listening for messages from server
        while True:
            response = self._client.recv(2048)
            if response is not None:
                response = pickle.loads(response)
                self._game.set_junk_lines(response['lines'])

    def out_connection(self):
        # Send data to server when needed
        while True:
            lines, target = self._game.get_attack_data()
            if len(lines) > 0:
                self._client.send(pickle.dumps({ 'target': target, 'lines': lines }))

if __name__ == '__main__':
    singleplayer_game = StandaloneWrapper(0, 1, 1)
    singleplayer_game.run()
    # multiplayer_game = MultiplayerWrapper('192.168.1.25', 9008)