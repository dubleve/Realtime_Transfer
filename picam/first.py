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

class NumpyEncoder(json.JSONEncoder):
   def default(self, obj):
      if isinstance(obj, np.ndarray):
         return obj.tolist()
      return json.JSONEncoder.default(self, obj)

#Import Datasets & set datasets
firebase = firebase.FirebaseApplication('https://pnu-dubleve.firebaseio.com')

#6
adc = MCP3208()

g_data = " "
g_cnt = 0
g_dtime = 0
g_sr = 0
g_dt = 0

g_disk = os.statvfs("/")
g_first_avail = g_disk.f_bsize * g_disk.f_bavail

#w_size = 100
#stride = 15

time_now = dt.datetime.now()

# time_fname = "time.txt"
# time_f = open(time_fname, "w")
# time_data = str(time_now)
# time_f.write(time_data)
# time_f.close()

fname = "data"+str(time_now)+".csv"
f=open(fname, "w")

if __name__ == '__main__':
   #signal.signal(signal.SIGUSR1, getpir)

   #os.kill(os.getpid(),signal.SIGUSR1)

   mydt = 0
   pdt = 0
   sr = 0
   cnt = 0
   data = ''

#   cam = picamera.PiCamera()
#   cam.resolution = (320,240)
#   cam.framerate = 10
#   cam.start_recording('video'+str(dt.datetime.now())+'.h264')
#   cam.start_preview()
#   cam.annotate_background = picamera.Color('black')
#   cam.annotate_text_size = 10

   start_time = time.time() # type: 153657908//6.30//0 (seconds)

   while True:
      try:

         dtime = time.time()-start_time
         mydt = long(dtime*1000)/10 # 100 seconds
         cdt = int(mydt%100) # 1 second

         print "cdt: ", cdt, ", pdt: ", pdt

         buff = list()

         if cdt!=pdt: # before receiving a 100th input / if cdt == 6 # cdt == 
            read = adc.read(6)
            cnt = cnt + 1
            sr = cnt/dtime
            data = data + str(read) + " "
	    #print("data: " + data + ", cnt:" + str(cnt))
            pdt = cdt # pdt will be 6

            # Collecting the previous data in buffer
            # and at this time, executing tensorflow!

            buff.append(map(int, data.split()))

            print("buff: " + str(buff) + ", time: " + str(dt.datetime.now()))

            if(cnt%100==0):
				#print("successfully")
               print "cnt", cnt

            # for row in data:
            #    rows = list()
            #    for column in row:
            #       rows.append(column.split())
            #    rowdata = [list(map(int, i)) for i in rows]
            #    buff.append(rowdata[0])


				#buff = list(data) # At this time, 'data' should be int or float type! 

                 # saver = tf.train.Saver()
               # init_op = tf.global_variables_initializer()

               # with tf.Session() as sess:
               #   sess.run(init_op)
               #   save_path = './model/dnn.ckpt'
               #   saver.restore(sess, tf.train.latest_checkpoint('./model/'))
               #   predictions = sess.run(Y, feed_dict={X: buff})

               #   firebase.put('Results/test', 'result', json.dumps(predictions, cls=NumpyEncoder))

               # Insert '\n' to PIR sensor data               
#               data += "\n"
#         cam.annotate_text = (dt.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-4]
#         + " sr : " + str(round(sr, 1)) + " sn : " + str(cnt) + "\npir : " + data[0:30])

         if cdt==0:
            f.write(data)
            data = ""
            print "sr", sr, "dt", str(dt.datetime.now())
            
         avail = g_disk.f_bsize * g_disk.f_bavail

         if avail < (g_first_avail * 3 / 5) :
            raise KeyboardInterrupt
      except KeyboardInterrupt:
         break



#   cam.stop_preview()
#   cam.stop_recording()
#   cam.close()

   f.close()
