import socket
import json
import numpy as np
from vpython import *

# listen to UDP messages TO this adress
UDP_IP = "192.168.137.1"
UDP_PORT = 5005

#setup socket to listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(1)	

firstmsgparsed = False

#log all recieved data?
logging = True

while True:

    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    
    # some data was received! Clean up and split to separate vars
    datastring = str(data).replace("b\'","").replace("\\n\'","")
    datavars = str(datastring).split(";")
    if logging:
        with open('logfile.txt','+a') as f:
            f.write("\n"+(datastring))    #write data to new line 
    if len(datavars)>2:
        #f.write(data)    #write data to new line 
        if not firstmsgparsed:
            # if first iteration, create canvas and initialize plot

            #Parse individual beacon positions:
            b1pos = json.loads(datavars[5].replace('(','[').replace(')',']'))
            b2pos = json.loads(datavars[6].replace('(','[').replace(')',']'))
            b3pos = json.loads(datavars[7].replace('(','[').replace(')',']'))
            b4pos = json.loads(datavars[8].replace('(','[').replace(')',']'))
            b5pos = json.loads(datavars[9].replace('(','[').replace(')',']'))
            b6pos = json.loads(datavars[10].replace('(','[').replace(')',']'))
            bp = [b1pos,b2pos,b3pos,b4pos,b5pos,b6pos]

            #create canvas for polot
            scene = canvas(width=2000, height=1700, center=vector(2,3,0),forward = vec(0,1,0.5), range=10, background=color.white)
            scene.range=5

            #plot one sphere for each beacon in bp
            for bc in bp:
                sphere(pos=vec(bc[0],bc[1],bc[2]), size=vec(0.5,0.5,0.5),color =vec(1,0,1))
            
            #plot a simple grid at Z = 0
            for i in np.arange(0,5,0.5):
                cylinder(pos = vec(0,i,0), length = 5, axis = vec(1,0,0),radius = 0.01)
                cylinder(pos = vec(i,0,0), length = 5, axis = vec(0,1,0),radius = 0.01)
                        
            #parse calculated tag positions
            msg_Xpos = json.loads(datavars[2])
            msg_Ypos = json.loads(datavars[3])        
            #for some reason Z is nan sometimes. 
            if not isnan(float(datavars[4])):
                msg_Zpos = json.loads(datavars[4])
            
            #plot a sphere at the position of the drone tag. Save it as dronepoint for later
            dronepoint=sphere(pos=vec(msg_Xpos,msg_Ypos,msg_Zpos), size=vec(0.5,0.5,0.5),color =vec(0,1,1), make_trail= True)    
            firstmsgparsed = True

        # at each subsequent iteration:
        #statuscodes are not really used 
        msg_statuscode1 = json.loads(datavars[0])
        msg_statuscode2 = json.loads(datavars[1])
        
        # parse new tag coordinates
        msg_Xpos = json.loads(datavars[2])
        msg_Ypos = json.loads(datavars[3])
        if not isnan(float(datavars[4])):
            msg_Zpos = json.loads(datavars[4])

        # set the sphere position to the new tag coordinates.
        dronepoint.pos=vec(msg_Xpos,msg_Ypos,msg_Zpos)
            


