from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send, join_room, leave_room

# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__)
socketio = SocketIO(app)



@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})
    print('connected')
    
@socketio.on('camera_b64')
def handle_message(data):
    emit('camera_b64_resp',{'data':data})
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=5000)