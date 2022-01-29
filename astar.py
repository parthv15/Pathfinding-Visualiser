import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* PathFinding Algorithm")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node: 
	def __init__(self,rows,cols,width,total_rows): 
		self.rows = rows
		self.cols = cols
		self.x = rows * width
		self.y = cols * width
		self.color = WHITE
		self.neighbours = []
		self.width = width
		self.total_rows = total_rows

	
	def makeClosed(self): 
		self.color = RED

	def makeOpen(self):
		self.color = GREEN

	def makeWall(self):
		self.color = BLACK

	def makeStart(self):
		self.color = ORANGE

	def makeEnd(self):
		self.color = TURQUOISE

	def isClosed(self): 
		return self.color == RED

	def isOpen(self):
		return self.color == GREEN

	def isWall(self):
		return self.color == BLACK

	def isStart(self):
		return self.color == ORANGE

	def isEnd(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def makePath(self):
		self.color = PURPLE

	def getPosition(self): 
		return self.rows, self.cols

	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

	def updateNeighbors(self,grid):
		self.neighbours = []
		if self.rows < self.total_rows-1 and not grid[self.rows+1][self.cols].isWall(): #down
			self.neighbours.append(grid[self.rows+1][self.cols])

		if self.rows > 0 and not grid[self.rows - 1][self.cols].isWall(): #up
			self.neighbours.append(grid[self.rows - 1][self.cols])

		if self.cols < self.total_rows-1 and not grid[self.rows][self.cols + 1].isWall(): #right
			self.neighbours.append(grid[self.rows][self.cols + 1])

		if self.cols > 0 and not grid[self.rows][self.cols - 1].isWall(): #left
			self.neighbours.append(grid[self.rows][self.cols - 1])

	def __lt__(self,other):
		return False

#use manhattan distance
def H(p1,p2):
	x1, y1 = p1
	x2, y2 = p2

	return abs(x1 - x2) + abs(y1 - y2)


def createPath(parent,curr,draw):

	while curr in parent:
		curr = parent[curr]
		curr.makePath()
		draw()



def aStarAlgorithm(draw,grid,start,end):

	pq = PriorityQueue()
	count = 0

	pq.put((0,count,start))
	parent = {}

	gScore = {node : float("inf") for row in grid for node in row}
	gScore[start] = 0

	fScore = {node : float("inf") for row in grid for node in row}
	fScore[start] = H(start.getPosition(),end.getPosition())

	pq_hash = {start}

	while not pq.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		curr = pq.get()[2]
		pq_hash.remove(curr)

		if curr == end: 
			createPath(parent,end,draw)
			end.makeEnd()
			return True

		for neighbour in curr.neighbours:
			temp_gScore = gScore[curr] + 1

			if temp_gScore < gScore[neighbour]:
				parent[neighbour] = curr
				gScore[neighbour] = temp_gScore

				fScore[neighbour] = temp_gScore + H(neighbour.getPosition(),end.getPosition())

				if neighbour not in pq_hash:
					count += 1
					pq.put((fScore[neighbour],count,neighbour))
					pq_hash.add(neighbour)
					neighbour.makeOpen()

		draw()

		if curr != start: 
			curr.makeClosed()

	return False

def makeGrid(rows,width):
	grid = []
	gap = width // rows

	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i,j,gap,rows)
			grid[i].append(node)


	return grid

def drawGrid(win,rows,width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win,GREY,(0,i * gap),(width, i * gap))
		for j in range(rows):
			pygame.draw.line(win,GREY,(j * gap,0),(j * gap,width))


def draw(win,grid,rows,width):
	win.fill(WHITE)

	for row in grid:
		for nodes in row:
			nodes.draw(win)


	drawGrid(win,rows,width)
	pygame.display.update()


#mouse position: 
def getClickedPosition(pos,rows,width):
	gap = width // rows
	y,x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(win, width):
	ROWS = 50
	
	grid = makeGrid(ROWS,width)

	start = None
	end = None

	run = True

	while run: 
		draw(win,grid,ROWS,width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: 
				pos = pygame.mouse.get_pos()
				row,col = getClickedPosition(pos,ROWS,width)

				node = grid[row][col]

				if not start and node != end: 
					start = node
					start.makeStart()

				elif not end and node != start:
					end = node
					end.makeEnd()

				elif node != end and node != start:
					node.makeWall() 

			elif pygame.mouse.get_pressed()[2]: 
				pos = pygame.mouse.get_pos()
				row,col = getClickedPosition(pos,ROWS,width)
				node = grid[row][col]
				node.reset()

				if node == start:
					start = None
				elif node == end:
					end = None 



			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for nodes in row:
							nodes.updateNeighbors(grid)

					aStarAlgorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)	

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = makeGrid(ROWS,width)


	pygame.quit()


main(WIN,WIDTH)











