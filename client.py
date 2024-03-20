import socketio
import pyreadline

# Initialize SocketIO client
sio = socketio.Client()
name = input("Enter your name: ")

# Connect to the server
@sio.event
def connect():
    print("Connected to chat server\n")
    # When connected, send the user's name to the server
    sio.emit('set_name', {'name': name})

@sio.on('client_id')
def receive_client_id(client_id):
    print(f"\033[1;32mJOINED: \033[0m:{client_id}\n")

@sio.on('names')
def receive_names(names):
    names_str = ' , '.join(map(str, names))
    #print(f"IN CHAT:\033[1;36m {names}\033[0m:")
    print(f"IN CHAT:\033[1;36m {names_str} \033[0m")

@sio.on('clients')
def receive_clients(clients):
    print(f"\033[1;35m Connected clients\033[0m: \033[1;31m : {clients}\033[0m:")

# Receive message from server
@sio.on('message')
def receive_message(data):
    sender = data['sender']
    message = data['message']
    print(f"\033[1;32m{sender}\033[0m: {message}\n")


# Start the client
def start_client():
    # Connect to the server
    sio.connect('http://localhost:5000')

    # Main loop to send messages
    while True:
        message = input( "")
        
        print('\033[1A\033[K')  # Move cursor up and clear the line
        print("\t\t\t\t\t\t\033[1;35m You:\033[0m", message)
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
