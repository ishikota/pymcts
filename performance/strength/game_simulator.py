import os
import sys
PARENT_PATH = os.getenv('PYMCTS_ROOT')
sys.path.append(PARENT_PATH+"examples/connectfour/")
import connectfour_model

class GameSimulator(object):

    def __init__(self):
        # return value for each game result
        self.DRAW = 0
        self.FIRST_WIN = 1
        self.SECOND_WIN = 2
        self.d = False  # if True then display game progress on shell

    def play(self, mc1, model1, mc2, model2):
        """Play one game by using passed algorithms
        Args
            mc1: first player of MCTS object
            model1: first player of model object
            mc2: second player if MCTS object
            model2: second player of model object
        Returns
            flg which indicates the game result
                0: DRAW
                1: FIRST PLAYER(mc1 & model1) won
                2: SECOND PLAYER(mc2 & model2) won
        """
        model = connectfour_model.ConnectFour()
        mc1.ME = 1; mc2.ME = -1
        while True:
            root, act = mc1.start(model1)
            end_flg, score = model.is_terminal(mc1.ME, act)
            model.update(act)
            model1.update(act)
            model2.update(act)
            if end_flg: return self.FIRST_WIN
            root, act = mc2.start(model2)
            end_flg, score = model.is_terminal(mc2.ME, act)
            model.update(act)
            model1.update(act)
            model2.update(act)
            if end_flg: 
                return self.SECOND_WIN if score !=0 else self.DRAW

