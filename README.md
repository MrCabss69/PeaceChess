# PeaceChess
A peacefull AI chess engine to learn and find the right pace into the board.


Zoobrist Hashing: 
https://en.wikipedia.org/wiki/Zobrist_hashing


Aperturas -> Mirar si estamos dentro de la teoría una apertura e ir calculando para nuestra BDD como castigar mejor cada movimiento o desviación del oponente.


Tensorflow!

** Añadir como variables o capas: casillas controladas[movimientos legales], casillas abiertas del rey, peones conectados, estructuras de peones,  posibilidad de enroque, jaques, capturas, amenazas y desventaja de material

- utilizar como parámetros el ELO de los oponentes. Se puede elegir un modelo distinto en base al elo estimado del oponente.

- debemos generar datos filtrados y normalizados, trabajados en un formato adecuado para el modelo.

- debemos separar los datos en conjunto de entrenamiento, conjunto de prueba, y conjunto de validación.

- El objetivo del modelo será evaluar númericamente una posición. ( -inf , inf ) En el fondo lo que estamos construyendo es una función heurística de precisión sobre la que aplicar el minimax.

- ¿Qué formato tendrán nuestros datos? Cada input de entrada será un array n-dimensional (¿habrá que aplanarlo?), donde estén reflejados los datos todas las capas. Este array representará una posición válida o terminal de una partida de ajedrez en. Cada fila o capa podrá tener un tamaño diferente, siendo el tamaño último (X,8,8),

# MINIMAX
Algoritmo para recorrer estrategias de forma alternativa para ambos escenarios en árboles binarios de decisión




"""
      
      -> si nodo.terminal or depth == 0:
        return heuristic_value(nodo)
      -> if maximizing:
        actual = -inf
        for child in node.childs:
          actual = max(actual,minimax(child,depth-1,False))
        return actual
      -> else: # ( minimizing )
        actual = inf
        for child in node.childs:
          actual = min(actual,minimax(child,depth-1))
        return actual
 """



-------


# MCTS 
- Selection - Expansion - Simulation - Backpropagation


La idea de este algoritmo es ir explorando poco a poco el árbol empezando por los nodos más cercanos a la raíz y pasando recursivamente y hacia atrás la información entre los nodos. El objetivo es alcanzar un nodo hoja y simular transiciones hasta alcanzar un nodo terminal.


En cada iteración se expanden las hojas, y se recalcula el valor de los nodos precendentes o parentales a las hojas simuladas.

***Selection***: s_i = x_i + C*sqrt(ln(t)/n_i)

            - s_i : value of a node
            - x_i: empirical mean value of a node
            - C: constant
            - t: number of simulations



Cuando estamos realizando una trayectoria del árbol, el nodo hijo que retorna el mayor valor de la ecuación será el seleccionado. Durante un recorrido transversal del árbol una vez se encuentre un nodo hoja se pasa a la fase de expansión.


***Simulación***: se escogen movimientos hasta encontrar un estado terminal o conocido.


***Backpropagación***: tras determinar el valor del nuevo nodo añadido, el arbol debe ser actualizado, se propaga el valor desde el nodo hijo hasta la raíz. Actualizar n-simulaciones y n_wins en cada nodo.

<sub>
          # main function for the Monte Carlo Tree Search
          def monte_carlo_tree_search(root):
              while resources_left(time, computational power):
                  leaf = traverse(root)
                  simulation_result = rollout(leaf)
                  backpropagate(leaf, simulation_result)
          return best_child(root)
<\sub>
