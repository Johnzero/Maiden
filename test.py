#!/usr/bin/env python

import threading
import string
from time import time
import itertools


PrinTable = string.printable.replace(" ",'').replace('\t\n\r\x0b\x0c','').replace("\\",'')

class PrintNumber(threading.Thread):
    def __init__(self, n,m):
        self.n = n
        self.m=m
        super(PrintNumber,self).__init__()

    def run(self):
        print self.n, self.n+self.m
        for i in range(self.n, self.n+self.m):
            abc = i

def run(m,n):
    timea = time()
    s= m/n
    a = [i*s for i in range(n)]
    for i in a:
        thread = PrintNumber(i,s)
        thread.start()
    timeb= time()
    print '=----------',timeb-timea,'---------'


m = 20000
n = 10
print len(list(itertools.permutations(list(PrinTable),3)))

comb = list(itertools.permutations(list(PrinTable),3))
combination = []

for each in comb:
    eachcomb = ''.join(list(each))
    combination.append(eachcomb)
    
