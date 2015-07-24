"""Caution

    This script depends on nexworkx and pygraphviz to write out tree as image.
    So to run this script, you need to setup these two library before.

"""
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
sys.path.append(SRC_PATH+"algorithm")
import mcts
import artist
import connectfour_model

"""
    sample of drawing MCTS result
"""
def main():
    painter = artist.Artist()
    _mcts = mcts.MCTS()
    _mcts.set_playout(500)
    model = connectfour_model.ConnectFour()
    root, act = _mcts.start(model)
    painter.draw('img/drawing_demo.png', root)

if __name__ == '__main__':
    main()
