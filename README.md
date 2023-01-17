# PeaceChess
A peacefull tree-search optimizer chess engine to learn and find the right pace into the board. In the future the evaluation will be calculated via TensorFlow model


## CURRRENTLY FULLY WORKING
![alt text](https://github.com/MrCabss69/PeaceChess/blob/main/resources/engine_example.png)

### MINIMAX
Algoritmo para recorrer estrategias de forma alternativa para ambos jugadores en árboles binarios de decisión. Info: https://en.wikipedia.org/wiki/Minimax

    
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
        
### ALFA BETA PRUNING
            function alphabeta(node, depth, α, β, maximizingPlayer) is
                if depth = 0 or node is a terminal node then
                    return the heuristic value of node
                if maximizingPlayer then
                    value := −∞
                    for each child of node do
                        value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
                        α := max(α, value)
                        if value ≥ β then
                            break (* β cutoff *)
                    return value
                else
                    value := +∞
                    for each child of node do
                        value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
                        β := min(β, value)
                        if value ≤ α then
                            break (* α cutoff *)
                    return value
Info: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

### Zoobrist Hashing: 

https://en.wikipedia.org/wiki/Zobrist_hashing



### Tabla de Transposiciones

Usar el hash zoobrist para almacenar una tabla de transposiciones y optimizar el orden de jugadas.
https://www.chessprogramming.org/Transposition_Table#How_it_works


--------------

## TODO: 

### Aperturas

Mirar si estamos dentro de la teoría una apertura e ir calculando para nuestra BDD (o tabla de transposiciones) como castigar mejor cada movimiento o desviación del oponente.



### Optimizar exploración de nodos hijos - política de selección

Optimizar los nodos hijos que se recorren primero para explorar en el algoritmo alfa-beta => cuanto antes descubramos mejores valores, antes podremos podar grandes porciones del árbol. 


Ejemplos de mejora heurística para capturas: política MVL-LVP. Most Valuable Piece - (eaten by) - Less Valuable Piece


### Implementación
La idea (como la mía original sin saber que existía) es usar tablas de posiciones con almacenando las evaluaciones anteriores, la profundidad a la que fueron hechas y las conclusiones de dichas evaluaciones. 

Lo ideal sería setear unos recursos límites de tiempo por llamada al mimimax, y cuando se ejecute el algoritmo sobre nodos ya conocidos, usar los recursos para ampliar el árbol por esas ramas.

--------------

## Tensorflow

** Añadir como variables o capas: casillas controladas[movimientos legales], casillas abiertas del rey, peones conectados, estructuras de peones,  posibilidad de enroque, jaques, capturas, amenazas y desventaja de material


- Generar datos filtrados y normalizadoa con su valor real correspondiente. Datos trabajados en un formato adecuado para el modelo.

- Separar los datos en conjunto de entrenamiento, conjunto de prueba, y conjunto de validación.

- El objetivo será evaluar númericamente una posición. ( -inf , inf ) En el fondo lo que estamos construyendo es una función heurística de precisión sobre la que aplicar el minimax.

- A futuro: utilizar como parámetros el ELO de los oponentes. Se puede elegir un modelo distinto en base al elo estimado del oponente.

- Formato para nuestros datos: cada input de entrada será un array n-dimensional (¿habrá que aplanarlo?). En este array estarám reflejados por capas todos los datos que describan de la forma más exhaustiva posible la situación actual. Dicho array representará una posición válida o terminal. Cada fila o capa podrá tener un tamaño diferente, siendo el tamaño último (X,8,8),

--------------

## MCTS 
- Selection - Expansion - Simulation - Backpropagation


La idea de este algoritmo es ir explorando poco a poco el árbol empezando por los nodos más cercanos a la raíz y pasando recursivamente y hacia atrás la información entre los nodos. El objetivo es alcanzar un nodo hoja y simular transiciones hasta alcanzar un nodo terminal.


En cada iteración se expanden las hojas, y se recalcula el valor de los nodos precendentes o parentales a las hojas simuladas.

***Selection***

Cuando estamos realizando una trayectoria del árbol, el nodo hijo que retorna el mayor valor de la ecuación será el seleccionado. Durante un recorrido transversal del árbol una vez se encuentre un nodo hoja se pasa a la fase de expansión.


<img src="https://latex.codecogs.com/gif.latex?S_i=x_i+C*sqrt(ln(t)/n_i)" /> 

Donde:

                  - s_i = Value of a node
                  
                  - x_i = Empirical mean value of a node
                  
                  - C   = Constant mean value of a node
                  
                  - t   = Number of simulation mean value of a node





***Simulación***: se escogen movimientos hasta encontrar un estado terminal o conocido.




***Backpropagación***: tras determinar el valor del nuevo nodo añadido, el arbol debe ser actualizado, se propaga el valor desde el nodo hijo hasta la raíz. Actualizar n-simulaciones y n_wins en cada nodo.

          # main function for the Monte Carlo Tree Search
          def monte_carlo_tree_search(root):
              while resources_left(time, computational power):
                  leaf = traverse(root)
                  simulation_result = rollout(leaf)
                  backpropagate(leaf, simulation_result)
          return best_child(root)
