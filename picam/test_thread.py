import threading 
import picamera
from pqueue import Queue
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


adc = MCP3208()

cnt = 0

g_data = " "
g_cnt = 0
g_dtime = 0
g_sr = 0
g_dt = 0

g_disk = os.statvfs("/")
g_first_avail = g_disk.f_bsize * g_disk.f_bavail

#fname = "data"+str(dt.datetime.now())+".txt"
#f=open(fname, "w")

s_buff = ''
r_buff = list()
room_buff = list()

q = Queue("Buffer")

firebase = firebase.FirebaseApplication('https://pnu-dubleve.firebaseio.com')

class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)

class Sender(threading.Thread):
	def run(self):

		global sr

		while True:
			try:
	#			print("hello, I'm sender!")

				dtime = time.time()-start_time
				mydt = long(dtime*1000)/10
				cdt = int(mydt%100)

				global pdt
				global cnt

				if cdt!=pdt: # read datas for 0.01 second
					read = adc.read(6)
					sr = cnt/dtime
					#data = data + str(read) + " "
					data = str(read)
					pdt = cdt
						
					buff.append(map(int, data.split()))
#					print "num of buff: ", len(buff), ", cnt: ", cnt
							
					if len(buff)>=100 :
						ret_flag = True
						cnt = cnt + 1
						s_buff = buff[first_idx:last_idx]
						if cnt==15: # for 0.15 second
								# for removing first 15 datas of list
							buff.reverse()
							for i in range(15):
								buff.pop()
							buff.reverse()

							s_buff = sum(s_buff, []) # 2 dimension list to 1 dimension list
							print "s_buff len: ", len(s_buff)
							q.put_nowait(s_buff)

#							print "s_buff: ", s_buff

	#						room_buff.append(s_buff)

							del s_buff[:]
							cnt = 0
						
			#			cam.annotate_text = (dt.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-4]
			#			+ " sr : " + str(round(sr, 1)) + " sn : " + str(cnt) + "\npir : " + data[0:30])

				if cdt==0: # write datas in file for 1 second
	#				f.write(data)
					data = ""
	#				print "sr", sr, "dt", str(dt.datetime.now())

				avail = g_disk.f_bsize * g_disk.f_bavail

				if avail < (g_first_avail * 3 / 5) :
					raise KeyboardInterrupt

			except KeyboardInterrupt:
				break

class Receiver(threading.Thread):
	def run(self):

		time.sleep(3)

		global room_buff
		r_buff = q.get_nowait()
		print "r_buff: ", r_buff, ", len", len(r_buff)
		room_buff.append(map(int, r_buff))
#		room_buff = sum(room_buff, [])

		while True:
	#		print("Nice to meet you!")
			X_data = room_buff
			print "X_data: ", X_data, ", len: ", len(X_data)

			X = tf.placeholder(tf.float32)

			W1 = tf.Variable(tf.random_uniform([100, 50], -1., 1.))
			W2 = tf.Variable(tf.random_uniform([50, 2], -1., 1.))
			b1 = tf.Variable(tf.zeros([50]))
			b2 = tf.Variable(tf.zeros([2]))

			L1 = tf.add(tf.matmul(X, W1), b1)
			Y = tf.nn.softmax(tf.matmul(L1, W2) + b2)

			sess = tf.Session()

			#tf.reset_default_graph()
			with tf.Session() as sess:
				saver = tf.train.Saver()
				sess.run(tf.global_variables_initializer())

				ckpt_path = saver.restore(sess, tf.train.latest_checkpoint("./model"))
				init_op = tf.global_variables_initializer()
				sess.run(init_op)
				predictions = sess.run(Y, feed_dict={X:X_data})

				print(predictions)

				for i in range(len(predictions)):
					if str(predictions[i]) == "[1. 0.]":
						print('exist')
					else:
						print('not exist')

#Import Datasets & set datasets

if __name__ == '__main__':

	mydt = 0
	pdt = 0
	sr = 0
	cnt = 0
	data = ''

	send = Sender()
	recv = Receiver()

	buff = list() # buffer that collects datas(more than 100 datas)			
#	s_buff = list() # buffer for sending datas

	first_idx = 0
	last_idx = first_idx + 100

	start_time = time.time()

	send.start()
	recv.start()
	send.join()	
	recv.join()

	queue_service.delete_queue("Buffer")

#	f.close()