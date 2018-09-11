import picamera
from mcp3208 import MCP3208
import datetime as dt
import time
import sys
import signal
import os

import tensorflow as tf
import pandas as pd
import json
import numpy as np
from firebase import firebase
from multiprocessing import Process, Queue


firebase = firebase.FirebaseApplication('https://pnu-dubleve.firebaseio.com')

def sender(buff, n):
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)



    adc = MCP3208()

    g_data = " "
    g_cnt = 0
    g_dtime = 0
    g_sr = 0
    g_dt = 0

    g_disk = os.statvfs("/")
    g_first_avail = g_disk.f_bsize * g_disk.f_bavail

    time_now = dt.datetime.now()

    fname = "data"+str(time_now)+".csv"
    f=open(fname, "w")

    mydt = 0
    pdt = 0
    sr = 0
    cnt = 0
    data = ''

    start_time = time.time()

    while True:

        try:

            dtime = time.time()-start_time
            mydt = long(dtime*1000)/10 # 100 seconds
            cdt = int(mydt%100) # 1 second

            #print "cdt: ", cdt, ", pdt: ", pdt

            buff = list()

            if cdt!=pdt: # before receiving a 100th input / if cdt == 6 # cdt == 
                read = adc.read(6)
                cnt = cnt + 1
                sr = cnt/dtime
                data = data + str(read) + " "
                pdt = cdt # pdt will be 6

                buff.append(map(int, data.split()))

                if(cnt%100==0):
                   #print("successfully")
                   # print "cnt", cnt
                    cdt += 1
                    del buff[:]

            if cdt==0:
                f.write(data)
                data = ""
               # print "sr", sr, "dt", str(dt.datetime.now())

            avail = g_disk.f_bsize * g_disk.f_bavail

            if avail < (g_first_avail * 3 / 5) :
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            break

    f.close()

def main():
    q = Queue()

    p = Process(target=sender, args=(q, 1))
    p.start()

    # get msg from the Queue
  
  print(q.get())

    p.join()

if __name__ == "__main__":
    main()
