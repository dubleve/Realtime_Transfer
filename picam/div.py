import picamera
from mcp3208 import MCP3208
import datetime as dt
import time
import sys
import signal
import os


adc = MCP3208()

g_data = " "
g_cnt = 0
g_dtime = 0
g_sr = 0
g_dt = 0

g_disk = os.statvfs("/")
g_first_avail = g_disk.f_bsize * g_disk.f_bavail

fname = "data"+str(dt.datetime.now())+".txt"
f=open(fname, "w")

s_buff = ''
r_buff = list()
room_buff = list()

ret_flag = False # Ture: complete, False: keep going!



def sender():
	while True:
		try:
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
				print "num of buff: ", len(buff), ", cnt: ", cnt
						
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

						print "s_buff: ", s_buff

#						output.put(s_buff)
						room_buff.append(s_buff)

						del s_buff[:]
						cnt = 0
					
		#			cam.annotate_text = (dt.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-4]
		#			+ " sr : " + str(round(sr, 1)) + " sn : " + str(cnt) + "\npir : " + data[0:30])

			if cdt==0: # write datas in file for 1 second
				global data
				global sr
				f.write(data)
				data = ""
				print "sr", sr, "dt", str(dt.datetime.now())

			avail = g_disk.f_bsize * g_disk.f_bavail

			if avail < (g_first_avail * 3 / 5) :
				raise KeyboardInterrupt

		except KeyboardInterrupt:
			break

if __name__ == '__main__':
	#signal.signal(signal.SIGUSR1, getpir)

	#os.kill(os.getpid(),signal.SIGUSR1)

	mydt = 0
	pdt = 0
	sr = 0
	cnt = 0
	data = ''
#	output = ''

#	p_send = Process(target=sender, args=(output))

	buff = list() # buffer that collects datas(more than 100 datas)			
#	s_buff = list() # buffer for sending datas

	first_idx = 0
	last_idx = first_idx + 99

	start_time = time.time()

	sender()

#	cam = picamera.PiCamera()
#	cam.resolution = (320,240)
#	cam.framerate = 10
#	cam.start_recording('video'+str(dt.datetime.now())+'.h264')
#	cam.start_preview()
#	cam.annotate_background = picamera.Color('black')
#	cam.annotate_text_size = 10

#	cam.stop_preview()
#	cam.stop_recording()
#	cam.close()

	f.close()
