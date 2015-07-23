"""Caution

    This script depends on nexworkx and pygraphviz to write out tree as image.
    So to run this script, you need to setup these two library before.

"""

"""
    sample of drawing MCTS result
"""
def main():
    painter = artist.Artist()
    _mcts = mcts4draw.MCTS(500)
    model = connectfour_model.ConnectFour()
    root, act = _mcts.start(model)
    painter.draw('img/drawing_demo.png', root)

if __name__ == '__main__':
    main()
