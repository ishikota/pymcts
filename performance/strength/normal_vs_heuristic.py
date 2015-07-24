import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
import tester

T = tester.Tester()
T.test("UCT MCTS", "model_heuristic", 100, 10, "out/n_vs_h")

