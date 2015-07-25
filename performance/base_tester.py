import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
ALGORITHM_PATH = SRC_PATH+"algorithm/"
PERFORMANTH_PATH = PARENT_PATH+"performance/"
ENHANCEMENTS_PATH = ALGORITHM_PATH+"enhancements/"
sys.path.append(ALGORITHM_PATH)
sys.path.append(PERFORMANTH_PATH)
sys.path.append(ENHANCEMENTS_PATH)
sys.path.append(SRC_PATH+"examples/connectfour")

import mcts
import mix_operator

import connectfour_model
import heuristic_model


class BaseTester(object):
    """

    Base Tester class for performance test.
    
    All tester class needs setup_algo method
    So override this base class to implemete it.

    """

    UCT = "UCT MCTS"
    HEURISTIC = "HEURISTIC SIMULATION MCTS"
    MIX_OPERATOR = "MIX OPERATOR MCTS"

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
        if algo == self.HEURISTIC:
            mc = mcts.MCTS()
            model = heuristic_model.ConnectFour()
        elif algo == self.MIX_OPERATOR:
            mc = mix_operator.MCTS()
            model = connectfour_model.ConnectFour()
        else: # algo == UCT
            mc = mcts.MCTS()
            model = connectfour_model.ConnectFour()
        return mc, model

