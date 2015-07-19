# add path to the src and test directory
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
TEST_PATH = PARENT_PATH +"test/"
sys.path.append(SRC_PATH)
sys.path.append(TEST_PATH)

from unittest import TestCase
from nose.tools import *
import pdb
import sample_game

class TestSampleGame:

    def setup(self):
        self.G = sample_game.SampleGame()
    
    def teardown(self):
        pass

    def test_update(self):
        X,O,_ = -1,1,0
        ans = [
                [_,X,O,O,O,_,_],
                [_,_,O,X,X,_,_],
                [_,_,_,O,_,_,_],
                [_,_,_,X,_,_,_],
                [_,_,_,O,_,_,_],
                [_,_,_,X,_,_,_],
            ]
        def u(i):
            self.G.update(i)
        u(3);u(3);u(3);u(3);u(3);u(3);u(4);u(4);u(2);u(1);u(2)
        eq_(ans, self.G.table)

    def test_clone(self):
        def u(i):
            self.G.update(i)
        u(3);u(3);u(3);u(3);u(3);u(3);u(4);u(4);u(2);u(1);u(2)
        cp = self.G.clone()
        eq_(self.G.table, cp.table)
        eq_(self.G.position, cp.position)

    def test_is_legal(self):
        def u(i):
            self.G.update(i)
        u(3);u(3);u(3);u(3);u(3);u(3);u(4);u(4);u(2);u(1);u(2)
        ok_(not self.G.is_legal(3))
        ok_(self.G.is_legal(4))
    
    def test_is_terminal(self):
        def u(i):
            self.G.update(i)
        u(3);u(3);u(3);u(3);u(3);u(3);u(4);u(4);u(2);u(1)
        flg, score = self.G.is_terminal(5)
        ok_(flg)
        flg, score = self.G.is_terminal(0)
        ok_(not flg)

    def test_is_draw(self):
        def u(i):
            self.G.update(i)
        for i in range(6):
            for j in range(7):
                if i==5 and j==6:break
                u(j)
        ok_(self.G.is_draw(6))

    def test_getlegalmove(self):
        def u(i):
            self.G.update(i)
        u(3);u(3);u(3);u(3);u(3);u(3);u(4);u(4);u(2);u(1);u(2)
        for i in range(100):
            ok_(3!=self.G.get_legal_move())

    def test_simulation(self):
        for i in range(50):
            cp = self.G.clone()
            cp.simulation()
            flg = False
            for i in range(7):
                cp.position[i] = max(cp.position[i]-1, 0)
            cp.next_player = -cp.next_player
            for i in range(7):
                tmp,score = cp.is_terminal(i)
                flg |= tmp
            if i%10 == 0:
                cp.display()
            ok_(flg)
