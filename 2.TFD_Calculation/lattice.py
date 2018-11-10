import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import lsq_linear
lattice=open("lattice.txt","w")
sqn=50
while(sqn<=200):
	nodes=sqn**2
	distmat=np.zeros([nodes,nodes])
	for i in range (0,nodes):
		for j in range(0,nodes):
			distmat[i][j]=abs(i-j)/sqn+abs(i-j)%sqn
	lbmax=2*(sqn-1)+1
	cil=np.zeros([nodes,lbmax])
	used=np.zeros(shape=(lbmax,nodes,nodes))
	for lb in range (0,lbmax):
         for i in range (1,nodes):
             for j in range(0,i):
                 if distmat[i][j]>lb:
                    used[lb][i][int(cil[j][lb])] = 1
             for col in range(0,nodes):
                 if used[lb][i][col]==0:
                     cil[i][lb]=col
                     break        
	#Number of boxes required
	nb=np.amax(cil,0)+1
	y=np.transpose([math.log(i) for i in nb])
	lboxes=range(1,lbmax+1)
	llboxes=[-math.log(i) for i in lboxes]
	A=np.column_stack(([1]*lbmax, llboxes))
	#print(A)
	lsq=lsq_linear(A,y)
	k=np.exp(lsq.x[0])
	tfd=lsq.x[1]
	fitted=[k*(1.0/lbox)**tfd for lbox in lboxes]
	lattice.write(str(sqn)+" "+str(tfd)+"\n")
	print("For {0}, TFD = {1:.4f}".format(sqn, tfd ) )
	sqn+=15

#plt.figure(1)
#plt.loglog(lboxes,nb,'.')
#plt.loglog(lboxes,fitted,'-')

