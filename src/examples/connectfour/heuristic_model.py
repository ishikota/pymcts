import connectfour_model
import heuristic
import random

class ConnectFour(connectfour_model.ConnectFour):
    """
    ConnectFour Game Object which uses 
    Odd/Even heuristic in simulation.
    """

    def __init__(self):
        super(ConnectFour, self).__init__()
        self.H = heuristic.Heuristic(1,-1)

    def get_legal_move(self):
        legal_move = [col for col in range(7) if self.is_legal(col)]
        self.H.ME = self.next_player
        self.H.OPPO = -self.next_player
        best_moves = self.H.choiceByHeuristic(self, legal_move)
        return random.choice(best_moves)
