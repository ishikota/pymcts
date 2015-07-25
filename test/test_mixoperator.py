# add path to the src and test directory
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
TEST_PATH = PARENT_PATH +"test/"
sys.path.append(SRC_PATH+"algorithm")
sys.path.append(SRC_PATH+"algorithm/enhancements")
sys.path.append(SRC_PATH+"examples/connectfour")
sys.path.append(TEST_PATH)
sys.path.append(PARENT_PATH+"performance/accuracy/testset")

from unittest import TestCase
from nose.tools import *
import mcts
import pdb
import connectfour_model
from node import Node
import math
import reader
import mix_operator

class TestMCTS(TestCase):

    def setUp(self):
        self.M = mix_operator.MCTS()
        self.G = connectfour_model.ConnectFour()
    
    def tearDown(self):
        pass


    def test_calc_node_score(self):
        root = Node(7)
        root.val = 50
        root.update = 1350
        
        v0 = Node(7)
        v0.val = 80+90+100/3
        v0.update = 1380
        v0.parent = root

        # child num < 2 case
        child = Node(7)
        child.val, child.update = 50,100
        v0.children[0] = child

        # mean operator case
        eq_(1.0*v0.val/v0.update, self.M.calc_node_score(v0,0))

        data =[ (80,450), (90,400), (100, 500)]
        for i in range(3):
            child = Node(7)
            child.val, child.update = data[i]
            child.parent = v0
            v0.children[i] = child
        
        # max operator case
        eq_(100/500.0, self.M.calc_node_score(v0,0))


        data =[ (80,450), (90,400), (100, 400)]
        for i in range(3):
            child = Node(7)
            child.val, child.update = data[i]
            child.parent = v0
            v0.children[i] = child

        # mean operator case
        eq_(1.0*v0.val/v0.update, self.M.calc_node_score(v0,0))
        
