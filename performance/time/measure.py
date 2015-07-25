import tester

T = tester.Tester()
playout = [500, 1000, 2000]
repeat = [20, 20, 20]
for i in range(len(playout)):
    T.test(T.UCT, playout[i], repeat[i], "out/normal/")
    T.test(T.HEURISTIC, playout[i], repeat[i], "out/heuristic/")

