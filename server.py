from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

connected_clients = set()  # Keep track of connected clients

@socketio.on('connect')
def handle_connect():
    client_id = request.sid  # Get the unique ID of the connected client
    connected_clients.add(client_id)
    
    print(f"Client connected: {client_id}")
    emit('client_id', client_id,broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    connected_clients.remove(client_id)
    print(f"Client disconnected: {client_id}")

@socketio.on('message')
def handle_message(data):
    sender_id = request.sid
    message = data['message']
    name = data['sender']
    print(f"Received message from {name}: {message}")

    # Broadcast the message to all connected clients
    emit('message', {'sender': name, 'message': message}, broadcast=True)

@socketio.on('get_clients')
def handle_get_clients():
    emit('clients', list(connected_clients))
    
if __name__ == '__main__':
    socketio.run(app, debug=False,allow_unsafe_werkzeug=True)
