"""Caution

    This script depends on nexworkx and pygraphviz to write out tree as image.
    So to run this script, you need to setup these two library before.

"""

#add path to the src and test directory
import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
SRC_PATH = PARENT_PATH +"src/"
sys.path.append(SRC_PATH+"algorithm")
sys.path.append(SRC_PATH+"examples/connectfour/")

import pdb
import mcts4draw
import connectfour_model
from node import Node
import networkx as nx
import matplotlib.pyplot as plt

def draw_tree(root):
    """draw tree of mcts result as image

    Args:
        root: object of root node of mcts tree to write out.
    """
    
    _mcts = mcts4draw.MCTS(1)
    C = 0.7071067811865475 # 1.0/sqrt(2)
    id_count = 0
    q = [] # (id, node)
    G = nx.DiGraph()
    best_node = []
    other_node = []
    best_edge = []
    other_edge = []
    labels = {}

    # add root to graph
    G.add_node(str(id_count))
    q.append((id_count, root, True))
    best_node.append(str(id_count))
    id_count += 1

    # construct graph object of MCTS tree
    while q:
        pid, parent, is_best = q.pop(0)
        best_index = _mcts.best_child(parent, C) if is_best else -1
        for i, child in enumerate(parent.children):
            if isinstance(child, int):continue
            G.add_node(str(id_count))
            G.add_edge(str(pid), str(id_count))
            if i==best_index:
                best_node.append(str(id_count))
                best_edge.append((str(pid),str(id_count)))
                labels[str(id_count)]=str(i)
            else:
                other_node.append(str(id_count))
                other_edge.append((str(pid),str(id_count)))
                labels[str(id_count)]=''
            q.append((id_count, child, i==best_index))
            id_count += 1

    # write out mcts tree as image
    pos=nx.graphviz_layout(G,prog='dot')
    nx.draw_networkx_nodes(G,pos,nodelist=other_node,node_color='r',alpha=0.1)
    nx.draw_networkx_nodes(G,pos,nodelist=best_node,node_color='b',alpha=1)
    nx.draw_networkx_edges(G,pos,edgelist=other_edge,width=1,alpha=0.5,edge_color='r')
    nx.draw_networkx_edges(G,pos,edgelist=best_edge,width=2,alpha=0.5,edge_color='b')
    nx.draw_networkx_labels(G,pos,labels)   # attachs the label only on best nodes
    plt.savefig('img/mcts_tree.png')

def main():
    _mcts = mcts4draw.MCTS(500)
    model = connectfour_model.ConnectFour()
    root, act = _mcts.start(model)
    draw_tree(root)

if __name__ == '__main__':
    main()
