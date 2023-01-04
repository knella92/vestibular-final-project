""" Package that solves the maze

Input
    maze - An array of the maze map with the walls and free space points assigned a certain value
    start - The index of the start point
    end - The index of the end point

Output 
    x_list - list of first indices of the calculated trajectory
    y_list - list of second indices of the calculated trajectory
"""

from re import X
import numpy as np
import matplotlib.pyplot as plt

class Solver():

    def __init__(self, maze):
        """ 
        Init function
        
        INPUTS: 
            maze (np.array) ~ mask containing walls of the maze as nonzero
        OUTPUTS:
            none
        """
        self.maze = maze
        self.wall_cost_function = np.zeros(np.shape(maze))
        self.goal_cost_function = np.zeros(np.shape(maze))-1
        self.x_list = []
        self.y_list = []
        self.neighbors = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]


    def goal_cost(self, goal):
        """ 
        Iterates over map to generate path cost map instance variable
        
        INPUTS: 
            goal (np.array) ~ goal cell
        OUTPUTS:
            none
        """

        queue = [(goal[0], goal[1])]
        self.goal_cost_function[goal[1]][goal[0]] = 0
        n = 0
        while len(queue) > 0:
            n = n+1
            index = queue.pop(0)
            goal_cost = self.goal_cost_function[index[1]][index[0]]
            for shift in self.neighbors:
                xs = index[0] + shift[0]
                ys = index[1] + shift[1]
                try:
                    if self.goal_cost_function[ys][xs] == -1 and self.maze[ys][xs] == 0:
                        self.goal_cost_function[ys][xs] = goal_cost + 1 + self.wall_cost_function[ys][xs]
                        queue.append((xs, ys))

                except:
                    pass
        print(n)

    def wall_cost(self):
        """ 
        Iterates over map to generate wall cost map instance variable
        
        INPUTS: 
            none
        OUTPUTS:
            none
        """
        (y, x) = np.where(self.maze>0)
        walls = [(x[i],y[i]) for i in range(len(y))]
        queue = walls.copy()
        n=0
        while len(queue) > 0:
            index = queue.pop(0)
            cost = self.wall_cost_function[index[1]][index[0]]
            for shift in self.neighbors:
                xs = index[0] + shift[0]
                ys = index[1] + shift[1]

                if xs < 0 or ys < 0:
                    continue
                try:
                    if self.maze[ys][xs] == 0 and self.wall_cost_function[ys][xs] == 0:
                        self.wall_cost_function[ys][xs] = cost + 1
                        queue.append((xs, ys))
                        print(cost-0.5)
                        
                except Exception as e:
                    pass
        self.wall_cost_function = (np.max(self.wall_cost_function) - self.wall_cost_function)**2
            

    def descend(self, cur):
        """ 
        Iterates over cost map to generate path
        
        INPUTS: 
            cur (np.array) ~ start cell
        OUTPUTS:
            none
        """
        queue = [cur]
        while True:
            index = queue.pop(0)
            if self.maze[index[1]][index[0]] == 0:
                cur = (index[0], index[1])
                break
            else:
                for shift in self.neighbors:
                    queue.append((index[0]+shift[0], index[1]+shift[1]))
        x = cur[0]
        y = cur[1]
        print(x)
        print(y)
        cost = self.goal_cost_function[y][x]
        
        while not self.goal_cost_function[y][x] == 0:
            print(x, y)
            lastx=x
            lasty=y
            self.x_list.append(x)
            self.y_list.append(y)
            n_x = x
            n_y = y
            for shift in self.neighbors:
                if y+shift[1]<0 or x+shift[0]<0:
                    continue
                try:
                    n_cost = self.goal_cost_function[y+shift[1]][x+shift[0]]
                    if n_cost < cost and n_cost > 0:
                        cost = n_cost
                        n_x = x+shift[0]
                        n_y = y+shift[1]
                except:
                    pass
            x = n_x
            y = n_y
            if lastx == x and lasty == y:
                break

        self.x_list.append(x)
        self.y_list.append(y)
        self.path = np.zeros(np.shape(self.maze))
        for i in range(len(self.x_list)):
            self.path[self.y_list[i]][self.x_list[i]] = 255

    def solve_maze(self, start, end):
        """ 
        Solves a maze
        
        INPUTS: 
            start (np.array) ~ start cell
            end (np.array) ~ end cell
        OUTPUTS:
            none
        """
        self.wall_cost()
        print("Wall done!")
        self.goal_cost(end)
        print(self.maze)
        print(self.goal_cost_function)
        self.descend(start)
        return (self.x_list, self.y_list)
    
    def solve_follow(self, start, end):
        """ 
        Follows a line by maze solving an inverted maze.
        
        INPUTS: 
            start (np.array) ~ start cell
            end (np.array) ~ end cell
        OUTPUTS:
            none
        """
        maze_temp = self.maze
        inv_maze = np.zeros(np.shape(self.maze))
        inv_maze = np.where(self.maze == -1, 0, inv_maze)
        inv_maze = np.where(self.maze == 0, -1, inv_maze)
        self.maze = inv_maze
        response = self.solve_maze(start, end)
        self.maze = maze_temp
        return response




            


                    
                