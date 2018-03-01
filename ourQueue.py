# -*- coding: utf-8 -*-
from kolejka import *

class ourQueue(Queue):
    def __init__(self):
        super().__init__()
        self.all = []
        
        
    def enqueue(self, item):
        self.items.insert(0,item)
        if item not in self.all:
            self.all.append(item)
            
    def enqueueItems(self, items):
        for el in items:
            if el not in self.all:
                self.enqueue(el)
    