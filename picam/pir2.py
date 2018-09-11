from mcp3208 import MCP3208
import time
import datetime

adc = MCP3208()

g_checkq = []
g_q = []
g_average = 2048
g_tog = 0


def __av__(reading):
	global g_q, g_average
	g_q.append(reading)
	if len(g_q)==10:
		g_average = sum(g_q)/len(g_q)
		g_q.pop(0)

while True:
	voltage = adc.read(6)
	read = voltage*1.0*5.0/4096
	time.sleep(0.1)
	#__av__(voltage)
	#av = __av__(voltage)
#	if (g_average > 1920 and g_average < 2176):
#		g_checkq.append(1)
#		if len(g_checkq) == 60:
#			print "SIGUSR1 CALL"
#			g_checkq = []
#	else :
#		g_checkq = []

	#print "TIME : ", datetime.datetime.now()
#	print "\tg_checkQ : ", len(g_checkq)
	print("\tVoltage : %f" % (voltage))
	#print "\tAV : ", g_average, "\t PIR : ",voltage,"\n", "\t VOL : ", read
	time.sleep(0.01)

