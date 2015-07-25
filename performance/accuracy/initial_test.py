import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
TESTSET_PATH = PARENT_PATH+"performance/accuracy/testset/"
import tester

T = tester.Tester()
T.test(T.UCT,500,30,TESTSET_PATH+"initial.in","out/initial/normal_500")
T.test(T.UCT,1000,30,TESTSET_PATH+"initial.in","out/initial/normal_1000")
T.test(T.UCT,2000,30,TESTSET_PATH+"initial.in","out/initial/normal_2000")
T.test(T.HEURISTIC,500,30,TESTSET_PATH+"initial.in","out/initial/heuristic_500")
T.test(T.HEURISTIC,1000,30,TESTSET_PATH+"initial.in","out/initial/heuristic_1000")
T.test(T.HEURISTIC,2000,30,TESTSET_PATH+"initial.in","out/initial/heuristic_2000")

