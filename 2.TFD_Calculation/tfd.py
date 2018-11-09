import numpy as np
import matplotlib.pyplot as plt
import math
import os
from scipy.optimize import lsq_linear
for filename in os.listdir('Sizes'):
        print(filename)
	#Save the number of nodes in the graph, stored in Sizes
	sizes=open('Sizes/'+filename,"r")
	for line in sizes:
		nodes=int(line.split(': ')[1])
		break
        sizes.close()
	#Save the distance matrix
	distmat = open ("Distmat/"+filename, 'r')
	l = [[int(num) for num in line.split()] for line in distmat ]
        distmat.close()
        print('Done reading')
	#Save the maximum distance in the graph
	maxima=open('Maxima/'+filename,"r")
	for line in maxima:
		lbmax=int(line)+1
		break;
	lb=1
        maxima.close()
	cil=np.zeros([nodes,lbmax]) #this tells the box numbers for each node at each lb, 0<=lb<lbmax
	#the "used" list tells which boxes are unavailable for node i at each lb
	#in the paper, lb would go actually from 1 to lbmax, and 
	used=[0]*nodes
	for lb in range (0,lbmax):
    		for i in range (1,nodes):
                	used=[0]*nodes
        		for j in range(0,i):
            			if l[i][j]>0:
                			if l[i][j]>lb: #if i and j are further than lb apart, i can't be in the same box as j 
                    				used[int(cil[j][lb])]=1
            			else: #if no path between i and j, i can't be in the same box as j
               				used[int(cil[j][lb])]=1
        		for col in range(0,nodes):
            			if used[col]==0: #first unused box becomes the box of i
                			cil[i][lb]=col
                			break       
	nb=np.amax(cil,0)+1 #select the number of boxes for each lb
	#Do the linear least square fit
	y=np.transpose([math.log(i) for i in nb])
	lboxes=range(1,lbmax+1)
	llboxes=[-math.log(i) for i in lboxes]
	A=np.column_stack(([1]*lbmax, llboxes))
	lsq=lsq_linear(A,y)
	k=np.exp(lsq.x[0])
	tfd=lsq.x[1]
	fitted=[k*(1.0/lbox)**tfd for lbox in lboxes]
        results=open('TFD/'+filename,"w")
	results.write(str(tfd)+"\n")
	results.write(str(lbmax)+"\n")
	results.write(str(nb)+"\n")
	results.write(str(fitted)+"\n")
        results.close()
