import sys
import eight_puzzle as ep

def print_node(cells):
	for x in range(0, 9):
		sys.stdout.write(str(cells[x]) + ('\n' if (x + 1) % 3 == 0 else ' '))

path = ep.solve([8,1,3,2,4,5,0,7,6], [0,1,3,8,2,4,7,6,5])

for node in path:
	print_node(node)
	print('-----')