import chess

class Nodo():

    def __init__(self, board):
        self.visits = 1
        self.board = board
        self.fen = board.fen()
        self.child_moves, self.childs = self.get_childs()
        self.terminal = self.board.is_game_over()
        if self.terminal:
            res = self.board.outcome().result()

    # get_childs -> return lista de string con FEN's de posiciones legales a un movimiento
    def get_childs(self):
        childs = []
        moves  = []
        for m in self.board.legal_moves:
            self.board.push(m)
            childs.append(self.board.fen())
            moves.append(m)
            self.board.pop()
        return moves,childs

    def update_visit(self):
        self.visits += 1
