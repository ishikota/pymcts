import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
sys.path.append(SRC_PATH+"algorithm")

import pdb
import mcts
import math

class MCTS(mcts.MCTS):
    """ MCTS enhancements proposed in CrazyStone's paper(2006).
        
        This algorithm modified backup operator by using mix operator.
        It means parent node value is defined by robust max and mean operator.
        Robust max child value is adopted when robust max and max child 
        is corresponds else adopts mean value of children.

    """

    def calc_node_score(self, node, c):
        """Calculate score of passed node by mix operator
        """
        #check if robust max and max mode is corresponds
        v0, v1 = None, None
        for child in node.children:
            if isinstance(child, int): continue
            if not v0 or v0.val < child.val:
                v1 = v0
                v0 = child
            elif not v1 or v1.val < child.val:
                v1 = v0

        exploitation_term = 0
        if v0 and v1 and v0.update > v1.update:    # if robust max == max
            exploitation_term = 1.0*v0.val/v0.update    # use max operator
        else:
            exploitation_term = 1.0*node.val/node.update    # use mean operator
        pdb.set_trace()

        exploration_term = c*math.sqrt(\
                2*math.log(node.parent.update)/node.update)

        score = exploitation_term + exploration_term
        if score > (1<<16): self.overflow_flg = True
        return score
