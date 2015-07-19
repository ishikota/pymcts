import pdb
import mcts
M = mcts.MCTS(50)
import sample_game
G = sample_game.SampleGame()
from node import Node
v_0 = Node(G.act_num)
v_0 = Node(7)

v2 = M.expand(v_0, G)
pdb.set_trace()
