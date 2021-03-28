from game import play
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, namespace, send, join_room, leave_room, rooms
from game_objects import GameRoom, Player
from backend.video_proc import VideoProc
from threading import Thread
import sys
import signal
import asyncio
import json


# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__)
video_proc = VideoProc(size=200, confidence=0.25, hand_count=1)
socketio = SocketIO(app)
game_rooms = {}
threads=[]
FRAME_RATE = 24
def handler(signal, frame):
  print('CTRL-C pressed!')
  sys.exit(0)

def start_interval(room_id):
    print("start",room_id)
    # global thread
    # thread = Thread(target=game_interval,args=(room_id,))
    game_interval(room_id)
    
def game_interval(room_id,*args,**kwargs):
    print(rooms())
    while True:
        game = game_rooms[room_id]
        game.update_gameroom()
        
        emit('game_state',dir(game),room=room_id)
        socketio.sleep(1/FRAME_RATE)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room,namespace=room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
    
@app.route('//room//<room_name>')
def go_to_room(room_name):
    return render_template('game.html')
        

@app.route('//join//<room_name>')
def game_view(room_name):
    #TODO PRZEKAZAC ID ROOMU DO HTMLA
    if room_name in game_rooms:
         return render_template('join.html')
    else:
         return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})
    print('connected')
    
@socketio.on('camera_b64')
def handle_camera(data):
    ip = request.remote_addr
    emit('camera_b64_resp',{'data':data})
    print('b64',rooms())
    # player = game_rooms[rooms()[-1]].players[ip]
    # player.set_frame(data)
    # x,y,w,h = video_proc.process_image(frame = data)
    # player.calc_hand(x,y,w,h)

    
@socketio.on('create_game') 
def on_create_game(data):
    print(data)
    room_id = data["id"]
    player_id = data["player_name"]
    ip = request.remote_addr
    game_rooms[room_id] = GameRoom(room_id,800,800)
    game_rooms[room_id].add_player(player_id,ip)
    join_room(room_id)
    print(rooms())
    
    emit("joined", room=room_id)
    start_interval(room_id)
    
    
@socketio.on('join_game') 
def on_join_game(data):
    room_id = data["id"]
    ip = request.remote_addr
    player_id = data["player_name"]
    game_rooms[room_id].add_player(player_id,ip)
    join_room(room_id)

def emit_game_state(room, game):
    socketio.emit('game_state',dir(game))

    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=5000)
    
signal.signal(signal.SIGINT, handler)
signal.pause()
