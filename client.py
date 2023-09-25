import socket as skt
import threading

# Ask the user to choose a nickname for the chat.
nickname = input("Choose a nickname: ")

# Create a client socket using IPv4 and TCP socket.
client = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

# Connect the client socket to the server's IP address and port.
client.connect(('127.0.0.1', 55555))


# Function to receive messages from the server.
def receive():
    while True:
        try:
            # Receive a message from the server (up to 1024 bytes) and decode it as ASCII.
            message = client.recv(1024).decode('ascii')

            # Check if the server requests a nickname.
            if message == 'NICK':
                # Send the chosen nickname to the server encoded as ASCII.
                client.send(nickname.encode('ascii'))
            else:
                # Print the received message (chat messages from other clients).
                print(message)
        except:
            print("An error occurred...")
            client.close()
            break


# Function to write and send messages to the server.
def write():
    while True:
        # Prompt the user for input and create a message with their nickname.
        message = f'{nickname}: {input("")}'  # asks for the input

        # Send the message to the server encoded as ASCII.
        client.send(message.encode('ascii'))


# Create a thread to receive messages from the server.
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Create a thread to write and send messages to the server.
write_thread = threading.Thread(target=write)
write_thread.start()