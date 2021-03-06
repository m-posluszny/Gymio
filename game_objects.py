from numpy import e
from game import play

class GameRoom:
    
    def __init__(self,id,w,h):
        self.id = id
        self.players = {}
        self.size = [w,h]
        self.ball = [w/2,h/2]
        self.velocity=15
        self.slots = 2
        self.up=True
        self.right=True
    
    def send_packet(self):
        data={}
        data["ball"]=self.ball
        for key, player in self.players.items():
            data[player.name]={}
            data[player.name]["frame"]=player.frame
            data[player.name]["score"]=player.score
            data[player.name]["position"]=player.position
            data[player.name]["size"]=player.size 
        return data
    
    def add_player(self,name,ip):
        self.players[ip+name] = Player(name,ip)
        if len(self.players.keys()) <= self.slots/2:
            self.players[ip+name].set_pos(self.size[0]/2,self.size[1]-self.players[ip+name].size[1]/1.5)
        else:
            self.players[ip+name].set_pos(self.size[0]/2,0)
            
    def remove_player(self, player):
        self.players.pop(player.ip)
    
    def update_gameroom(self):
        for name,player in self.players.items():
            player.move_player(self.size)
        self.move_ball()
    
    def move_ball(self):
        for name, player in self.players.items():
            miny = player.position[1] - 10
            maxy = player.position[1] + player.size[1] + 10

            if(self.ball[0] > player.position[0] 
            and self.ball[0] < player.position[0] + player.size[0]
            and self.ball[1] > miny and self.ball[1] < maxy):
                self.up = not self.up
                self.right = not self.right

        if(self.ball[0] < 0 ):
            self.right = True
        
        if(self.ball[0] > self.size[0]):
            self.right = False
        
        if(self.ball[1] > self.size[1]):
            self.up = False
        
        if(self.ball[1] < 0):
            self.up = True

        if (self.up):
            self.ball[1]+=self.velocity
        else:
            self.ball[1]-=self.velocity

        if(self.right):
            self.ball[0]+=self.velocity
        else:
            self.ball[0]-=self.velocity

    
class Player:
    
    def __init__(self,name,ip):
        self.ip = ip
        self.name = name
        self.frame = ""
        self.score = 0
        self.velocity = 10
        self.position = [0,0]
        self.size = [320,240] #TODO
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
        w = self.size[0]
        pos = self.position[0]
        velo = self.velocity
        # print(f'{self.hand_pos[0]} left_val{w/2} right_val{(w/2)}')
        if (self.hand_pos[0] < (w/2) and pos - velo > 0):
            self.position[0]-=velo
        elif (self.hand_pos[0] > (w/2) and pos + velo + self.size[0] < max_size[0]):
            self.position[0]+=velo
         