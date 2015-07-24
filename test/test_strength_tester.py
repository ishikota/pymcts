# add path to the src and test directory
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
TEST_PATH = PARENT_PATH +"test/"
sys.path.append(SRC_PATH+"algorithm")
sys.path.append(TEST_PATH)
sys.path.append(PARENT_PATH+"performance/accuracy/testset")
sys.path.append(PARENT_PATH+"performance/strength")
sys.path.append(SRC_PATH+"examples/connectfour/")

from unittest import TestCase
from nose.tools import *
import pdb
import mcts
import connectfour_model
import heuristic_model
import game_simulator

def test_game():
    mc1 = mcts.MCTS()
    mc2 = mcts.MCTS()
    model1 = connectfour_model.ConnectFour()
    model2 = heuristic_model.ConnectFour()
    T = game_simulator.GameSimulator()
    res = T.play(mc1,model1,mc2,model2)
    ok_(res in [0,1,2])
