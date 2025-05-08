import socket
import threading

IP = 'localhost'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

clients: set[socket.socket] = set()


def broadcast(message: str) -> None:
    for client in clients:
        client.send(message.encode())


def handle(client: socket.socket) -> None:
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(f'{client}:{message}')
        except:
            broadcast(f'{client} left the chat.')
            print(f'{client} left the chat')
            clients.remove(client)
            client.close()
            break


def main():
    print(f'server is running on port={PORT}')
    while True:
        client, address = server.accept()
        print(f'{client} joined the chat')
        broadcast(f'{client} joined the chat')
        clients.add(client)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == '__main__':
    main()
