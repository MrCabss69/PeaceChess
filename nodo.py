import copy
import chess

v = {'p': -1, 'P': 1, 'n': -3, 'N': 3, 'b': -3, 'B': 3, 'k': -
     1000, 'K': 1000, 'r': -5, 'R': 5, 'q': -9, 'Q': 9}


class Nodo():

    def __init__(self, board):
        self.visits = 1
        self.board = board
        self.fen = board.fen()
        self.terminal = self.board.outcome() != None
        if self.terminal:
            res = self.board.outcome().result()

    def get_childs(self):
        board = copy.deepcopy(self.board)
        childs = {}
        for m in board.legal_moves:
            board.push(m)
            hijo = Nodo(chess.Board(board.fen()))
            childs[m.uci()] = hijo
            board.pop()
        self.childs = childs  # legal moves productions
        return childs

    def update_visit(self):
        self.visits += 1
