import chess
import random
import signal
from stockfish import Stockfish


class Engine():

    # constructor
    def __init__(self) -> None:
        self.eng = Stockfish()
        self.ter = {}
        self.posCont = 0

    # get_random_board -> devuelve una posición aleatoria de un tablero de ajedrez
    def get_random_board(self, n_moves=100):
        board = chess.Board()
        while n_moves > 0 and not board.is_game_over():
            choosen = random.choice(list(board.legal_moves))
            board.push(choosen)
            if not board.is_valid():
                board.pop()
            n_moves -= 1
        return board

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

    # get_material_v -> devuelve en un valor numérico el desequilibrio material

    def get_material_v(self, board):
        v = 0
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                piece_value = chess.PIECE_TYPES[piece.piece_type-1]
                if piece.color == chess.WHITE:
                    v += piece_value
                else:
                    v -= piece_value
        return v

    # heuristic_value -> devuelve un valor heurístico para un nodo

    def heuristic_value(self, board):
        # tablero terminal
        if board.is_game_over():
            res = board.outcome().result()
            if '/' in res:
                return 0
            else:
                return 100_000 if res[0] == '1' else -100_000
        # evaluación heurística de material
        else:
            return self.get_material_v(board)

    # sort_moves -> devuelve un valor que evalúa cuán de bueno es un movimiento 'a primeras'
    def rate_move(self, board, move):
        if not board.is_valid():
            return -100
        v = 0.
        ov = self.heuristic_value(board)
        
        board.push(move)
        if not board.is_valid() or move is None:
            return -100
        # aplicar heurística de jaques 
        if board.is_check():
            v += .5
        # aplicar heurística de material
        nv              = self.heuristic_value(board)
        piece_moved     = board.piece_at(move.from_square)
        if piece_moved:
            piece_moved_val = chess.PIECE_TYPES[piece_moved.piece_type-1]
            if nv > ov:
                # aplicar heurística capturas con política mvp-lvp
                # PSEUDO MVP-LVP: cuanto más vale la pieza con la que capturamos, menos vale la captura
                v += abs(nv-ov) * ( 3 / piece_moved_val )
            elif nv < ov:
                v -= abs(nv-ov) * ( 3 / piece_moved_val )
        board.pop()
        return v

    def get_childs(self, board):

        to_explore = list(board.legal_moves) 
        to_explore.sort(key=lambda x: self.rate_move(board,x))
        moves = []
        # hijos = []
        for m in to_explore:
            board.push(m)
            if board.is_valid():
                moves.append(m)
                #hijos.append(board.fen())
            board.pop()
        return moves

    # alfa-beta prunning + memoization - LONG + FAST VERSION
    def minimax_ab(self, board, depth, maximize, alfa, beta):
        self.posCont += 1
        # check terminal o maxima alcanzada del minimax por ahora
        if depth == 0 or board.fen in self.ter.keys() or board.is_game_over():
            if board.fen() not in self.ter.keys():
                self.ter[board.fen()] = self.heuristic_value(board)
                # self.nodos[node.fen] = self.stockfish_value(node)[1]
            return self.ter[board.fen()]

        elif maximize:
            # estamos maximizando - actualizamos alfa
            act = -100_000
            for f in self.get_childs(board):
                board.push(f)
                act = max(act, self.minimax_ab(
                    board, depth-1, False, alfa, beta))
                board.pop()
                # cortamos cuando nuestro valor_a_maximizar sea mayor que el del minimizador
                # el adversario (mimizador) siempre escogera el menor en su turno
                if act >= beta:
                    break
                alfa = max(alfa, act)
            return act
        else:
            # estamos minimizando - actualizamos alfa
            act = 100_000
            for f in self.get_childs(board):
                board.push(f)
                act = min(act, self.minimax_ab(
                    board, depth-1, True, alfa, beta))
                # cortamos cuando nuestro valor_a_minimizar sea menor que el del adversario
                # él como maximizador siempre escogera el mayor de los valores en su turno
                board.pop()
                if act <= alfa:
                    break
                beta = min(beta, act)
            return act

    def get_move(self, board, depth=2, limit=None):

        # TODO: IMPLEMENTAR estructura <GAMETREE> (para memoization) - almacenar los nodos recorridos y sus valores
        #   - ir recalculando recursivamente las últimas hojas candidatas según aumentemos la profundidad
        # TABLA DE TRANSPOSICIONES CON NOTACIÓN ZOIBRIST

        maximize = bool(board.turn)
        comparator = " < " if maximize else " > "

        best_move = None
        best_val = -100_000 if maximize else 100_000

        # recorremos los hijos del nodo actual
        try:
            for m in board.legal_moves:
                board.push(m)
                mmval = self.minimax_ab(
                    board, depth, not maximize, -100_000, 100_000)
                board.pop()
                # si es un nodo mejor que el actual
                if eval(str(best_val)+comparator+str(mmval)) == True:
                    best_val, best_move = mmval, m
                
            return best_move, best_val
        except:
            return best_move, best_val
