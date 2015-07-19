
class Game(object):
    """Base class of Game representation.

    MCTS needs game specific information 
    like what action is illegal one, or how to simulates the game.
    This object teaches such information to MCTS module.
    So you define these game specific rules in this object.
    
    What you need to define is 5 methods
    clone, update, is_legal, is_terminal, simulation

    Attributes:
        act_num: the number of action in each state.(must act_num > 0)
        ex.) if ConnectFour of BOARD_WIDTH=6 then set act_num to 6
    """
    def __init__(self, act_num):
        if act_num <= 0 or not isinstance(act_num, int):
            raise ValueError("act_num must be positive integer")
        self.act_num = act_num


    def clone(self):
        """Clones this Game instance.

        MCTS search uses Game object of start state in each iteration.
        So this method is called every search iteration.

        Returns:
            A deep copy of this Game object.
        """
        raise NotImplementedError('method "clone" is not overriden.')
    
    def update(self, node_index):
        """Progress the Game state.

        Progress the Game state by passed node_index.
        This method is called in Expand phase of MCTS
        to descend the search tree.
        
        Args:
            node_index: index of child node which MCTS has desended
        """
        raise NotImplementedError('method "update" is not overriden.')

    def is_legal(self, action):
        """Check if passed action is legal.

        This method is used in Expand phase of MCTS
        not to descend the node which is illegal state.

        Args:
            action: information to update game state.
                ex.) if Game is [ConnectFour] then action=(who, column)

        Returns:
            boolean if passed action is legal or not.
        """
        raise NotImplementedError('method "is_legal" is not overriden.')

    #return tuple of (boolean, score)
    def is_terminal(self, action):
        """Check if passed action reaches to terminal game state.

        This method is used in Expand phase of MCTS.

        Args:
            action: information to update game state.
                ex.) if Game is [ConnectFour] then action=(who, column)

        Returns:
            tuple of (flg, score)
            flg: boolean if passed action is legal or not.
            score: score of game result if it's terminal.
        """
        raise NotImplementedError('method "is_terminal" is not overriden.')

    def simulation(self):
        """Simulates the game and get result.

        Simulates the game from current state to the end of the game 
        and returns the result of simulation.

        Returns:
            the score of simulation result.
            ex.) if win in the simulation then return 1 else -1.
        """
        raise NotImplementedError('method "simulation" is not overriden.')

