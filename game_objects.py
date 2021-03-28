from numpy import e
from game import play


class GameRoom:
    
    def __init__(self,id,w,h):
        self.id = id
        self.players = {}
        self.size = [w,h]
        self.ball = [w/2,h/2]
        self.velocity=1
        self.up=True
        
    def add_player(self,name,ip):
        self.players[ip] = Player(name,ip)

    def remove_player(self, player):
        self.players.pop(player.ip)
    
    def update_gameroom(self):
        for name,player in self.players.items():
            player.move_player(self.size)
    
    def move_ball(self):
        if (self.up):
            self.ball[0]+=self.velocity
            self.ball[1]+=self.velocity
        
        else:
            self.ball[0]-=self.velocity
            self.ball[1]-=self.velocity
            
    
class Player:
    
    def __init__(self,name,ip):
        self.ip = ip
        self.name = name
        self.frame = ""
        self.score = 0
        self.velocity = 1
        self.position = [0,0]
        self.size = [200,200] #TODO
        self.hand_pos=[0,0]

    def set_frame(self,b64):
        self.frame = b64

    def set_pos(self,x,y):
        self.position = [x,y]
    
    def set_size(self,w,h):
        self.size = [w,h]
    
    def get_point(self):
        self.score+=1

    def calc_hand(self,x,y,w,h):
        self.hand_pos = [x+w/2, y+h/2]
        
    def move_player(self,max_size):
        w = max_size[0]
        pos = self.position[0]
        velo = self.velocity
        if (self.hand_pos[0] < (w/3) and pos-velo > 0):
            self.position[0]-=velo
        elif (self.hand_pos[0] > (2*w/3) and pos + velo < w):
            self.position[0]+=velo
         