import socket
import threading

IP = 'localhost'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

clients: set[socket.socket] = set()


def broadcast(message: str, sender: socket.socket | None = None) -> None:
    for client in clients:
        if client != sender:
            client.send(message.encode())


def handle(client: socket.socket, address) -> None:
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(f'{address}:{message}', client)
        except:
            broadcast(f'{address} left the chat.')
            print(f'{address} left the chat')
            clients.remove(client)
            client.close()
            break


def main():
    print(f'server is running on port={PORT}')
    while True:
        client, address = server.accept()
        print(f'{address} joined the chat')
        broadcast(f'{address} joined the chat')
        clients.add(client)
        thread = threading.Thread(target=handle, args=(client, address))
        thread.start()


if __name__ == '__main__':
    main()
