# add path to the src and test directory
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
TEST_PATH = PARENT_PATH +"test/"
sys.path.append(SRC_PATH+"algorithm")
sys.path.append(SRC_PATH+"examples/connectfour")
sys.path.append(TEST_PATH)
sys.path.append(PARENT_PATH+"performance/accuracy/testset")

from unittest import TestCase
from nose.tools import *
import mcts
import pdb
import connectfour_model
from node import Node
import time
import math
import reader

class TestMCTS(TestCase):

    def setUp(self):
        self.M = mcts.MCTS()
        self.G = connectfour_model.ConnectFour()
    
    def tearDown(self):
        pass

    def test_main_routine(self):
        model = self.G
        r = reader.Reader()
        f_name = PARENT_PATH+"performance/accuracy/testset/sample.in"
        ans, model, next_player = r.read_board(f_name, model)
        self.M.set_playout(2000)
        root, act = self.M.start(model)
        eq_(6,act)
        f_name = PARENT_PATH+"performance/accuracy/testset/5-step-read.in"
        ans, model, next_player = r.read_board(f_name, model)
        self.M.set_playout(2000)
        root, act = self.M.start(model)
        ok_(0==act or 1==act)

    def test_budget_type(self):
        self.M.set_budget(self.M.PLAYOUT)
        self.M.set_limit(250)
        root, act = self.M.start(self.G)
        ok_(250, root.update)
        self.M.set_budget(self.M.TIME)
        self.M.set_limit(3)
        st = time.time()
        self.M.start(self.G)
        et = time.time()
        ok_(3<= et -st <= 3.1)

    def test_tree_policy(self):
        data = [(31.16,105),(52.89,153),(113.05,285),
                (6.87,44),(100.89,259),(16.5,70),(22.05,84)]
        v0 = Node(7)
        v0.update= 1000
        for i in range(7):
            child = Node(7)
            child.val, child.update = data[i]
            child.parent = v0
            v0.children[i] = child
        v0.unvisited = 0
        v_l = self.M.tree_policy(v0, self.G)
        eq_(v0.children[1], v_l.parent)    # best child is children[1]

    """
       - - - X - - - 
       - - - O - - - 
       - - - X - - - 
       - - - O - - - 
       - X O X X - - 
       - X O O O - - 
       1 2 3 4 5 6 7 
    """
    def testExpand(self):
        def u(i):
            self.G.update(i)
        u(3);u(3);u(3);u(3);u(3);u(3);u(4);u(4);u(2);u(1);u(2);u(1)
        
        p = Node(7)
        self.M.ME = self.G.next_player
        for i in range(6):
            self.M.expand(p, self.G)
        eq_(p.unvisited,0)
        for i in range(7):
            if i==5:
                ok_(p.children[i].is_terminal)
                eq_(1,p.children[i].val)
            elif i!=3:
                ok_(not p.children[i].is_terminal)
                eq_(0,p.children[i].val)

    def test_best_child(self):
        data = [(31.16,105),(52.89,153),(113.05,285),
                (6.87,44),(100.89,259),(16.5,70),(22.05,84)]
        v0 = Node(7)
        v0.update= 1000
        for i in range(7):
            child = Node(7)
            child.val, child.update = data[i]
            child.parent = v0
            v0.children[i] = child
        eq_(2,self.M.best_child(v0, 0))
        eq_(1,self.M.best_child(v0, 1.0/math.sqrt(2)))

        data = [(20.57,83),(33.24,113),(112.03,285),
                (1025.74,2029),(139.79,343),(22.06,86),(11.96,61)]
        v0 = Node(7)
        v0.update= 3000
        for i in range(7):
            child = Node(7)
            child.val, child.update = data[i]
            child.parent = v0
            v0.children[i] = child
        eq_(3,self.M.best_child(v0, 0))
        eq_(3,self.M.best_child(v0, 1.0/math.sqrt(2)))

    def test_calc_node_score(self):
        data = [(31.16,105),(52.89,153),(113.05,285),
                (6.87,44),(100.89,259),(16.5,70),(22.05,84)]
        v0 = Node(7)
        v0.update= 1000
        ans = [0.55325390369,0.558168573334,0.552351405228\
                ,0.552361600287,0.552848864639,0.549851545954,0.549266772644]
        for i in range(7):
            child = Node(7)
            child.val, child.update = data[i]
            child.parent = v0
            v0.children[i] = child
            ok_(abs(ans[i] - self.M.calc_node_score(child, 1.0/math.sqrt(2))) < 0.000001)

    def test_backup(self):
        v_l = Node(7)
        root = None
        np = v_l
        for i in range(3):
            np.parent = Node(7)
            np = np.parent
        root = np
        self.M.backpropagation(v_l, 1)
        np = v_l
        i = 0
        ans = [1,-1,1,-1]
        while np:
            eq_(1, np.update)
            eq_(ans[i], np.val)
            np = np.parent
            i += 1
