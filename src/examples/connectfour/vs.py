# add path to the src and test directory
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
sys.path.append(SRC_PATH+"algorithm")

import mcts
import connectfour_model
import heuristic_model

# Clear the shell
os.system("clear")

# Setup for MCTS
model = heuristic_model.ConnectFour()
#model = connectfour_model.ConnectFour()
print '> Input the maximum number of iteration in MCTS...'
playout_num = int(raw_input())
_mcts = mcts.MCTS()
_mcts.set_playout(playout_num)
_mcts.show_progress = True

# start the game !!
print 'Let\'s ConnectFour !!'
model.display()
while True:

    # Player turn
    print '> Input the column to make a move...'
    action = int(raw_input())-1
    end_flg, score = model.is_terminal(action)
    model.update(action)
    model.display()
    if end_flg:
        print '\nYou win !!!\n'
        break
    
    # MCTS CPU Turn
    root, action = _mcts.start(model)
    print 'MCTS make a move on column '+str(action+1)
    end_flg, score = model.is_terminal(action)
    model.update(action)
    model.display()
    if end_flg:
        print '\nYou lose ...\n'
        break
