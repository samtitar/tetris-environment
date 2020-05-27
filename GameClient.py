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

def in_connection():
    while True:
        response = client.recv(2048)
        if response is not None:
            response = pickle.loads(response)
            game.set_junk_lines(response['lines'])


def out_connection():
    while True:
        lines, target = game.get_attack_data()
        if len(lines) > 0:
            client.send(pickle.dumps({ 'target': target, 'lines': lines }))

print('Starting Game')
in_thread = Thread(target=in_connection)
in_thread.start()

out_thread = Thread(target=out_connection)
out_thread.start()
game.run()

client.close()