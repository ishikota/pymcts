import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
TESTSET_PATH = PARENT_PATH+"performance/accuracy/testset/"
import tester

T = tester.Tester()
T.test("UCT MCTS",500,30,TESTSET_PATH+"initial.in","out/initial/normal_500")
T.test("UCT MCTS",1000,30,TESTSET_PATH+"initial.in","out/initial/normal_1000")
T.test("UCT_MCTS",2000,30,TESTSET_PATH+"initial.in","out/initial/normal_2000")
T.test("model_heuristic",500,30,TESTSET_PATH+"initial.in","out/initial/heuristic_500")
T.test("model_heuristic",1000,30,TESTSET_PATH+"initial.in","out/initial/heuristic_1000")
T.test("model_heuristic",2000,30,TESTSET_PATH+"initial.in","out/initial/heuristic_2000")

