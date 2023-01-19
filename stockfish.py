#from stockfish import Stockfish
"""
    # stockfish_value -> devuelve la evaluación de stockfish para un bord dado em la forma (best_move,board_eval)
    def stockfish_value(self, board):

        self.eng.set_fen_position(board.fen())
        eval = self.eng.get_evaluation()
        best_m = self.eng.get_best_move()

        if board.is_game_over() and board.fen() not in self.ter:
            self.ter[board.fen()] = eval

        if eval["type"] == "cp":
            return best_m, eval['value']/100

        elif eval["type"] == "mate":
            return best_m, 100_000 if eval['value'] > 0 else best_m, -100_000
"""