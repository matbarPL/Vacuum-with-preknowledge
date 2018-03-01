# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 20:00:48 2016

@author: Piotr
"""
import heapq
import copy as cp

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        x = [el for el in self._queue if el[2] == item]
    
        if len(x) != 0 and x[0] in self._queue:
            self._queue.remove(x[0])
            self.push(item,priority)
            return 
            
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
    
    def pushItems(self, items, priorities):
        for i in range(len(items)):
            self.push(items[i],priorities[i])
            
    def first(self):
        temp = cp.deepcopy(self)
        return temp.pop()
            
    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def popItem(self,item):
        found = False
        counter = -1
        while (counter +1< len(self._queue) and not found):
            counter +=1
            if self._queue[counter] == item:
                found = True
    
        return heapq.heappop(self._queue)[counter]

    def isEmpty(self):
        return len(self._queue) == 0 
    
    def __contains__(self,item):
        x = [el[2] for el in self._queue]
        if item in x:
            return True
        return False
        
if __name__ =='__main__':
    pq = PriorityQueue()
    pq.push((0,0),1/2)
    pq.push((1,1),1/1)
    print ((0,0) in pq)
    pq.pop()
    pq.push((1,1),1/3)
    pq.popItem(pq.first())
    print(pq._queue)
    