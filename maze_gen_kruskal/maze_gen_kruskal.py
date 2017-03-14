#!/usr/bin/python3
#py3.5.2

from random import shuffle,choice
from collections import defaultdict

try:
    from PIL import Image,ImageDraw
except ImportError:
    flag = 0
else:
    flag = 1

def findParent(node):
    if parent[node]!=node:
        return findParent(parent[node])
    return parent[node]

def unionNodes(node1,node2):
    ParentOfNode1 = findParent(node1)
    ParentOfNode2 = findParent(node2)
    if ParentOfNode1==ParentOfNode2:
        return False

    if rank[ParentOfNode1]>rank[ParentOfNode2]:
        parent[ParentOfNode2] = ParentOfNode1
    elif rank[ParentOfNode1]<rank[ParentOfNode2]:
        parent[ParentOfNode1] = ParentOfNode2
    else:
        parent[ParentOfNode2] = ParentOfNode1
        rank[ParentOfNode1] += 1
    return True

def vertex(l,w):
    vertexList = []
    for i in range(l):
        for j in range(w):
            if i<l-1: vertexList.append((i,j,1))
            if j<w-1: vertexList.append((i, j,7))
            parent[(i,j)] = (i,j)
            rank[(i,j)] = 0
    return vertexList

def kruskalMST(vertexList):
    while vertexList:
        *node,d = x,y,d = vertexList.pop()
        next_node = (x+ways[d][0],y+ways[d][1])
        node = tuple(node)

        if not unionNodes(node,next_node):
            maze[node].add(d)
            maze[next_node].add(~d)


def main(l,w): 
    global ways
    global maze
    global parent
    global rank
    
    maze = defaultdict(set)
    parent = dict()
    rank = dict()       #O(logN)
    
    ways = {1: (1,0),    #down
            7: (0,1),    #right
            ~1: (-1,0),  #up
            ~7: (0,-1)}  #left
    #vertical, horizontal and direction
    
    vertexList = vertex(l,w)
    shuffle(vertexList)        #random list
    kruskalMST(vertexList)
                
def drawImage(name,l,w):
    a = sorted(list(maze.keys()))
    b = list(maze.keys())
    
    #png
    for i in range((l*w)//10):
        node = choice(b)
        b.remove(node)
        maze[node].pop()
        
    image = Image.new('RGBA',(15*(w+1),15*(l+1)),(255,255,255,0))
    draw = ImageDraw.Draw(image)

    borderx, bordery = (15*(w+1)-10,
                        15*(l+1)-10)
    sx = sy = 5
    
    draw.line((sx,sy,sx,bordery),fill=(0,0,0,255),width=2)
    draw.line((sx,bordery,borderx-15,bordery),fill=(0,0,0,255),width=2) # exit
    draw.line((sx+15,sy,borderx,sy),fill=(0,0,0,255),width=2) #enterance
    draw.line((borderx,sy,borderx,bordery),fill=(0,0,0,255),width=2)
    
    for x,y in a:
        dirs = maze[(x,y)]
        m,n = (y+1)*15+sy,(x+1)*15+sx
        for i in dirs:
            if i==1:
                draw.line((m-15,n,m,n),fill=(0,0,0,255),width=2)
            if i==7:
                draw.line((m,n-15,m,n),fill=(0,0,0,255),width=2)

    image.show()
    #image.save('{}.png'.format(name),'PNG')

if __name__=='__main__':
    main(5,5)
    if flag:
        drawImage(101,5,5) #name of file,length,width
    
