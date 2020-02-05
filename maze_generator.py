import pygame
import time
import random
pygame.init()


SCREEN_SIZE = 501
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Maze")
width = 25


WHITE = (255,255,255)
GREY = (200,200,200)
BLACK = (0,0,0)
BLUE = (90,200,255)
RED = (255,0,0)


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

    def draw(self):
        x = self.x * width
        y = self.y * width

        color = BLACK if self.walls['N'] else GREY
        draw_line(screen, color, (x, y), (x + width, y), 1)
        color = BLACK if self.walls['S'] else GREY
        draw_line(screen, color, (x, y + width), (x + width, y + width), 1)
        color = BLACK if self.walls['E'] else GREY
        draw_line(screen, color, (x + width, y), (x + width, y + width), 1)
        color = BLACK if self.walls['W'] else GREY
        draw_line(screen, color, (x, y), (x, y + width), 1)


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
            cell.draw()
            pygame.draw.rect(screen, BLUE, ((cell.x * width) + 5, (cell.y * width) + 5, width-10, width-10))
            neighbors = self.unvisited_neighbors(cell)
            if neighbors:
                stack.append(cell)
                direction, next_cell = random.choice(neighbors)
                cell.remove_wall(next_cell, direction)
                cell.draw()
                pygame.draw.rect(screen, GREY, ((cell.x * width) + 2, (cell.y * width) + 2, width - 4, width - 4))
                stack.append(next_cell)

    def clear_rects(self):
        for col in self.maze:
            for cell in col:
                pygame.draw.rect(screen, GREY, ((cell.x * width) + 2, (cell.y * width) + 2, width - 4, width - 4))
        pygame.display.flip()


def draw_line(surface, color, start_pos, end_pos, line_width):
    pygame.draw.line(surface, color, start_pos, end_pos, line_width)
    pygame.display.flip()
    time.sleep(.005)


def main():
    screen.fill(GREY)

    # Create maze and generate the full-on maze
    maze_size = int(SCREEN_SIZE/width)
    maze_generator = Maze(size_x=maze_size, size_y=maze_size)
    maze_generator.dfs_generate()
    maze_generator.clear_rects()

    keep_running = True

    while keep_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False


main()
pygame.quit()
