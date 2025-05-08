import socket
import threading

IP = 'localhost'
PORT = 1234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print('disconnected')
            client.close()
            break


def send():
    while True:
        message = input('>>')
        client.send(message.encode())

