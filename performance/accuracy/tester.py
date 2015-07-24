# add path
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
sys.path.append(SRC_PATH+"algorithm")
sys.path.append(SRC_PATH+"examples/connectfour/")
sys.path.append(PARENT_PATH+"performance/accuracy/testset")
sys.path.append(SRC_PATH+"drawing")

import reader
import mcts
import connectfour_model
import heuristic_model
import pdb
import artist

class Tester(object):
    """
    Execute test with passed parameter and output result
    
    Outputs:
        report.txt: result of test
        {best,worst}_{correct,wrong}.png: img of MCTS tree
    """
    
    def setup_algo(self, algo):
        """
        get proper MCTS module and model from specified algorithm
        
        Args:
            algo: algorithm to use

        Returns:
            mcts: MCTS module which is used in algo
            model: model which is used in algo
        """

        mc, model = None, None
        if algo == "model_heuristic":
            mc = mcts.MCTS()
            model = heuristic_model.ConnectFour()
        else: # default
            mc = mcts.MCTS()
            model = connectfour_model.ConnectFour()
        return mc, model

    def test(self, algo, playout, repeat, testfile, output_dir):
        """
        Execute test with passed parameter and
        output result to specified directory.

        Args:
            algo: algorithm of MCTS to test
            playout: number of playout in one MCTS search
            repeat: the number of times to repeat test
            testfile: the name of input file which is used in test.
            output_dir: the name of directory to output the result
        """

        # setup
        r = reader.Reader()
        mc, model = self.setup_algo(algo)
        mc.set_playout(playout)
        ans, model, next_player = r.read_board(testfile, model)
        ans = int(ans)
        model.next_player = next_player

        # execute test
        res = []
        bc_visit, bw_visit, wc_visit, ww_visit = 0,0,100000,100000
        bc,bw,wc,ww = None, None, None, None
        for i in range(repeat):
            root, act = mc.start(model)
            res.append(act)
            best_visit = root.children[ans].update
            if act == ans:
                if best_visit > bc_visit:
                    bc = root.children[act]
                    bc_visit = best_visit
                elif best_visit < wc_visit:
                    wc = root.children[act]
                    wc_visit = best_visit
            else:
                if best_visit > bw_visit:
                    bw = root.children[act]
                    bw_visit = best_visit
                elif best_visit < ww_visit:
                    ww = root.children[act]
                    ww_visit = best_visit

        self.output_result(algo, playout, repeat, testfile, output_dir,ans,res,bc,bw,wc,ww)

    def output_result(self, algo, playout, repeat, testfile, output_dir, ans, res, bc, bw, wc, ww):
        """ Format and output result
            ** definition **
            best: the search which most assigned simulation to best move
            worst: the search which least assigned simulation to best move
            correct: the search which returns correct answer
            wrong: the search which returns wrong answer

        Args:
            res: array of action which mcts choosed
            bc: root node object of best correct search
            bw: root node object of best wrong search
            wc: root node object of worst correct search
            ww: root node object of worst wrong search
        """
        # aggregate distribution of choosed action
        model = connectfour_model.ConnectFour()
        n = model.act_num
        dist = [0 for i in range(n)]
        for act in res:
            dist[act]+=1

        accuracy = len([1 for act in res if act == ans])*1.0/len(res)
        bc_freq = bc.parent.children[ans].update*1.0/bc.parent.update if bc else 0
        bw_freq = bw.parent.children[ans].update*1.0/bw.parent.update if bw else 0
        wc_freq = wc.parent.children[ans].update*1.0/wc.parent.update if wc else 0
        ww_freq = ww.parent.children[ans].update*1.0/ww.parent.update if ww else 0

        # make directory to output result
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # write out tree images
        painter = artist.Artist()
        if bc: painter.draw(output_dir+'/bc_tree.png', bc.parent)
        if bw: painter.draw(output_dir+'/bw_tree.png', bw.parent)
        if wc: painter.draw(output_dir+'/wc_tree.png', wc.parent)
        if ww: painter.draw(output_dir+'/ww_tree.png', ww.parent)

        # write out the accuracy result
        def w(s):
            f.write(s+'\n')

        with open(output_dir+'/report.txt', 'w+') as f:
            w('')
            w('')
            w('************** MCTS PERFORMANCE TEST ******************')
            w('')
            w(' *** SETTINGS ***')
            w(' ALGORITHM   = {0}'.format(algo))
            w(' PLAYOUT_NUM = {0}'.format(playout))
            w(' TESTSET     = {0}'.format(testfile))
            w(' REPEAT      = {0}'.format(repeat))
            w('')
            w(' *** DISTRIBUTION ***')
            w('FREQUENCY  = '+str(dist))
            w('RATIO      = '+str([freq*1.0/sum(dist) for freq in dist]))
            w('')
            w(' ***  ACCURACY  ***')
            w(' - accuracy = {1:>5}/{2:<5} = {0:4.5f} %'.format(accuracy*100, len([1 for i in res if i==ans]), len(res)))
            w(' - bc_freq  = {1:>5}/{2:<5} = {0:4.5f} %'.format(bc_freq*100, bc.parent.children[ans].update if bc else 0, bc.parent.update if bc else 0))
            w(' - bw_freq  = {1:>5}/{2:<5} = {0:3.5f} %'.format(bw_freq*100, bw.parent.children[ans].update if bw else 0, bw.parent.update if bw else 0))
            w(' - wc_freq  = {1:>5}/{2:<5} = {0:3.5f} %'.format(wc_freq*100, wc.parent.children[ans].update if wc else 0, wc.parent.update if wc else 0))
            w(' - ww_freq  = {1:>5}/{2:<5} = {0:3.5f} %'.format(ww_freq*100, ww.parent.children[ans].update if ww else 0, ww.parent.update if ww else 0))
            w('')

        print
        print '************** MCTS PERFORMANCE TEST ******************'
        print 
        print ' *** SETTINGS ***'
        print ' ALGORITHM   = {0}'.format(algo)
        print ' PLAYOUT_NUM = {0}'.format(playout)
        print ' TESTSET     = {0}'.format(testfile)
        print ' REPEAT      = {0}'.format(repeat)
        print
        print
        print ' *** DISTRIBUTION ***'
        print 'FREQUENCY  = '+str(dist)
        print 'RATIO      = '+str([f*1.0/sum(dist) for f in dist])
        print
        print ' ***  ACCURACY  ***'
        print ' - accuracy = {1:>5}/{2:<5} = {0:4.5f} %'.format(accuracy*100, len([1 for i in res if i==ans]), len(res))
        print ' - bc_freq  = {1:>5}/{2:<5} = {0:4.5f} %'.format(bc_freq*100, bc.parent.children[ans].update if bc else 0, bc.parent.update if bc else 0)
        print ' - bw_freq  = {1:>5}/{2:<5} = {0:3.5f} %'.format(bw_freq*100, bw.parent.children[ans].update if bw else 0, bw.parent.update if bw else 0)
        print ' - wc_freq  = {1:>5}/{2:<5} = {0:3.5f} %'.format(wc_freq*100, wc.parent.children[ans].update if wc else 0, wc.parent.update if wc else 0)
        print ' - ww_freq  = {1:>5}/{2:<5} = {0:3.5f} %'.format(ww_freq*100, ww.parent.children[ans].update if ww else 0, ww.parent.update if ww else 0)
        print
