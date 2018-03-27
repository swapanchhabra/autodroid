import os
from decimal import *
import time
import subprocess
#import elementtree.ElementTree as ET


action_list = []
time_rec = []


#tree = ET.parse('view.xml')
#root = tree.getroot()

minX = 0
minY = 0
maxX = 1360
maxY = 2510

print "Setting up device.."
time.sleep(1)
#result = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
os.system("adb shell getevent -lt |grep -E --line-buffered 'ABS_MT_POSITION_X|ABS_MT_POSITION_Y|ABS_MT_TRACKING_ID   fffffff' > /Users/hscuser/Documents/backup/SWAPAN/setup_log.txt")
process = subprocess.Popen(['ls', '-l'], shell=True, stdout=subprocess.PIPE)
process.wait()
print process.returncode




print "\n*** Starting Execution of recorded events: ***"
raw_display = os.popen('adb shell dumpsys window | grep mUnrestrictedScreen').read()
device_name = os.popen('adb shell getprop ro.product.model').read()
print "\nResolution of device "+ '\033[1m' + device_name + '\033[0m'
print raw_display.strip().split()
print "\n"

matching = [s for s in raw_display.strip().split() if "x" in s]

displayWidth = int(matching[0].split('x')[0])
displayHeight = int(matching[0].split('x')[1])

with open('log1.txt') as f: 
	data = f.read() 
out_f = open('action.command', 'w')
count = 0
action_list.append(data.strip().split('ABS_MT_TRACKING_ID'))
print "****** Total Actions ******"
print len(action_list[0])

#print action_list

for it in action_list[0]:

	count_x = it.count("ABS_MT_POSITION_X")
	count_y = it.count("ABS_MT_POSITION_Y")

	index_x = it.find("ABS_MT_POSITION_X") + 21
	index_time = index_x - 55
	time_rec.append(it[index_time-12:index_time])
	count = count + 1

	if count_x == 0 or count_y == 0:
		continue
	elif count_x > 30 or count_y > 30:
		print "Swipe"
		index_x = it.find("ABS_MT_POSITION_X") + 21
		index_y = it.find("ABS_MT_POSITION_Y") + 21
		x1_hexa = it[index_x:index_x+8]
		y1_hexa = it[index_y:index_y+8]
		x1_int = int(x1_hexa, 16)
		y1_int = int(y1_hexa, 16)
		index_x2 = it.rfind("ABS_MT_POSITION_X") + 21
		index_y2 = it.rfind("ABS_MT_POSITION_Y") + 21
		x2_hexa = it[index_x2:index_x2+8]
		y2_hexa = it[index_y2:index_y2+8]
		x2_int = int(x2_hexa, 16)
		y2_int = int(y2_hexa, 16)
		displayX1 = (x1_int - minX) * displayWidth / (maxX - minX + 1)
		displayY1 = (y1_int - minY) * displayHeight / (maxY - minY + 1)
		displayX2 = (x2_int - minX) * displayWidth / (maxX - minX + 1)
		displayY2 = (y2_int - minY) * displayHeight / (maxY - minY + 1)
		out_f.write("adb shell input swipe " + str(displayX1) + " " + str(displayY1) + " " + str(displayX2) + " " + str(displayY2) + " 3000\n")
		os.system("adb shell input swipe " + str(displayX1) + " " + str(displayY1) + " " + str(displayX2) + " " + str(displayY1) + " 3000\n" )
	else:
		print "Tap"
		index_x = it.find("ABS_MT_POSITION_X") + 21
		index_y = it.find("ABS_MT_POSITION_Y") + 21
		index_time = index_x - 55
		x_hexa = it[index_x:index_x+8]
		y_hexa = it[index_y:index_y+8]
		x_int = int(x_hexa, 16)
		y_int = int(y_hexa, 16)
		displayX = (x_int - minX) * displayWidth / (maxX - minX + 1)
		displayY = (y_int - minY) * displayHeight / (maxY - minY + 1)
        out_f.write("adb shell input tap " + str(displayX) + " " + str(displayY) + "\n")
        os.system("adb shell input tap " + str(displayX) + " " + str(displayY) + "\n")

	if count == 1:
		print "\n**Sleeping for 1.00000 second**"
		time.sleep(1)
	else:
		step_time = float(time_rec[count-1])-float(time_rec[count-2])
		print "\n**Sleeping for " + str(step_time) + " seconds**"
		time.sleep(step_time)
		out_f.write("sleep " + str(step_time) + "\n")

out_f.close()


