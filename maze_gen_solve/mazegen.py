from random import choice
from os import system
import argparse

def maze(l,w,x=0,y=0):

    direc = ((1,0,'D'),
             (-1,0,'U'),
             (0,-1,'L'),
             (0,1,'R'))
    
    oppo = {'R':'L',
            'L':'R',
            'U':'D',
            'D':'U'}
    
    ways = {}
    visited = set()        
    stack = [(x,y)]
    
    def add_random(ways):
        directions = {'R','L','U','D'}
        nodes = list(i for i in ways)
        for i in range(l):    
            node = choice(nodes)
            diff = list(directions - ways[node])
            try:
                way = choice(diff)
            except:continue
            if way=='U':
                try:
                    nodem = (node[0]-1,node[1])
                    ways[nodem].add(oppo[way])
                    ways[node].add(way) 
                except: pass
            elif way=='D':
                try:
                    nodem = (node[0]+1,node[1])
                    ways[nodem].add(oppo[way])
                    ways[node].add(way) 
                except: pass
            if way=='R':
                try:
                    nodem = (node[0],node[1]+1)
                    ways[nodem].add(oppo[way])
                    ways[node].add(way) 
                except: pass
            if way=='L':
                try:
                    nodem = (node[0],node[1]-1)
                    ways[nodem].add(oppo[way])
                    ways[node].add(way) 
                except: pass
        
        return ways
    
    def control(x,y):
        if w>x>=0 and l>y>=0 \
        and ((x,y) not in visited):
            return True
        return False
        
    while stack:
        visited.add((x,y))
        try:
            if ways[(x,y)]:
                pass
        except KeyError:
            ways[(x,y)] = set()
        check = []
        for d in direc:
            dx, dy = x+d[0],y+d[1]
            if control(dx,dy):
                check.append(d)
        if check:
            stack.append((x,y))
            di=choice(check)
            ways[(x,y)].add(di[2])
            x, y = x+di[0],y+di[1]
            ways[(x,y)] = set([oppo[di[2]]])
        else:
            x,y = stack.pop()
    return add_random(ways)

    

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('p',help='rows',type=int)
    parser.add_argument('q',help='columns',type=int)
    args= parser.parse_args()
    system('clear')
    q = args.q
    p = args.p
    #p=4
    #q=4
    c = maze(q,p)

    a = sorted([i for i in c])
    g = 0
    c[(0,0)].add('L')
    c[(p-1,q-1)].add('R')
    for i in a:
        g+=1
        if {'L','R','U','D'} == c[i]:
            print(u'\u256C',end='')
        elif {'L','R','U'} == c[i]:
            print(u'\u2569',end='')
        elif {'L','R','D'} == c[i]:
            print(u'\u2566',end='')
        elif {'L','U','D'} == c[i]:
            print(u'\u2563',end='')
        elif {'U','R','D'} == c[i]:
            print(u'\u2560',end='')
        elif {'L','R'} == c[i]:
            print(u'\u2550',end='')
        elif {'L','U'} == c[i]:
            print(u'\u255D',end='')
        elif {'R','U'} == c[i]:
            print(u'\u255A',end='')
        elif {'L','D'} == c[i]:
            print(u'\u2557',end='')
        elif {'R','D'} == c[i]:
            print(u'\u2554',end='')
        elif {'U','D'} == c[i]:
            print(u'\u2551',end='')
        elif {'D'} == c[i]:
            print(u'\u2565',end='')
        elif {'U'} == c[i]:
            print(u'\u2568',end='')
        elif {'L'} == c[i]:
            print(u'\u2561',end='')
        elif {'R'} == c[i]:
            print(u'\u255E',end='')
        if g % q==0:
            print()
