from game import play
from flask import Flask, render_template, request, jsonify, session
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
    while True:
        game = game_rooms[room_id]
        game.update_gameroom()
        emit('game_state',game.send_packet(),room=room_id)
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
    
@app.route('//room//<room_name>', methods=['GET'])
def go_to_room(room_name):
    name = request.args.get("user")
    if name:
        return render_template('game.html')
    else:
        return render_template('join.html')

        

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
    
@socketio.on('camera_b64')
def handle_camera(data):
    ip = request.remote_addr
    player = game_rooms[data["room"]].players[ip+data["name"]]
    player.set_frame(data["data"])
    data = video_proc.process_image(frame = data["data"])
    if data:
        print(data)
        player.calc_hand(*data)

    
@socketio.on('create_game') 
def on_create_game(data):
    player_id = data["player_name"]
    room_id = data["id"]
    create_room = False
    ip = request.remote_addr
    if room_id not in game_rooms:
        game_rooms[room_id] = GameRoom(room_id,1200,700)
        create_room = not create_room
    game_rooms[room_id].add_player(player_id,ip)
    join_room(room_id)
    emit("user_handshake")
    emit("joined",{"name":player_id,"room":game_rooms[room_id].send_packet()}, room=room_id)
    if create_room:
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
