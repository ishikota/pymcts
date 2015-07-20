import game
import random
from node import Node
import math
import util

class MCTS(object):
    """Base routine of MCTS method.
        Attributes:
            PLAYOUT_NUM: paremter to define maximum iteration times of MCTS
    """

    def __init__(self, playout_num):
        self.show_progress = False
        self.PLAYOUT_NUM = playout_num
        self.overflow_flg = False

    def start(self, start_state):
        """Start point of MCTS algorithm

        Args:
            game_state: game object which represents current game state

        Returns:
            act_index: index of best action of root node.
        """
        self.overflow_flg = False
        v_0 = Node(start_state.act_num)
        counter = 0
        
        while counter < self.PLAYOUT_NUM and not self.overflow_flg:
            if self.show_progress:
                util.show_progress(counter, self.PLAYOUT_NUM)
            game_state = start_state.clone()
            v_l = self.tree_policy(v_0, game_state)
            delta = self.default_policy(v_l, game_state)
            self.backpropagation(v_l, delta)
            counter += 1
        if self.show_progress: util.fin_progress()
        act_index = self.best_child(v_0, 0)
        return act_index

    C = 0.7071067811865475 # 1.0/sqrt(2)
    def tree_policy(self, v, game):
        """Descend tree until un-visited node is found.

        Descends the tree with updating state of passed game object
        until un-visited node(action) is found.
        If v is terminal state, then just return v.

        Args:
            v: start node to descend the tree.(mostly root node)
            game: game object which corresponds to the state of v
        
        Returns:
            v: the node which has un-visited child node or terminal node.
        """
        while True:
            if v.is_terminal: return v
            if v.unvisited != 0: return self.expand(v, game)
            act_index = self.best_child(v, self.C)
            v = v.children[act_index]
            game.update(act_index)
        return v

    def expand(self, v, game):
        """Choose un-tried action and expand tree.
        
        Args:
            v: parent node which has un-visited child node.
            game: game state which corresponds to passed node v

        Returns:
            child_node: insrance of new created node whose parent is v
        """
        act_index = 0
        while True:
            act_index = v.children.index(-1)    # get index of untried action
            v.unvisited -= 1

            if not game.is_legal(act_index):
                v.children[act_index] = -2  # -2 indicates this action is illegal

                # if all unvisited nodes are illegal one, 
                # then go tree_policy process and descend the tree again.

                if v.unvisited == 0: return self.tree_policy(v, game)
            else:
                break

        # add new expanded node to the tree
        child_node = Node(game.act_num)
        child_node.parent = v
        is_terminal, score = game.is_terminal(act_index)
        game.update(act_index)
        if is_terminal:
            child_node.is_terminal = True
            child_node.val = score
        v.children[act_index] = child_node
        return child_node

    def best_child(self, v, c):
        """Choose best child node of v(passed node).
        
        Args:
            v: choose best child node of v
            c: adjustment constant for calculate node score
        Returns:
            best_index: index of child node which gets highest score
        """
        is_first, best_val, best_index = True, 0, -1
        for i, child in enumerate(v.children):
            if child == -2: continue    # this child is illegal action
            val = self.calc_node_score(child, c)
            if val > best_val or is_first:
                best_val = val
                best_index = i
                is_first = False
            elif val == best_val:
                if bool(random.Random().getrandbits(1)):    # probability of 1/2.
                    best_index = i
        return best_index

    def calc_node_score(self, node, c):
        """Calculate score of passed node
            
            Now score is calculated by UCT algorithm with
            adjustment constant C = 1.0/sqrt(2)
            
        """
        exploitation_term = 1.0*node.val/node.update
        exploration_term = c*math.sqrt(\
                2*math.log(node.parent.update)/node.update)
        score = exploitation_term + exploration_term
        if score > (1<<16): self.overflow_flg = True
        return score

    def default_policy(self, v_l, game):
        """ do the simulation until reaches the end state.
            Args:
                v_l: start point node of simulation
                game: start point game state of simulation
            Returns:
                result score of simulation which defined in game object.
        """
        if v_l.is_terminal: return v_l.val
        return game.simulation()

    def backpropagation(self, v_l, delta):
        """backpropagates simulation result
            Args:
                v_l: start point node of backpropagation
                delta: simulation result score to backpropagetes
        """
        cp = v_l
        while cp:
            cp.update += 1
            cp.val += delta
            delta = -delta  # do negamax here
            cp = cp.parent