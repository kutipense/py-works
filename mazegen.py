import random
import sys


class Node():
    def __init__(self, *args, **kwargs):
        self.isVisited = False
        self.type = 0 # 0: wall, 1: free space

    def __str__(self):
        return str(self.type)

class MazeGen():
    directions = (
        (2,0,1,0),
        (0,2,0,1),
        (-2,0,-1,0),
        (0,-2,0,-1)
    )

    def __init__(self, size):
        self.maze = [[Node() for _ in range(size)] for _ in range(size)]

    def __str__(self):
        return ''.join([''.join(map(str,i)) for i in self.maze])

    def control(self,x,y):
        return 0<x<size and 0<y<size and not self.maze[x][y].isVisited

    def generate(self,x,y):
        self.maze[x][y].isVisited = True
        self.maze[x][y].type = 1

        adjancents = []

        for x_n, y_n, x_, y_ in self.directions:
            dx, dy = x+x_n, y+y_n
            if self.control(dx,dy):
                adjancents.append((dx,dy,x_, y_))

        if adjancents:
            random.shuffle(adjancents)
            for x_next, y_next, x_, y_ in adjancents:
                if not self.maze[x_next][y_next].isVisited:
                    self.maze[x+x_][y+y_].type = 1
                    self.generate(x_next, y_next)


if __name__=='__main__':
    size = int(sys.argv[1])
    size += not size%2
    generator = MazeGen(size)
    generator.generate(1,1)
    with open('random.maze','w') as f:
        print(size,generator,sep='\n',file=f)
