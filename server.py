from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

connected_clients = {}  # Dictionary to store connected clients and their names

@socketio.on('connect')
def handle_connect():
    client_id = request.sid  # Get the unique ID of the connected client
    connected_clients[client_id] = None  # Add the client to the dictionary with no name initially
    
    print(f"Client connected: {client_id}")

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in connected_clients:
        name = connected_clients[client_id]  # Get the name of the disconnecting client
        del connected_clients[client_id]  # Remove the client from the dictionary
        print(f"Client disconnected: {client_id}")
        if name:
            emit('message', {'sender': 'Server', 'message': f'{name} has left the chat.'}, broadcast=True)

@socketio.on('set_name')
def handle_set_name(data):
    client_id = request.sid
    name = data['name']
    if client_id in connected_clients:
        connected_clients[client_id] = name  # Set the name for the client
        emit('names', list(connected_clients.values()))  # Emit the updated list of names to all clients
        emit('message', {'sender': 'Server', 'message': f'{name} has joined the chat.'}, broadcast=True, include_self=False)  # Send a message to all clients except the new one

@socketio.on('message')
def handle_message(data):
    sender_id = request.sid
    message = data['message']
    name = connected_clients.get(sender_id, "Unknown")  # Get the name of the sender
    print(f"Received message from {name}: {message}")

    # Broadcast the message to all connected clients
    emit('message', {'sender': name, 'message': message}, broadcast=True,include_self=False)

@socketio.on('get_clients')
def handle_get_clients():
    emit('clients', list(connected_clients.values()))

if __name__ == '__main__':
    socketio.run(app, debug=True)
