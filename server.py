import socket
import threading

IP = "localhost"
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(4)

clients: set[socket.socket] = set()
clients_lock = threading.Lock()


def broadcast(message: str, sender: socket.socket | None = None) -> None:
    with clients_lock:
        snapshot = list(clients)
    for client in snapshot:
        if client != sender:
            client.send(message.encode())


def handle(client, address):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            message = data.decode()
            broadcast(f"{address}:{message}", client)
    except Exception:
        pass
    finally:
        with clients_lock:
            clients.discard(client)
        try:
            client.close()
        except OSError:
            pass
        broadcast(f"{address} left the chat.", client)
        print(f"{address} left the chat")


def main():
    print(f"server is running on port={PORT}")
    while True:
        client, address = server.accept()
        print(f"{address} joined the chat")
        broadcast(f"{address} joined the chat")
        with clients_lock:
            clients.add(client)
        thread = threading.Thread(target=handle, args=(client, address))
        thread.start()


if __name__ == "__main__":
    main()

