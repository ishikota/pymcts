import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
TESTSET_PATH = PARENT_PATH+"performance/accuracy/testset/"
import tester

T = tester.Tester()
T.test("UCT MCTS",50,10,TESTSET_PATH+"sample.in","out/sample")
T.test("UCT MCTS",500,10,TESTSET_PATH+"initial.in","out/start_500")
T.test("UCT MCTS",1000,10,TESTSET_PATH+"initial.in","out/start_1000")
T.test("UCT MCTS",2000,10,TESTSET_PATH+"initial.in","out/start_2000")

