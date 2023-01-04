"""
Unittest for the maze_solve package

Inputs
    Solver - calls the Solver class in the maze_solve package

"""
import rospy
import unittest
from maze_solve import Solver
import numpy as np

class MazeTest(unittest.TestCase):
    def small_maze_test(self):
        """ Tests if the maze_solver solves this maze and returns the x and y indices
            as a list
        """
        maze = np.array([[0,0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]
                        ])
        solver = Solver(maze)
        start = np.array([1, 1])
        end = np.array([5,6])

        (x_path, y_path) = solver.solve_maze(start, end)
        print(x_path)
        print(y_path)
        self.assertEquals(x_path,[1, 2, 3, 3, 4, 4])
        self.assertEquals(y_path,[1, 2, 3, 4, 5, 5])


if __name__ == "__main__":
    import rosunit
    rosunit.unitrun('balance_board', 'MazeTest', MazeTest)