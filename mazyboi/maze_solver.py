
from heapq import *
import tkinter as tk
from PIL import Image, ImageTk
import math
global xs, ys, xt, yt
count = 0

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
                min_dist = value_map[i]

        if min_dist==float('inf'):
            raise NameError('No valid path!')

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

            if math.isinf(dist_next_node):
                raise NameError("No valid path!")
                
            path.append(next_node)
            current_node = next_node

        return path
    
    def draw_path(self, path=None):
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
        if path:
            for _, i in enumerate(path):
                x = i[1]
                y = i[0]
                if (y,x) not in self.maze.target and (y,x) not in self.maze.start:
                    rgb_teal = (51, 255, 255)
                    picture.putpixel((x,y), rgb_teal)

        #TODO: Also incorporate this new size into parameters later too lazy now
        #new_size = (500, 500)
        #picture = picture.resize(new_size, Image.NEAREST)
        picture.save("Maze_Soln", "png")

    # Creates a 2d-array-like chart of a given maze image
    # using a thresholding method.
    def create_maze_from_image(self, image):
        width, height = image.size
        chart = [[1 for i in range(width)] for j in range(height)]
        for i in range(height):
            for j in range(width):
                pix = image.getpixel((j,i))
                if sum(pix)/len(pix) > 240 :
                    chart[i][j] = 0
        return chart

    def _callback(self, event):
        global count, xs, ys, xt, yt
        if count == 0:
            xs = event.x
            ys = event.y
        elif count == 1:
            xt = event.x
            yt = event.y
        count +=1
        print("clicked at", event.x, event.y) 

    def create_gui(self, image_path):
        root = tk.Tk()
        # load image
        image = Image.open(image_path)
        image = image.convert("RGB")

        root.geometry('750x750')
        #TODO resizing?
        out = image.resize((750,750))
        photo = ImageTk.PhotoImage(out)

        # label with image
        l = tk.Label(root, image=photo)
        l.pack()

        # bind click event to image
        l.bind('<Button-1>', self._callback)

        # button with image binded to the same function 
        b = tk.Button(root, image=photo, command=self._callback)
        b.pack()

        # button with text closing window
        b = tk.Button(root, text="Close", command=root.destroy)
        b.pack()

        # "start the engine"
        root.mainloop()

        # create the maze with start and target 
        start = [(ys,xs)]
        target = [(yt,xt)]
        chart = self.create_maze_from_image(out)
        maze = Maze(chart, start, target)

        # set maze
        self.maze = maze

class Maze:

    def __init__(self, chart, start, target):
        self.chart = chart #2D array-like
        self.start = start #array-like indices of start node(s)
        self.target = target #array-like indices of target node(s)



#!TESTY BOI
if __name__ == '__main__':
    solver1 = MazeRunner()
    solver1.create_gui("mazyboi/artistic_maze.png")
    value_map1 = solver1.label_path()
    path = solver1.find_path(value_map1)
    print(path)
    solver1.draw_path(path)