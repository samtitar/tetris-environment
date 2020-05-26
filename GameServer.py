import random
import socket
import pickle
from threading import Thread

GAME_SIZE = 2
GAME_SEED = random.random()
clients = []

def handle_client(connection, address, client_id):
    connection.send(pickle.dumps({
        'id': client_id,
        'seed': GAME_SEED,
        'game_size': GAME_SIZE
    }))

    while True:
        try:
            attack_data = connection.recv(2048)

            if attack_data:
                attack_data = pickle.loads(attack_data)
                target = clients[attack_data['target']]
                target.send(pickle.dumps(attack_data))
            else:
                if connection in clients:
                    clients.remove(connection)
                    connection.close()
                    break
        except:
            continue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 9008)
print('Starting server on {}:{}'.format(*server_address))
server.bind(server_address)

server.listen(2)

while True:
    connection, client_address = server.accept()
    print('Client connected')
    clients.append(connection)

    client_id = len(clients)
    thread = Thread(target=handle_client(connection, client_address, client_id))
    thread.start()

    if len(clients) > 0:
        for client in clients:
            client.send('START')
server.close()