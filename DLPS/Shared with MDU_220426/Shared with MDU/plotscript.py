from statistics import *
import numpy as np
import matplotlib.pyplot as plt
import json
import math

x_list = []
y_list = []
z_list = []
d1 = []
d2 = []
d3 = []
d4 = []
d5 = []

beacon_list = []

with open("filename - kopia.txt",'r') as f:
    for line in f:
        line = f.readline().replace("nan","0")
        dummy =1
        variables = line.split(";")
        if len(variables)>1:
            x_list.append(json.loads(variables[2]))        
            y_list.append(json.loads(variables[3]))        
            z_list.append(json.loads(variables[4]))     
            d1.append(json.loads(variables[-1])[0])     
            d2.append(json.loads(variables[-1])[1])     
            d3.append(json.loads(variables[-1])[2])     
            d4.append(json.loads(variables[-1])[3])     
            d5.append(json.loads(variables[-1])[4])              
            b1pos = json.loads(variables[5].replace('(','[').replace(')',']'))
            b2pos = json.loads(variables[6].replace('(','[').replace(')',']'))
            b3pos = json.loads(variables[7].replace('(','[').replace(')',']'))
            b4pos = json.loads(variables[8].replace('(','[').replace(')',']'))

        #point = ax.scatter(msg_Xpos,msg_Ypos,msg_Zpos,color = 'green' ,s=200 )



d1np=np.array(d1)#[1400:-1])-mean(d1[1400:-1])
d2np=np.array(d2)#[1400:-1])-mean(d2[1400:-1])
d3np=np.array(d3)#[1400:-1])-mean(d3[1400:-1])
d4np=np.array(d4)#[1400:-1])-mean(d4[1400:-1])
d5np=np.array(d5)#[1400:-1])-mean(d5[1400:-1])

dstart = 1400
dend = len(d1np)-1

fig,ax = plt.subplots(5,1,sharey=True,sharex=True)
for data,nr in zip([d1np[dstart:dend],d2np[dstart:dend],d3np[dstart:dend],d4np[dstart:dend],d5np[dstart:dend]],range(5)):
    ax[nr].plot(data)#(d1[1400:-1])
    ax[nr].set_title(f'Delta d1-d {nr}. Mean: {mean(data):.4f} Std.Dev: {stdev(data):.4f}')

errVect = []
avgWindow = 100
for dataset in [d1np[dstart:dend],d2np[dstart:dend],d3np[dstart:dend],d4np[dstart:dend],d5np[dstart:dend]]:
    errVect.append(np.zeros(len(dataset)-avgWindow))
    for datapointnr in range(avgWindow,len(dataset)-avgWindow):
        errVect[-1][datapointnr-avgWindow] = dataset[datapointnr]-mean(dataset[datapointnr-avgWindow:datapointnr+avgWindow])

fig2,ax2 = plt.subplots(5,1,sharey=True,sharex=True)
for data,nr in zip(errVect,range(5)):
    ax2[nr].plot(data)#(d1[1400:-1])
    ax2[nr].set_title(f'Estimated error {nr}. Mean: {mean(data):.4f} Std.Dev: {stdev(data):.4f}')
    
fig3,ax3 = plt.subplots(5,1,sharex=True)
for data,nr in zip([d1np,d2np,d3np,d4np,d5np],range(5)):
    ax3[nr].plot(data)#(d1[1400:-1])
    ax3[nr].set_title('Delta d1-d'+str(nr)+', full data')
    ax3[nr].fill_between([dstart,dend],[max(data*1.1),max(data)*1.1],min(data)*1.1,alpha = 0.1)

plt.show()
while True:
    dummy =1
