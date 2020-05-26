from TetrisEnv import StandaloneWrapper

import pickle
import socket
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9008)
print('connecting to {}:{}'.format(*server_address))
client.connect(server_address)

response = client.recv(2048)
game_data = pickle.loads(response)
game = StandaloneWrapper(**game_data)

while response is not 'START':
    response = client.recv(2048)

game.run()

while True:
    response = None
    target, lines = game.get_attack_data()
    if len(lines) > 0:
        client.send(pickle.dumps({ 'target': target, 'lines': lines }))

    response = client.recv(2048)
    if response is not None:
        response = pickle.loads(response)
        game.set_junk_lines(response['lines'])

client.close()

# while True:
#     try:
#         # Send data
#         message = b'This is the message.  It will be repeated.'
#         print('sending {!r}'.format(message))
#         sock.sendall(message)

#         # Look for the response
#         amount_received = 0
#         amount_expected = len(message)

#         while amount_received < amount_expected:
#             data = sock.recv(16)
#             amount_received += len(data)
#             print('received {!r}'.format(data))

#     finally:
#         print('closing socket')
#         sock.close()