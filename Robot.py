# -*- coding: utf-8 -*-
import random as r

class Robot():
    def __init__(self,n,lAvail):
        self.n = n
        self.visited = []
        self.lAvail = lAvail
        self.pos = self.genPos()
        
    def genPos(self):
        return r.sample(self.lAvail,1)[0]
    
    def move(self,corr):
        self.pos = corr
        
    def getPossMoves(self):
        possMoves = []
        lMoves = [(-1,0),(1,0),(0,1),(0,-1)]
        for item in lMoves:
            move = tuple(map(sum, zip(self.pos, item)))
            if move in self.lAvail:
                possMoves.append(move)
                
        return possMoves
