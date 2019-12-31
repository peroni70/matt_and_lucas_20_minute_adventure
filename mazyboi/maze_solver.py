
from heapq import *

class MazeRunner:

    def __init__(self, maze=None):
        if maze:
            self.maze = maze

    def set_maze(self, maze):
        self.maze = maze

    def solve_path(self,maze):
        if self.maze == None:
            raise NameError('No Maze!')
        n = len(maze.chart)
        m = len(maze.chart[0])

        #create value_map
        value_map = {i: 0 for i in enumerate(maze.target)}
        target_set = set(maze.target)
        for i in range(n):
            for j in range(m):
                if (i,j) not in target_set:
                    value_map = {(i,j): float('inf')}

        queue = [(0, i) for _, i in enumerate(maze.target)]
        visited = set()
        while queue:
            value, v = heappop(queue)
            visited.add(v)
            #check four neighbors
            for _,i in enumerate([(0,1), (1,0), (-1,0), (0,-1)]):
                neighbor = (v[0]+i[0], v[1]+i[1])
                #check if neighbor is in bounds
                if neighbor[0] >=0 and neighbor[0] < n and neighbor[1] >= 0 and neighbor[1] < m:
                    #check if neighbor is in path 
                    if maze.chart[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                        if value_map[neighbor] > value + 1:
                            value_map[neighbor] = value + 1
                            heappush(queue, (value_map[neighbor], neighbor))
        return value_map
                        



class Maze:

    def __init__(self, chart, start, target):
        self.chart = chart #2D array-like
        self.start = start #array-like indices of start node(s)
        self.target = target #array-like indices of target node(s)

class Graph:

    def __init__(self, chart, start):
        pass


