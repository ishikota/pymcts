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
import pdb
import time

class Tester(base_tester.BaseTester):
    """
    Execute test with passed parameter and output result
    
    Outputs:
        report.txt: result of test
        {best,worst}_{correct,wrong}.png: img of MCTS tree
    """
    
    def test(self, algo, playout, repeat, output_dir):
        """
        Measure MCTS search time of specified MCTS algorithm
        Result time is the average of repeated test.

        Args:
            algo: algorithm of MCTS to test
            playout: number of iteration of MCTS search
            repeat: the number of times to repeat test
            output_dir: the path of directory to output the result
        """

        # setup
        mc, model = self.setup_algo(algo)
        mc.ME = 1
        mc.set_playout(playout)

        # execute test
        search_time = [0 for i in range(repeat)]    # time of 1-MCTS process
        iterate_time = [0 for i in range(repeat)] # time of 1-MCTS iteration
        for i in range(repeat):
            st = time.time()
            root, act = mc.start(model)
            search_tm = time.time() - st
            iteration_tm = search_tm*1.0/playout
            search_time[i] = search_tm
            iterate_time[i] = iteration_tm
        self.output_result(algo, playout, repeat, output_dir, search_time, iterate_time)

    def output_result(self, algo, playout, repeat, output_dir, search, iterate):
        """ 
            Format and output result
        """
        
        # make directory to output result
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # write out the result
        def w(s):
            f.write(s+'\n')

        # calculate average and median
        m = repeat/2
        search.sort()
        mean_proc = sum(search)*1.0/len(search)
        median_proc = search[m/2] if m%2==1 else 1.0*(search[m/2] + search[m/2-1])/2
        iterate.sort()
        mean_iter = sum(iterate)*1.0/len(iterate)
        median_iter = iterate[m/2] if m%2==1 else 1.0*(iterate[m/2] + iterate[m/2-1])/2

        with open(output_dir+'/report.txt', 'a+') as f:
            w('')
            w('')
            w('************** MCTS SEARCH TIME TEST ******************')
            w('')
            w(' *** SETTINGS ***')
            w(' ALGORITHM = {0}'.format(algo))
            w(' PLAYOUT   = {0}'.format(playout))
            w(' REPEAT    = {0}'.format(repeat))
            w('')
            w(' *** RESULT ***')
            w(' MEAN   OF 1-MCTS PROCESS   : {0:f}'.format(mean_proc))
            w(' MEDIAN OF 1-MCTS PROCESS   : {0:f}'.format(median_proc))
            w(' MEAN   OF 1-ITERATION      : {0:f}'.format(mean_iter))
            w(' MEDIAN OF 1-ITERATION      : {0:f}'.format(median_iter))
            w('')
            w('')

            print ''
            print ''
            print '************** MCTS SEARCH TIME TEST ******************'
            print ''
            print ' *** SETTINGS ***'
            print ' ALGORITHM = {0}'.format(algo)
            print ' PLAYOUT   = {0}'.format(playout)
            print ' REPEAT    = {0}'.format(repeat)
            print ''
            print ' *** RESULT ***'
            print ' MEAN   OF 1-MCTS PROCESS   : {0:f}'.format(mean_proc)
            print ' MEDIAN OF 1-MCTS PROCESS   : {0:f}'.format(median_proc)
            print ' MEAN   OF 1-ITERATION      : {0:f}'.format(mean_iter)
            print ' MEDIAN OF 1-ITERATION      : {0:f}'.format(median_iter)
            print ''
            print ''

