import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
import tester

T = tester.Tester()
T.test(T.UCT, T.HEURISTIC, 0, 3, 20, "out/normal_vs_heuristic")
T.test(T.HEURISTIC, T.UCT, 0, 3, 20, "out/normal_vs_heuristic")

