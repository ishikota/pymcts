# add path
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
sys.path.append(SRC_PATH+"algorithm")
sys.path.append(SRC_PATH+"examples/connectfour/")
sys.path.append(PARENT_PATH+"performance/")
sys.path.append(PARENT_PATH+"performance/accuracy/testset")
sys.path.append(SRC_PATH+"drawing")

import base_tester
import mcts
import connectfour_model
import heuristic_model
import game_simulator
import pdb

class Tester(base_tester.BaseTester):
    """
    Execute test with passed parameter and output result
    
    Outputs:
        report.txt: result of test
        {best,worst}_{correct,wrong}.png: img of MCTS tree
    """
    

    def test(self, algo1, algo2, playout, repeat, output_dir):
        """
        Execute test with passed parameter and
        output result to specified directory.

        Args:
            algo1: algorithm of MCTS to test
            algo2: algorithm of MCTS to test
            playout: computational budget of MCTS iteration
            repeat: the number of times to repeat test
            output_dir: the name of directory to output the result
        """

        # setup
        G = game_simulator.GameSimulator()
        mc1, model1 = self.setup_algo(algo1)
        mc2, model2 = self.setup_algo(algo2)
        mc1.ME = 1; mc2.ME = -1
        mc1.set_playout(playout)
        mc2.set_playout(playout)

        # execute test
        memo = [0 for i in range(3)] # draw, first-win, second-win
        for i in range(repeat):
            _model1 = model1.clone()
            _model2 = model2.clone()
            res = G.play(mc1, _model1, mc2, _model2)
            memo[res] += 1
        self.output_result(algo1, algo2, playout, repeat, output_dir, memo)

    def output_result(self, algo1, algo2, playout, repeat, output_dir, memo):
        """ 
            Format and output result
        """
        
        # make directory to output result
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # write out the result
        def w(s):
            f.write(s+'\n')

        with open(output_dir+'/report.txt', 'w+') as f:
            w('')
            w('')
            w('************** MCTS STRENGTH TEST ******************')
            w('')
            w(' *** SETTINGS ***')
            w(' PLAYER1   = {0}'.format(algo1))
            w(' PLAYER2   = {0}'.format(algo2))
            w(' BUDGET    = {0}'.format(playout))
            w(' REPEAT    = {0}'.format(repeat))
            w('')
            w(' *** RESULT ***')
            w(' PLAYER1 WIN : {0:d} '.format(memo[1]))
            w(' PLAYER2 WIN : {0:d} '.format(memo[2]))
            w(' DRAW        : {0:d}'.format(memo[0]))
            w('')
            w('')

            print ''
            print ''
            print '************** MCTS STRENGTH TEST ******************'
            print ''
            print ' *** SETTINGS ***'
            print ' PLAYER1   = {0}'.format(algo1)
            print ' PLAYER2   = {0}'.format(algo2)
            print ' BUDGET    = {0}'.format(playout)
            print ' REPEAT    = {0}'.format(repeat)
            print ''
            print ' *** RESULT ***'
            print ' PLAYER1 WIN : {0:d} '.format(memo[1])
            print ' PLAYER2 WIN : {0:d} '.format(memo[2])
            print ' DRAW        : {0:d}'.format(memo[0])
            print ''
            print ''
