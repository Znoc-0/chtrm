import socketio
import requests
# Initialize SocketIO client
sio = socketio.Client()

# Connect to the server
@sio.event
def connect():
    print("Connected to server")

@sio.on('client_id')
def receive_client_id(client_id):
    print(f"\033[1;32mJOINED: \033[0m:{client_id}\n")

@sio.on('names')
def receive_names(names):
    print(f"Connected names: {names}")

@sio.on('clients')
def receive_clients(clients):
    print(f"\033[1;35m Connected clients\033[0m: \033[1;31m : {clients}\033[0m:")

# Receive message from server
@sio.on('message')
def receive_message(data):
    sender = data['sender']
    message = data['message']
    print(f"\033[1;32m{sender}\033[0m: {message}")


# Start the client
def start_client():
    name = input("Enter your name: ")

    # Connect to the server
    sio.connect('http://localhost:5000')
   # payload={'name': name}
    # requests.get('http://localhost:5000/connect',params=payload)


    # Main loop to send messages
    while True:
        message = input( "->")

        if message.lower() == 'exit':
            break
        if message.lower() == 'get_clients':
            sio.emit('get_clients')
        elif message.strip():  # Check if the message is not empty
            sio.emit('message', {'sender': name, 'message': message})

    # Disconnect from the server
    sio.disconnect()

if __name__ == '__main__':
    start_client()
