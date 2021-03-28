from gevent import monkey
monkey.patch_all()
 
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, disconnect
 
 def background_stuff():
     """ python code in main.py """
     print 'In background_stuff'
     while True:
         time.sleep(1)
         t = str(time.clock())
         socketio.emit('message', {'data': 'This is data', 'time': t}, namespace='/test')

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_stuff)
        thread.start()
    return render_template('index.html')

 
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None