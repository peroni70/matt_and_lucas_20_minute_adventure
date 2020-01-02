
from heapq import *
from PIL import Image

class MazeRunner:

    def __init__(self, maze=None):
        if maze:
            self.maze = maze

    def set_maze(self, maze):
        self.maze = maze

    def label_path(self):
        if self.maze.chart == None:
            raise NameError('No Maze!')
        n = len(self.maze.chart)
        m = len(self.maze.chart[0])

        #create value_map
        value_map = {i: 0 for _, i in enumerate(self.maze.target)}
        target_set = set(self.maze.target)
        for i in range(n):
            for j in range(m):
                if (i,j) not in target_set:
                    value_map[(i,j)] = float('inf')
        queue = [(0, i) for _, i in enumerate(self.maze.target)]
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
                    if self.maze.chart[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                        if value_map[neighbor] > value + 1:
                            value_map[neighbor] = value + 1
                            heappush(queue, (value_map[neighbor], neighbor))
        return value_map

    #find the shortest path
    def find_path(self, value_map):
        #dimensions of maze
        n = len(self.maze.chart)
        m = len(self.maze.chart[0])

        min_dist = float('inf')
        for _, i in enumerate(self.maze.start):
            if value_map[i] < min_dist:
                start_node = i
        
        current_node = start_node
        path = [start_node]
        
        while current_node not in self.maze.target:
            dist_next_node = float('inf')
            
            for _, i in enumerate([(0,1), (1,0), (-1,0), (0,-1)]):
                neighbor = (current_node[0]+i[0], current_node[1]+i[1])
                #check if neighbor is in bounds
                if neighbor[0] >=0 and neighbor[0] < n and neighbor[1] >= 0 and neighbor[1] < m:
                    if value_map[neighbor] < dist_next_node:
                        dist_next_node = value_map[neighbor]
                        next_node = neighbor
            
            path.append(next_node)
            current_node = next_node

        return path
    
    def draw_path(self, path):
        chart = self.maze.chart
        height = len(chart)
        width = len(chart[0])
        dimensions = (height, width)
        
        picture = Image.new("RGB", dimensions, 0)

        for r in range(height):
            for c in range(width):
                if chart[r][c] == 1:
                    rgb_black = (0,0,0)
                    picture.putpixel((c,r), rgb_black)
                else:
                    if (r,c) in self.maze.target:
                        rgb_green = (0, 102, 0)
                        picture.putpixel((c,r), rgb_green)
                    elif (r,c) in self.maze.start:
                        rgb_red = (153, 0, 0)
                        picture.putpixel((c,r), rgb_red)
                    else:
                        rgb_white = (255, 255, 255)
                        picture.putpixel((c,r), rgb_white)
        
        for _, i in enumerate(path):
            x = i[1]
            y = i[0]
            if (y,x) not in self.maze.target and (y,x) not in self.maze.start:
                rgb_teal = (51, 255, 255)
                picture.putpixel((x,y), rgb_teal)

        #TODO: Also incorporate this new size into parameters later too lazy now
        new_size = (500, 500)
        picture = picture.resize(new_size, Image.NEAREST)
        picture.save("Maze_Soln", "png")



class Maze:

    def __init__(self, chart, start, target):
        self.chart = chart #2D array-like
        self.start = start #array-like indices of start node(s)
        self.target = target #array-like indices of target node(s)

class Graph:

    def __init__(self, chart, start):
        pass

#!TESTY BOI
if __name__ == '__main__':
    chart1 = [[1,0,0,1], [1,0, 0, 1], [1,0,1,1], [0, 0 , 1, 1]]
    start1 = [(3,0)]
    target1 = [(0,1), (0,2)]
    maze1 = Maze(chart1, start1, target1)
    solver1 = MazeRunner(maze1)
    value_map1 = solver1.label_path()
    path = solver1.find_path(value_map1)
    print(path)