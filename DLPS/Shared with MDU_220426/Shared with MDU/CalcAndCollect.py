import math
import serial
from time import sleep
from statistics import *
import socket
import json
import ctypes
from ctypes import c_void_p, c_double, c_int, cdll
from numpy.ctypeslib import ndpointer
import numpy as np

UDP_IP = "192.168.137.1" #This is the wifi hotspot gateway! UDP messages will go here, update accordingly
UDP_PORT = 5005

#path and filename to numerical functions.
SO_FILENAME = "./calc_pos6.so"
SO_FILENAME_5 = "./calc_pos5.so"


class bpos(ctypes.Structure):
        _fields_ = [("x", ctypes.c_double),("y",ctypes.c_double),("z",ctypes.c_double)]

class ddist(ctypes.Structure):
        _fields_ = [("a_b", ctypes.c_double),("a_c",ctypes.c_double),("a_d",ctypes.c_double)]


# Define cfunction
pos_calc_fn_obj = ctypes.CDLL(SO_FILENAME)
pos_calc_fn_obj_5 = ctypes.CDLL(SO_FILENAME_5)

delta_dist = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]



#Call this function to run data calculation and collection
def calcPos(zValues):

	# PC Partner adress and port:
	ser = serial.Serial ("/dev/ttyS0", 115200,timeout = 1)    #Open port with baud rate
	sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
	# Start listening for UART messages from nRF board. When recieved, calculate position and send to PC over UDP
	print("Start listening for UART messages from nRF board")

	#Try to flush out old values still in the buffer
	ser.read_all()

	i = 0
	iteration = 0
	estimatedPosArray = []
	while iteration < 200:
		print('Iteration ' + str(iteration))
		received_data = ser.readline()              #read serial port
		print ("Something received: "+ str(received_data))          #print received data
		sleep(.1)

		if len(received_data)>5:

			# some data was received! Clean up and split to separate vars
			datastring = str(received_data).replace("b\'","").replace("\\n\'","")
			datavars = str(datastring).split(";")
			print(datavars)

			#if enough data (messages can clip sometimes, if so discard)
			if len(datavars)>5:
				try:
					msg_statuscode = json.loads(datavars[0])
					if msg_statuscode > 0:
						msg_b1pos = json.loads(datavars[1])
						msg_b2pos = json.loads(datavars[2])
						msg_b3pos = json.loads(datavars[3])
						msg_b4pos = json.loads(datavars[4])
						msg_b5pos = json.loads(datavars[5])
						msg_b6pos = json.loads(datavars[6])
						msg_dDist = json.loads(datavars[7])

						bpos1=(0,0,zValues[0])
						bpos2=(0,4.95,zValues[1])
						bpos3=(4.65,4.95,zValues[2])
						bpos4=(-1.16,2.2,zValues[3])
						bpos5=(4.75,0,zValues[4])
						bpos6=(2.25,-2.5,zValues[5])
							
						#these are the raw latest differences
						delta_dist[i] = (msg_dDist[0],msg_dDist[1],msg_dDist[2],msg_dDist[3],msg_dDist[4])
						
						#this is a running average of differences, 3 latest values.
						d1 = mean([di[0] for di in delta_dist])
						d2 = mean([di[1] for di in delta_dist])
						d3 = mean([di[2] for di in delta_dist])
						d4 = mean([di[3] for di in delta_dist])
						d5 = mean([di[4] for di in delta_dist])

						if max(abs(delta_dist[i][0]),abs(delta_dist[i][1]),abs(delta_dist[i][2]),abs(delta_dist[i][3]),abs(delta_dist[i][4]))<100:


							#input vector to c-function is: [dDistanceA-B,dDistanceA-C,dDistanceA-D,...etc...,BeaconAPosX,BeaconAPosY,BeaconAPosZ,BeaconBPosX....etc.....]
							inputvector = np.array((d1,d2,d3,d4,d5,#delta_dist[0],delta_dist[1],delta_dist[2],delta_dist[3],delta_dist[4], #if raw differences should be used instead
											bpos1[0],bpos1[1],bpos1[2],
											bpos2[0],bpos2[1],bpos2[2],
											bpos3[0],bpos3[1],bpos3[2],
											bpos4[0],bpos4[1],bpos4[2],
											bpos5[0],bpos5[1],bpos5[2],
											bpos6[0],bpos6[1],bpos6[2]))
							
							#input vector to c-function is: [dDistanceA-B,dDistanceA-C,dDistanceA-D,...etc...,BeaconAPosX,BeaconAPosY,BeaconAPosZ,BeaconBPosX....etc.....]
							inputvector_5 = np.array((d1,d2,d3,d4,#delta_dist[0],delta_dist[1],delta_dist[2],delta_dist[3], #if raw differences should be used instead
											bpos1[0],bpos1[1],bpos1[2],
											bpos2[0],bpos2[1],bpos2[2],
											bpos3[0],bpos3[1],bpos3[2],
											bpos4[0],bpos4[1],bpos4[2],
											bpos5[0],bpos5[1],bpos5[2]))


							# call the compiled C functions using the correct inputvector, for 5 or 6 beacons
							result_obj = pos_calc_fn_obj.calc_pos(c_void_p(inputvector.ctypes.data))
							result_obj_5 = pos_calc_fn_obj_5.calc_pos(c_void_p(inputvector.ctypes.data))

							#some mumbojumbo about the reply format. The reply data is a vector on format [X,Y,Z,error,statuscode]
							ArrayType = ctypes.c_double*5
							array_pointer = ctypes.cast(result_obj, ctypes.POINTER(ArrayType))
							array_pointer_5 = ctypes.cast(result_obj, ctypes.POINTER(ArrayType))

							print("Calculated position (6): "+str((array_pointer.contents[0],array_pointer.contents[1],array_pointer.contents[2])))
							#print("Calculated position (5): "+str((array_pointer_5.contents[0],array_pointer_5.contents[1],array_pointer_5.contents[2])))

							#pack up results in a ; delimited string
							msgstr_5 = str(msg_statuscode)+";"+str(int(array_pointer_5.contents[4]))+";"+str(array_pointer_5.contents[0])+";"+str(array_pointer_5.contents[1])+";"+str(array_pointer_5.contents[2])+";"+str(bpos1)+";"+str(bpos2)+";"+str(bpos3)+";"+str(bpos4)+";"+str(bpos5)+";"+str(bpos6)+";"+str(msg_dDist)+"\n"
							msgstr_6 = str(msg_statuscode)+";"+str(int(array_pointer.contents[4]))+";"+str(array_pointer.contents[0])+";"+str(array_pointer.contents[1])+";"+str(array_pointer.contents[2])+";"+str(bpos1)+";"+str(bpos2)+";"+str(bpos3)+";"+str(bpos4)+";"+str(bpos5)+";"+str(bpos6)+";"+str(msg_dDist)+"\n"
							
							#Add estimated position to array
							estimatedPosArray.append((array_pointer.contents[0], array_pointer.contents[1], array_pointer.contents[2]))

							#send on of the strings (5 or 6 beacons) as an UDP message. 
							UDPMESSAGE = bytearray(msgstr_6.encode())
							sock.sendto(UDPMESSAGE, (UDP_IP, UDP_PORT))
							
						else:
							("Bad data (unrealistic distances). Skipping iteration")
						i=i+1
						if i==3:
							i = 0
					else:
						print("Bad data (Timeout or dropped frame) Skipping iteration")
				except Exception as e:
					print("Some error!")
					print(datastring)
					print(e)
					UDPMESSAGE = b"0;2;12;13;5\n" #status_nrf;status_pi;posX;posY;posZ
		else:
			UDPMESSAGE = bytearray("NoData;".encode())
			print("No data")
			sock.sendto(UDPMESSAGE, (UDP_IP, UDP_PORT))

		iteration+=1
	ser.close()
	return estimatedPosArray