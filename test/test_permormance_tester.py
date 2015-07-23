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

def test_read():
    r = reader.Reader()
    model = connectfour_model.ConnectFour()
    f_name = PARENT_PATH+"performance/accuracy/testset/sample.in"
    answer, model, next_player = r.read_board(f_name, model)
    ans_act = 6
    ans_table = [[-1, 1, 1, 1, -1, 0, -1], [0, 0, 0, 1, 1, 0, -1], [0, 0, 0, 1, 1, 0, -1], [0, 0, 0, -1, 0, 0, -1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    ans_pos = [1, 1, 1, 4, 3, 0, 4]
    ans_next = -1
    ok_(ans_act, answer)
    ok_(ans_table, model.table)
    ok_(ans_pos, model.position)
    ok_(ans_next, model.next_player)

