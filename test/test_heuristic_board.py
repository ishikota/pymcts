# add path to the src and test directory
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
TEST_PATH = PARENT_PATH +"test/"
sys.path.append(SRC_PATH+"algorithm")
sys.path.append(TEST_PATH)
sys.path.append(PARENT_PATH+"performance/accuracy/testset")
sys.path.append(SRC_PATH+"examples/connectfour/")

from unittest import TestCase
from nose.tools import *
import pdb
import reader
import connectfour_model
import heuristic_model

def test_choice():
    model = heuristic_model.ConnectFour()
    def u(i):
        model.update(i)
    for i in range(6):
        ok_(3, model.get_legal_move())
        model.update(3)
    
