# -*- coding: utf-8 -*-
from Robot import *
import random as r
import Graph as g
from matplotlib import pyplot as plt
import pylab 
import imageio
import os
import shutil
import subprocess
from math import sqrt
from ourQueue import *

class Board():
    def __init__(self, n, nObst, nDirt):
        self.n = n
        self.nObst = nObst
        self.nDirt = nDirt
        self.lObst = self.genObst()
        self.lAvail = self.genAvail()
        self.lDirt = r.sample(self.lAvail,nDirt)
        self.robot = Robot(n,self.lAvail)
    
    def genAvail(self):
        gridpoints = []
        for i in range(self.n):
            for j in range(self.n):
                gridpoints.append((i,j))
                
        return [x for x in gridpoints if x not in self.lObst]
        
    def genObst(self):
        temp = set(zip([r.randint(0,self.n-1) for i in range(self.nObst)],\
                        [r.randint(0,self.n-1) for i in range(self.nObst)]))
        while (len(temp) !=self.nObst):
            temp = list(temp)
            temp.append((r.randint(0,self.n-1),r.randint(0,self.n-1)))
            temp = set(temp)
   
        return list(temp)
        
    def checkMoves(self,square):
        possMoves = []
        lMoves = [(-1,0),(1,0),(0,1),(0,-1)]
        for item in lMoves:
            move = tuple(map(sum, zip(self.pos, item)))
            if move in self.lAvail:
                possMoves.append(move)
        
    def draw(self,moves,pos,path,keepPictures = False, gif=True):
        ex = 0.001
        x,y = [i for i in range(self.n)], [i for i in range(self.n)]
        positions = [(i[0]+0.5,i[1]+0.5) for i in moves]
                     
        if (gif ==True):
            try: 
                os.makedirs(path[:-1])
            except OSError:
                if os.path.isdir(path[:-1]):
                    shutil.rmtree(path[:-1])
                    os.makedirs(path[:-1])
                    
        filenames = []
        for i in range(len(moves)):
            printProgressBar(i,len(moves)-1,"Progress","Creating gif")
            fig = plt.gcf()
            
            fig.set_size_inches(8, 8)
            plt.axis([0-ex, self.n+ex, 0-ex, self.n+ex])
            
            plt.gca().set_aspect('equal', adjustable='box')
            plt.grid(True,color = 'k')
            
            plt.gca().patch.set_facecolor('0.8')
            
            ox,oy = [x[0] + 0.5 for x in self.lObst], [x[1] + 0.5 for x in self.lObst]
            dx,dy = [x[0] + 0.5 for x in self.lDirt], [x[1] + 0.5 for x in self.lDirt]
            
            plt.plot(ox,oy,'ys',markersize=8/self.n*55)
            plt.plot(dx,dy,'k8',markersize=8/self.n*55)
            
            ax, ay = [x[0] for x in positions[:i+1]], [x[1]  for x in positions[:i+1]]
            
            plt.plot(ax,ay,'rs',markersize=8/self.n*55)
            plt.plot(positions[i][0],positions[i][1],'wo',markersize=8/self.n*30)
            f = path+str(i)+'.png'
            pylab.savefig(f)
            filenames.append(f)  
            plt.close()
            
        if (gif == True):
            images = []
            for filename in filenames:
                images.append(imageio.imread(filename))
            imageio.mimsave(path+'oursearch.gif', images,fps = int(sqrt(len(moves))/2))
            
        if (not keepPictures):
            for filename in filenames:
                os.remove(filename)
        subprocess.call(path+'oursearch.gif',shell=True)
        
    def drawGraph(self, moves, pos, graph, path, keepPictures = False, gif=False):
        
        filenames = []
        filenames2 = []
        prevVert = []
        currVert = []

        for i in range(len(moves)):
            printProgressBar(i,len(moves)-1,"Progress","Creating graph")
            prevVert = currVert
            currVert = graph.getVertex(moves[i])
            currVert.setColor('brown')
            if prevVert:
                prevVert.setColor('red')
            graph.makeDotGraph(str(i),path)
            filenames.append(path+str(i)+'.png')
            filenames2.append(path+str(i))
        if (gif):
            images = []
            for filename in filenames:
                images.append(imageio.imread(filename))
            imageio.mimsave(path+'graph.gif', images,fps = 6)
        if (not keepPictures):
            for i in range(len(filenames)):
                os.remove(filenames[i])
                os.remove(filenames2[i])
        subprocess.call(path+'graph.gif',shell=True)
            
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 70, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

    if iteration == total: 
        print()
            
        
def search(n,nObst,nDirt,path,gif=False, makeGraph = False,counter = 0):
    if (counter == 0):
        print('Board ' + str(n) + ' x ' + str(n) +'.\n')
        print(str(nObst) + ' obstacles on the board.\n')
        print(str(nDirt) + ' dirts on the board.\n')
        dec = input(path + ' is the location where your gif files will be created.'\
              + 'If in your comupter this path already exists it will be replaced by the new folder.\n'\
              + 'Do you want to continue? [Y]\[N] \n')
        while (dec not in ['y', 'Y','n','N']):
            dec = input('Please the correct letter!\n' + path +\
                 ' is the location where your gif files will be created.'\
              + 'If in your comupter this path already exists it will be replaced by the new folder.\n'\
              + 'Do you want to continue? [Y]\[N] \n')
       
        while (dec in ['n','N']):     
            path = input ('Please type in a new path.\n')
            
            dec = input(path + ' is the location where your gif files will be created. '\
              + 'If in your comupter this path already exists, it will be replaced by the new folder.\n'\
              + 'Do you want to continue? [Y]\[N] \n')        
    board = Board(n,nObst,nDirt)
    robot = Robot(n,board.lAvail)
    graph = g.Graph()
    start = robot.pos
    graph.addVertex(robot.pos)
    graph.getVertex(start).setColor('green')   
    sortAvail = sorted(board.lAvail)
    queue = ourQueue()
    queue.enqueueItems(robot.getPossMoves())
    while not queue.isEmpty(): 
        
        possMoves = robot.getPossMoves()
        
        queue.enqueueItems(possMoves)
        for item in possMoves:
            graph.addEdge(robot.pos, item)
            graph.addEdge(item,robot.pos)
        robot.move(queue.dequeue())
        
    if sortAvail == sorted(list(graph.getVertices())):
        moves = graph.ourSearch(start,n,nObst)
        print (len (moves))

        if (gif):
            board.draw(moves,start,path,True,gif)
        if (makeGraph):
            board.drawGraph(moves, start, graph, path,False, makeGraph)
        return   
    else:
        print('Obstacles in the wrong positions!\n Trying once again!')
        counter +=1
        search(n,nObst,nDirt,path,gif, makeGraph,counter)
        return

if __name__ == '__main__':
    path = 'C:/Users/Mateusz/Desktop/Agent/gif/' #type your path in here! 
    search(10,15,3,path,True,False)    
    