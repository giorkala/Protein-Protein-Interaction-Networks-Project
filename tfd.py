import numpy as np
import matplotlib.pyplot as plt
import math
import os
from scipy.optimize import lsq_linear
for filename in os.listdir('Sizes'):
        print(filename)
	sizes=open('Sizes/'+filename,"r")
	for line in sizes:
		nodes=int(line.split(': ')[1])
		break
        sizes.close()
	distmat = open ("Distmat/"+filename, 'r')
	l = [[int(num) for num in line.split()] for line in distmat ]
        distmat.close()
        print('Done reading')
	maxima=open('Maxima/'+filename,"r")
	for line in maxima:
		lbmax=int(line)+1
		break;
	lb=1
        maxima.close()
	cil=np.zeros([nodes,lbmax])
	used=[0]*nodes
	for lb in range (0,lbmax):
    		for i in range (1,nodes):
                	used=[0]*nodes
        		for j in range(0,i):
            			if l[i][j]>0:
                			if l[i][j]>lb:
                    				used[int(cil[j][lb])]=1
            			else:
               				used[int(cil[j][lb])]=1
        		start=0
        		stop=i
        		mid=(start+stop)/2
        		while start<stop:
				if used[mid]==1:
        				start=mid+1
                		else:
					stop=mid
                		mid=(start+stop)/2     
        		cil[i][lb]=mid    
	nb=np.amax(cil,0)+1
	y=np.transpose([math.log(i) for i in nb])
	lboxes=range(1,lbmax+1)
	llboxes=[-math.log(i) for i in lboxes]
	A=np.column_stack(([1]*lbmax, llboxes))
	lsq=lsq_linear(A,y)
	k=np.exp(lsq.x[0])
	tfd=lsq.x[1]
	fitted=[k*(1.0/lbox)**tfd for lbox in lboxes]
    	results=open('TFD2/'+filename,"w")
	results.write(str(tfd)+"\n")
	results.write(str(lbmax)+"\n")
	results.write(str(nb)+"\n")
	results.write(str(fitted)+"\n")
    	results.close()
