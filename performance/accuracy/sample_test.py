import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
TESTSET_PATH = PARENT_PATH+"performance/accuracy/testset/"
import tester

T = tester.Tester()
T.test("model_heuristic",50,10,TESTSET_PATH+"sample.in","out/heuristic")
#T.test("UCT MCTS",500,10,TESTSET_PATH+"initial.in","out/sample")
#T.test("UCT MCTS",1000,10,TESTSET_PATH+"initial.in","out/sample")
#T.test("UCT MCTS",2000,10,TESTSET_PATH+"initial.in","out/sample")

