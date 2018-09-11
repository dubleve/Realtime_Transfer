import datetime as dt
import time
import sys
import signal
import os
from get_realtime import s_buff

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

r_buff = list()

while True:

	"""
	Room for modifying the code under this line.
	"""
	r_buff.append(map(int, s_buff.split())) # It is a not accurate code. It must add `synchronizing between r_buff and s_buff`
	print "r_buff: ", r_buff
	X_data = r_buff[0]

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

		"""
		Room for implementing the sending code from here to database
		"""

	del r_buff[0]

