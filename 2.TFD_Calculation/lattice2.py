import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import lsq_linear
lattice=open("lattice.txt","w")
sqn=70
while(sqn<=300):
	nodes=sqn**2
	lbmax=2*(sqn-1)+1
	cil=np.zeros([nodes,lbmax])
	used=[0]*nodes
	for lb in range (0,lbmax):
         for i in range (1,nodes):
            used=[0]*nodes
            for j in range(0,i):
                if abs(i-j)/sqn+abs(i-j)%sqn>lb:
                    used[int(cil[j][lb])]=1
            for col in range(0,nodes):
                if used[col]==0:
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
	print(sqn, tfd)
	sqn+=10

#plt.figure(1)
#plt.loglog(lboxes,nb,'.')
#plt.loglog(lboxes,fitted,'-')

