import socket

IP = 'localhost'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

clients: set[socket.socket] = set()


def broadcast(message: str) -> None:
    for client in clients:
        client.send(message.encode())
