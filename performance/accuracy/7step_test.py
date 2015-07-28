import os
PARENT_PATH = os.getenv('PYMCTS_ROOT')
TESTSET_PATH = PARENT_PATH+"performance/accuracy/testset/"
import tester

T = tester.Tester()
T.test(T.UCT,500,100,TESTSET_PATH+"7-step-read.in","out/7step/normal/normal_500")
T.test(T.UCT,1000,100,TESTSET_PATH+"7-step-read.in","out/7step/normal/normal_1000")
T.test(T.UCT,2000,100,TESTSET_PATH+"7-step-read.in","out/7step/normal/normal_2000")
T.test(T.UCT,5000,100,TESTSET_PATH+"7-step-read.in","out/7step/normal/normal_5000")
T.test(T.HEURISTIC,500,100,TESTSET_PATH+"7-step-read.in","out/7step/heuristic/heuristic_500")
T.test(T.HEURISTIC,1000,100,TESTSET_PATH+"7-step-read.in","out/7step/heuristic/heuristic_1000")
T.test(T.HEURISTIC,2000,100,TESTSET_PATH+"7-step-read.in","out/7step/heuristic/heuristic_2000")
#T.test(T.HEURISTIC,5000,100,TESTSET_PATH+"7-step-read.in","out/7step/heuristic/heuristic_5000")
T.test(T.MIX_OPERATOR,500,100,TESTSET_PATH+"7-step-read.in","out/7step/mixoperator/mixoperator_500")
T.test(T.MIX_OPERATOR,1000,100,TESTSET_PATH+"7-step-read.in","out/7step/mixoperator/mixoperator_1000")
T.test(T.MIX_OPERATOR,2000,100,TESTSET_PATH+"7-step-read.in","out/7step/mixoperator/mixoperator_2000")
T.test(T.MIX_OPERATOR,5000,100,TESTSET_PATH+"7-step-read.in","out/7step/mixoperator/mixoperator_5000")
