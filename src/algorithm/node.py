
class Node(object):


    def __init__(self, child_num):
        # pointer of parent and children nodes
        self.parent = None
        self.children = [-1 for i in range(child_num)]
        # value for MCTS search
        self.val = 0
        self.update = 0
        self.is_terminal = False
        self.unvisited = child_num

