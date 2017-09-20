import heapq
import numpy as np

class PriorityQueue:
	""" Fila de nodos com prioridade """
	def __init__(self):
		self.elements = []

	def empty(self):
		""" Verifica se a fila esta vazia """
		return len(self.elements) == 0

	def put(self, item, priority):
		""" Insere um nodo nodo na fila """
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		""" Remove e retorna o nodo com maior prioridade, ou seja,
		nodo contendo menor valor de prioridade """
		return heapq.heappop(self.elements)[1]

def neighbors(node):
	""" Gera e retorna a lista de nodos adjacentes possiveis do nodo enviado por parametro """
	neighbors = []
	for direction in ['left', 'right', 'up', 'down']:
		sucessor = neighbor(node, direction)
		if sucessor:
			neighbors.append(sucessor)
	return neighbors

def neighbor(node, direction):
	""" Gera e retorna um nodo adjacente a partir do nodo parametro e direcao """
	zero_pos = node.index(0)
	xpos = zero_pos % 3
	ypos = int(zero_pos / 3)
	# verifica direcao e se a posicao da celula vazia esta em
	# uma parede para atualizar zero_pos com nova posicao
	if direction == 'left' and xpos != 0:
		zero_pos = zero_pos - 1
	elif direction == 'right' and xpos != 2:
		zero_pos = zero_pos + 1
	elif direction == 'up' and ypos != 0:
		zero_pos = zero_pos - 3
	elif direction == 'down' and ypos != 2:
		zero_pos = zero_pos + 3
	else:
		# retorna nulo se nao existe nodo adjacente naquela direcao
		return None
	# retorna novo nodo com posicao da celula vazia atualizada
	return swap_zero(list(node), zero_pos)

def swap_zero(node, new_pos):
	""" Troca posicao da celula vazia pela nova posicao """
	old_zero_index = node.index(0)
	old_zero, new_zero = node[old_zero_index], node[new_pos]
	node[new_pos], node[old_zero_index] = old_zero, new_zero
	return node

def node_hash(node):
	""" Gera e retorna hash unico para nodo parametro
	Ex:
		node[0] * 1        +
		node[1] * 10       +
		node[2] * 100      +
		node[3] * 1000     +
		node[4] * 10000    +
		node[5] * 100000   +
		node[6] * 1000000  +
		node[7] * 10000000 +
		node[8] * 100000000
	"""
	return sum(np.multiply(node,
		[1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
		)
	)

def heuristic(neighbor, goal):
	""" Calcula e retorna diferenca entre dois vetores,
		subtraindo e somando os valores absolutos
	"""
	return sum(np.absolute(np.subtract(np.array(neighbor), np.array(goal))))

def solve(start, goal):
	""" Busca e retorna caminho entre dois nodos usando A* """
	# inicia fila de prioridades e lista de custos com nodo inicial
	queue = PriorityQueue()
	queue.put(start, 0)
	cost_so_far = {}
	cost_so_far[node_hash(start)] = 0
	current = None
	path = []
	while not queue.empty():
		# obter proximo nodo com maior prioridade e verificar se e o objetivo
		current = queue.get()
		path.append(current)
		if current == goal:
			break
		# itera nodos sucessores
		for neighbor in neighbors(current):
			# custo de movimento sera altura da arvore ate o nodo atual + 1
			new_cost = cost_so_far[node_hash(current)] + 1
			# se o nodo nao estiver na lista de custos ou o custo
			# de movimento for menor que atual para aquele nodo
			if node_hash(neighbor) not in cost_so_far or new_cost < cost_so_far[node_hash(neighbor)]:
				# altera ou adiciona nodo na lista de custo contendo custo como valor
				cost_so_far[node_hash(neighbor)] = new_cost
				# adiciona nodo na fila de prioridades com prioridade sendo custo + heuristica
				priority = new_cost + heuristic(neighbor, goal)
				queue.put(neighbor, priority)
	return path