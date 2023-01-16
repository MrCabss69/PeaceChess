import chess 
import random
from stockfish import Stockfish

class Engine():

    def __init__(self) -> None:
        self.eng = Stockfish()
        self.ter = {}
        self.posCont = 0

    # get_random_board -> devuelve una posición aleatoria de un tablero de ajedrez
    def get_random_board(self,n_moves=None):
        if n_moves == None:
            n_moves = random.randint(100, 125)
        board = chess.Board()
        while n_moves > 0 and not board.is_game_over():
            choosen = random.choice(list(board.legal_moves))
            board.push(choosen)
            if not board.is_valid():
                board.pop()
            n_moves -= 1
        return board

    def stockfish_value(self, board):

        self.eng.set_fen_position(board.fen())
        eval   = self.eng.get_evaluation()
        best_m = self.eng.get_best_move()

        if board.is_game_over() and board.fen() not in self.ter:
            self.ter[board.fen()] = eval

        if eval["type"] == "cp":
            return best_m, eval['value']/100

        elif eval["type"] == "mate":
            return best_m, 100_000 if eval['value'] > 0 else best_m, -100_000


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


    def heuristic_value(self, board):
        # el tablero ya es terminal
        if board.is_game_over():
            res = board.outcome().result()
            if '/' in res:
                return 0
            else:
                return 100_000 if res[0] == '1' else -100_000
        # evaluación heurística de material
        else:
            return self.get_material_v(board)

    def get_childs(self,board):
        hijos  = []
        for m in board.legal_moves:
            board.push(m)
            hijos.append(board.fen())
            board.pop()
        return hijos

    # alfa-beta prunning + memoization - LONG + FAST VERSION
    def minimax_ab(self, board, depth, maximize, alfa, beta):
        self.posCont += 1
        # check terminal o maxima alcanzada del minimax por ahora
        if board.is_game_over() or depth == 0 or board.fen in self.ter.keys():
            
            if board.fen() not in self.ter.keys():
                self.ter[board.fen()] = self.heuristic_value(board)
                # self.nodos[node.fen] = self.stockfish_value(node)[1]
            return self.ter[board.fen()]
            
        elif maximize:
            # estamos maximizando - actualizamos alfa
            act = -100_000
            for f in self.get_childs(board):
                hijo = chess.Board(f)
                act  = max(act, self.minimax_ab(hijo, depth-1, False, alfa, beta))
                # cortamos cuando nuestro valor a_maximizar, sea mayor que el del minimizador - él siempre escogera este
                if act >= beta:
                    break
                alfa = max(alfa, act)
            return act
        else:
            # estamos minimizando - actualizamos alfa
            act = 100_000
            for f in self.get_childs(board):
                hijo = chess.Board(f)
                act = min(act, self.minimax_ab(hijo, depth-1, True, alfa, beta))
                if act <= alfa:
                    break
                beta = min(beta, act)
            return act


    def get_move(self, board, depth=3,limit=None):
         
        # TODO: IMPLEMENTAR estructura <GAMETREE> (para memoization) - almacenar los nodos recorridos y sus valores
        #   - ir recalculando recursivamente las últimas hojas candidatas según aumentemos la profundidad

        maximize   = bool(board.turn)
        comparator = " < " if maximize else  " > " 

        best_move  = None
        best_val   = -100_000 if maximize else 100_000

        # recorremos los hijos del nodo actual
        for m in board.legal_moves:
            board.push(m)
            mmval = self.minimax_ab(board, depth, not maximize, -100_000, 100_000)
            # si es un nodo mejor que el actual
            if eval(str(best_val)+comparator+str(mmval)) == True:
                best_val, best_move = mmval, m
            board.pop()

        print(best_move)
        return best_move, best_val# if move != None else random.choice(list(board.legal_moves))