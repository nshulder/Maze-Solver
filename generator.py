import random


class Edge:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class Cell:
    opposite_wall = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        # x, y position in grid
        self.x = x
        self.y = y
        # Explicitly define direction: bool to cut down on confusion
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def been_visited(self):
        # First action we take when visiting a new cell is knock down a wall, so not visited if it has all walls
        return not(all(self.walls.values()))

    def remove_wall(self, other, direction):
        # Remove both walls between two cells
        self.walls[direction] = False
        other.walls[Cell.opposite_wall[direction]] = False


class Maze:
    def __init__(self, size_x=15, size_y=15, start_x=0, start_y=0):
        self.start_x = start_x
        self.start_y = start_y
        self.size_x = size_x
        self.size_y = size_y
        self.maze = [[Cell(x, y) for y in range(size_y)] for x in range(size_x)]

    def unvisited_neighbors(self, cell):
        delta = [('N', (0, -1)),
                 ('S', (0, 1)),
                 ('E', (1, 0)),
                 ('W', (-1, 0))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.size_x) and (0 <= y2 < self.size_y):
                neighbour = self.maze[x2][y2]
                if not(neighbour.been_visited()):
                    neighbours.append((direction, neighbour))
        return neighbours

    def dfs_generate(self):
        # Use a list as a 'stack' data structure
        stack = [self.maze[self.start_x][self.start_y]]

        # Following iterative backtracking method algorithm for maze generation on Wikipedia
        while not(len(stack) == 0):
            cell = stack.pop()
            neighbors = self.unvisited_neighbors(cell)
            if neighbors:
                stack.append(cell)
                direction, next_cell = random.choice(neighbors)
                cell.remove_wall(next_cell, direction)
                stack.append(next_cell)


maze = Maze()
maze.dfs_generate()
