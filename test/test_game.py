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
import game

@raises(ValueError)
def test_init_raise():
    game.Game(-1)

def test_init():
    game.Game(7)
