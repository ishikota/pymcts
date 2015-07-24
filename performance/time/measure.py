import tester

T = tester.Tester()
playout = [500, 1000, 2000]
repeat = [20, 20, 20]
for i in range(len(playout)):
    T.test("UCT MCTS", playout[i], repeat[i], "out/normal/")
    T.test("model_heuristic", playout[i], repeat[i], "out/heuristic/")

