
import signal
import os

import tensorflow as tf
import pandas as pd
import json
import numpy as np
from firebase import firebase

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

                       # directly choose
                       # ckpt_path = saver.restore(sess, "./model/dnn0909")

                       # use latest_checkpoint
                  ckpt_path = saver.restore(sess, tf.train.latest_checkpoint("./model"))

                       #saver = tf.train.import_meta_graph('./model/dnn2-1000.meta')
                       # saver.restore(sess, tf.train.latest_checkpoint('./model'))

                       # X=graph.get_tensor_by_name()
                       # Y=graph.get_tensor_by_name()

                       # op_to_restore = graph.get_tensor_by_name("op_to_restore:()")
                  init_op = tf.global_variables_initializer()

                       # print(sess.run(op_to_restore, feed_dict={X:X_data}))

                  sess.run(init_op)

                       # save_path = './model/dnn0809.ckpt'
                       # saver.restore(sess, tf.train.latest_checkpoint('./model'))
                  predictions = sess.run(Y, feed_dict={X:buff})

                  print(predictions)

                  for i in range(len(predictions)):
                     if str(predictions[i]) == "[1. 0.]":
                        print('exist')
                     else:
                        print('not exist')			   X = tf.placeholder(tf.float32)

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

                       # directly choose
                       # ckpt_path = saver.restore(sess, "./model/dnn0909")

                       # use latest_checkpoint
                  ckpt_path = saver.restore(sess, tf.train.latest_checkpoint("./model"))

                       #saver = tf.train.import_meta_graph('./model/dnn2-1000.meta')
                       # saver.restore(sess, tf.train.latest_checkpoint('./model'))

                       # X=graph.get_tensor_by_name()
                       # Y=graph.get_tensor_by_name()

                       # op_to_restore = graph.get_tensor_by_name("op_to_restore:()")
                  init_op = tf.global_variables_initializer()

                       # print(sess.run(op_to_restore, feed_dict={X:X_data}))

                  sess.run(init_op)

                       # save_path = './model/dnn0809.ckpt'
                       # saver.restore(sess, tf.train.latest_checkpoint('./model'))
                  predictions = sess.run(Y, feed_dict={X:buff})

                  print(predictions)

                  for i in range(len(predictions)):
                     if str(predictions[i]) == "[1. 0.]":
                        print('exist')
                     else:
                        print('not exist')			   X = tf.placeholder(tf.float32)

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

                       # directly choose
                       # ckpt_path = saver.restore(sess, "./model/dnn0909")

                       # use latest_checkpoint
                  ckpt_path = saver.restore(sess, tf.train.latest_checkpoint("./model"))

                       #saver = tf.train.import_meta_graph('./model/dnn2-1000.meta')
                       # saver.restore(sess, tf.train.latest_checkpoint('./model'))

                       # X=graph.get_tensor_by_name()
                       # Y=graph.get_tensor_by_name()

                       # op_to_restore = graph.get_tensor_by_name("op_to_restore:()")
                  init_op = tf.global_variables_initializer()

                       # print(sess.run(op_to_restore, feed_dict={X:X_data}))

                  sess.run(init_op)

                       # save_path = './model/dnn0809.ckpt'
                       # saver.restore(sess, tf.train.latest_checkpoint('./model'))
                  predictions = sess.run(Y, feed_dict={X:buff})

                  print(predictions)

                  for i in range(len(predictions)):
                     if str(predictions[i]) == "[1. 0.]":
                        print('exist')
                     else:
                        print('not exist')
