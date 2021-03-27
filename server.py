from flask import Flask, render_template
from flask_socketio import SocketIO, emit,  join_room, leave_room

# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__)
socketio = SocketIO(app)



@socketio.on('join')
def on_join(data):
    username = data['username']
    channel = data['channel']
    join_room(channel)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})
    print('connected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=5000)