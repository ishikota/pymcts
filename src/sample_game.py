import copy
from game import Game
import random

class SampleGame(Game):
    """Sample game concrete class.

    Game concrete class to demonstrate MCTS module.
    This sample represents the game of ConnectFour.
    """

    def __init__(self):
        super(SampleGame, self).__init__(7)   # 7 is the WIDTH of board
        
        # ConnectFour Constants
        self.CONNECT_K = 4
        self.WIDTH = 7
        self.HEIGHT = 6
        self.P1 = 1
        self.P2 = -1
        
        # instance varialbes
        self.table = [[0 for j in range(self.WIDTH)] for i in range(self.HEIGHT)]
        self.position = [0 for i in range(self.WIDTH)]
        self.next_player = 1

    def clone(self):
        return copy.deepcopy(self)

    def update(self, node_index):
        col = node_index
        row = self.position[col]
        self.table[row][col] = self.next_player
        self.position[col] += 1
        self.next_player = -self.next_player

    def is_legal(self, node_index):
        return self.position[node_index] != self.HEIGHT

    def simulation(self):
        while True:
            action = self.get_legal_move()
            flg, score = self.is_terminal(action)
            self.update(action)
            if flg: return score

    def get_legal_move(self):
        return random.choice([col for col in range(7) if self.is_legal(col)])

    def is_terminal(self, node_index):
        if self.is_draw(node_index): return True, 0

        row = self.position[node_index]
        col = node_index
        line_nums = [1,1,1,1]
        di = [1,-1,0,0,-1,1,-1]
        dj = [1,-1,1,-1,1,-1,0]

        for d in range(7):
            line_num = 1
            ni, nj = row,col
            for k in range(self.CONNECT_K-1):
                ni += di[d]
                nj += dj[d]
                if not(0<=ni<self.HEIGHT) or not(0<=nj<self.WIDTH) \
                        or self.table[ni][nj] != self.next_player:
                    break
                line_nums[d/2] += 1
            if d%2==1 or d==6:
                if line_nums[d/2] >=self.CONNECT_K:
                    return True, 1
        return False, None

    def is_draw(self, node_index):
        for i in range(self.WIDTH):
            if i == node_index and self.position[i] != self.HEIGHT-1:
                return False
            if i != node_index and self.position[i] != self.HEIGHT:
                return False
        return True

    def display(self):
        char_map = {0:'-',1:'O',-1:'X'}
        # display table state to shell
        print 
        for row in reversed(range(self.HEIGHT)):
            line = '   '
            for col in range(self.WIDTH):
                line += char_map[self.table[row][col]]+' '
            print line
        line = '   '
        for i in range(self.WIDTH):
            line +=str(i+1)+' '
        print line
        print ''

