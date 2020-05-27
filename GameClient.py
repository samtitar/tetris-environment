from TetrisEnv import StandaloneWrapper

import pickle
import socket
import sys
from threading import Thread

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.1.25', 9009)
print('connecting to {}:{}'.format(*server_address))
client.connect(server_address)

response = client.recv(2048)
game_data = pickle.loads(response)
game = StandaloneWrapper(**game_data)

while not response == b'START':
    response = client.recv(2048)

def connection():
    client.setblocking(False)

    while True:
        response = None
        lines, target = game.get_attack_data()
        print(target, lines)
        if len(lines) > 0:
            client.send(pickle.dumps({ 'target': target, 'lines': lines }))

        response = client.recv(2048)
        if response is not None:
            response = pickle.loads(response)
            game.set_junk_lines(response['lines'])

print('Starting Game')
thread = Thread(target=connection)
thread.start()
game.run()

client.close()