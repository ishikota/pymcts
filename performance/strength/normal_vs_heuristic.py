import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
import tester

T = tester.Tester()
T.test(T.UCT, T.HEURISTIC, 100, 10, "out/n_vs_h")

