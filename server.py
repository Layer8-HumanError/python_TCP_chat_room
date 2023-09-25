# A small program that uses our local host address as a server for clients to
# connect to over a TCP socket and partake in a chatroom.

import socket as skt
import threading

host = '127.0.0.1'  # Uses the localhost address of our machine.
port = 55555  # Ideally use a non-reserved port: 49152 - 65535

# Create a server socket using IPv4 and TCP socket.
server = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

# Bind the server with the host address and port.
server.bind((host, port))

# Start the server to listen for connections.
server.listen()

# Lists to store connected clients and their nicknames.
clients = []  # clients connected
nicknames = []  # nicknames assigned to connected clients


# Function to broadcast a message to all connected clients.
def broadcast(message):
    for client in clients:
        client.send(message)


# Function to handle a client's connection.
def handle(client):
    while True:
        try:
            # Receive a message from the client (up to 1024 bytes).
            message = client.recv(1024)

            # Broadcast the received message to all clients.
            broadcast(message)
        except:
            # If an exception occurs (client disconnects), remove the client from the list, close the connection,
            # and notify other clients about the client leaving.
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]

            broadcast(f'{nickname} left the chat.'.encode('ascii'))
            nicknames.remove(nickname)
            break


# Function to accept incoming client connections.
def receive():
    while True:
        # Accept a new client connection.
        client, address = server.accept()
        print(f"Connected with {str(address)}.")  # Admin knows which client connected

        # Request a nickname from the client.
        client.send('NICK'.encode('ascii'))

        # Receive and decode the client's chosen nickname.
        nickname = client.recv(1024).decode('ascii')

        # Add the client's nickname to the nicknames list.
        nicknames.append(nickname)

        # Add the client to the clients list.
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')

        # Broadcast to all clients that a new client joined.
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        # Send a welcome message to the newly connected client.
        client.send('Connected to the server!'.encode('ascii'))

        # Create a new thread to handle communication with this client.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()  # Start accepting client connections and handling them in separate threads.
