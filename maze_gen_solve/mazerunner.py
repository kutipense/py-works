from time import sleep
import mazegen
import argparse
from random import choice
from os import system
from copy import deepcopy

def depth(mazem,start):
    M = mazem
    r, c = start[0], start[1]
    node = (r,c)
    graph = dict((node,set()) for node in M)
    checked = set()
    history = list()
    stack = list(); stack.append(start);
    look = 'O'
    new_look = look 
    oppo = {'A':('<','V'),'<':('A','>'),'>':('A','<'),'V':('<','A')}
    def move(node,side):
        if side=='R':
            if look == '<':
                n_look = ('V','>')
            else:
                n_look = '>'
            c = node[1]+1
            node_new = (node[0],c)
        elif side=='L':
            if look == '>':
                n_look = ('V','<')
            else:
                n_look = '<'
            c = node[1]-1
            node_new = (node[0],c)
        elif side=='U':
            if look == 'V':
                n_look = ('>','A')
            else:
                n_look = 'A'
            r = node[0]-1
            node_new = (r,node[1])
        elif side=='D':
            if look == 'A':
                n_look = ('>','V')
            else:
                n_look = 'V'
            r = node[0]+1
            node_new = (r,node[1])
        return node_new,n_look
    p = -1    
    while stack: 
        checked.add(node)
        ways = []
        
        for side in M[node]:
            node_new,_ = move(node,side)
            graph[node].add(node_new)
            if node_new not in checked:
                ways.append(side)
        if ways:
            p=-1
            stack.append(node)
            if len(ways)>1:
                stack.append(0)
            side = ways.pop()
            node_n,new_look = move(node,side)
            if isinstance(new_look,tuple):
                history.append((node,(look,*new_look)))
                look = new_look[1]
            else:
                history.append((node,(look,new_look)))
                look = new_look
            node = node_n
        else:
            stack.reverse()
            try:
                tmp = stack.index(0)
            except ValueError:
                break
            trgt = len(stack)-tmp-1
            stack.reverse()
            return_path = dijkstra(node,stack[trgt-1],graph)
            history.append((node,(look,*oppo[look])))
            history.extend(parse_road(return_path))
            stack = stack[:trgt]
            node = stack[-1]
            
    return graph,history

def parse_road(path):
    path.reverse()
    his = list()
    lookk = 'O'
    for i in range(len(path)-1):
        x = path[i][0] - path[i+1][0]
        y = path[i][1] - path[i+1][1]
        if x==1:
            his.append((path[i],('V',lookk)))
            lookk='V'
        elif x==-1:
            his.append((path[i],('A',lookk)))
            lookk='A'            
        elif y==1:
            his.append((path[i],('>',lookk)))
            lookk='>'
        elif y==-1:
            his.append((path[i],('<',lookk)))
            lookk='<'
    his[0]=(his[0][0],(his[0][1][0],his[0][1][0]))
    his.reverse()
    return his
    
def road(start,end,parent):
    road = [end]                               #path
    while road[-1] != start:      
        road.append(parent[road[-1]])         #add the parent of last node
    road.reverse()
    return road
    
def distance_parent(node,next_node,distances,parent):
    distance = distances[node] + 1       #distance + next node's distance
    if distance<distances[next_node]:
        distances[next_node] = distance  #distance
        parent[next_node] = node        #parent
       
def dijkstra(start,end,parents):
    parent = dict()
    nodes = [i for i in parents]
    distances = dict([(node,10000) for node in nodes])
    distances[start] = 0
    while nodes:          #check later
        current_node = min(nodes, key=distances.__getitem__)
        nodes.remove(current_node)
        if current_node==end:
            return road(start,end,parent)                 #shortest path
        for node in parents[current_node]:
            if node in nodes:
                distance_parent(current_node,node,distances,parent)    

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('s',help='sleep_ms',type=int)
    parser.add_argument('p',help='rows',type=int)
    parser.add_argument('q',help='columns',type=int)
    parser.add_argument('-hi',help='history',action='store_true')
    parser.add_argument('-d',help='dijkstra',action='store_true')
    parser.add_argument('-g',help='graph',action='store_true')
    args= parser.parse_args()
    system('clear')
    q = args.q
    p = args.p
    
    w, l = p, q
    end = (w-1,l-1)
    start = (0,0)
    maze = mazegen.maze(l,w) 
    graph,history = depth(maze,start)                  
    M = maze
    M[start].add('L')
    M[end].add('R')
    a = sorted([i for i in M])
    g = 0
  
    for hii in history:
        M = deepcopy(maze)
        M[hii[0]] = hii[1]
        for looky in hii[1]:
            system('clear')
            for i in a:
                g+=1
                if {'L','R','U','D'} == M[i]:
                    print(u'\u256C',end='')
                elif {'L','R','U'} == M[i]:
                    print(u'\u2569',end='')
                elif {'L','R','D'} == M[i]:
                    print(u'\u2566',end='')
                elif {'L','U','D'} == M[i]:
                    print(u'\u2563',end='')
                elif {'U','R','D'} == M[i]:
                    print(u'\u2560',end='')
                elif {'L','R'} == M[i]:
                    print(u'\u2550',end='')
                elif {'L','U'} == M[i]:
                    print(u'\u255D',end='')
                elif {'R','U'} == M[i]:
                    print(u'\u255A',end='')
                elif {'L','D'} == M[i]:
                    print(u'\u2557',end='')
                elif {'R','D'} == M[i]:
                    print(u'\u2554',end='')
                elif {'U','D'} == M[i]:
                    print(u'\u2551',end='')
                elif {'D'} == M[i]:
                    print(u'\u2565',end='')
                elif {'U'} == M[i]:
                    print(u'\u2568',end='')
                elif {'L'} == M[i]:
                    print(u'\u2561',end='')
                elif {'R'} == M[i]:
                    print(u'\u255E',end='')
                elif isinstance(M[i],tuple):
                    print(looky,end='')
                if g % l ==0:
                    print()
            sleep(args.s/100)
    print('----------------------------------------------------------')
    if args.hi:    
        for i in history:
            print((str(i[0])+' '+str(i[1])).ljust(9),end=', ')
        print('\n----------------------------------------------------------')
    if args.d:
        M = deepcopy(maze)
        dij = dijkstra(start,end,graph)
        for i in a:
            if {'L','R','U','D'} == M[i]:
                maze[i] = u'\u256C'
            elif {'L','R','U'} == M[i]:
                maze[i] = u'\u2569'
            elif {'L','R','D'} == M[i]:
                maze[i] = u'\u2566'
            elif {'L','U','D'} == M[i]:
                maze[i] = u'\u2563'
            elif {'U','R','D'} == M[i]:
                maze[i] = u'\u2560'
            elif {'L','R'} == M[i]:
                maze[i] = u'\u2550'
            elif {'L','U'} == M[i]:
                maze[i] = u'\u255D'
            elif {'R','U'} == M[i]:
                maze[i] = u'\u255A'
            elif {'L','D'} == M[i]:
                maze[i] = u'\u2557'
            elif {'R','D'} == M[i]:
                maze[i] = u'\u2554'
            elif {'U','D'} == M[i]:
                maze[i] = u'\u2551'
            elif {'D'} == M[i]:
                maze[i] = u'\u2565'
            elif {'U'} == M[i]:
                maze[i] = u'\u2568'
            elif {'L'} == M[i]:
                maze[i] = u'\u2561'
            elif {'R'} == M[i]:
                maze[i] = u'\u255E'
        for h in dij:
           maze[h] = '\033[91m' + maze[h] + '\033[0m'
        for i in a:
            print(maze[i],end='')
            g+=1
            if g % l ==0:
               print()
       
        print('\n----------------------------------------------------------')
    if args.g:
        print(*graph.items(),sep='\n')
        print('\n----------------------------------------------------------')
    
    #print(history)
