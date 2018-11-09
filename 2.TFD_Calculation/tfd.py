import numpy as np
import matplotlib.pyplot as plt
import math
import os
from scipy.optimize import lsq_linear
from scipy import stats

for filename in os.listdir('EdgeLists_Relabeled/Dictionaries'):
    # get the number of nodes from the re-labeling dictionary
    translator = open('EdgeLists_Relabeled/Dictionaries/'+filename,'r')
    nNodes = 0
    for node in translator:
        nNodes += 1
    # get only the name of the organism
    organism = filename.replace('.dictionary','')
    # Progress Check
    print( "\nThere are {0} nodes in the graph of \n{1}\n".format(nNodes, organism) )
    distmat = open("Distance_Calc/DistMats/" + organism + '-Distances.txt', 'r')
    table = [ [int(num) for num in line.split()] for line in distmat ]
    distmat.close()
    print('Done reading')

    lbmax=max(max(table))
    lb=1
    cil=np.zeros([nNodes,lbmax])
    used=[0]*nNodes
    for lb in range (0,lbmax):
        for i in range (1,nNodes):
            used=[0]*nNodes
            for j in range(0,i):
                if table[i][j]>0:
                    if table[i][j]>lb:
                        used[int(cil[j][lb])]=1
                #else:
                #    used[int(cil[j][lb])]=1
            for col in range(0,nNodes):
                if used[col]==0:
                    cil[i][lb]=col
                    break
	nb = np.amax(cil,0)+1
	y = np.transpose([math.log(i) for i in nb])
	lboxes=range(1,lbmax+1)
    for i in range(1,lbmax+1):
        print(i, nb[i])
    print(len(y), len(lboxes))
    A = [ [1 , math.log(i)] for i in lboxes]
	#A = np.column_stack(([1]*lbmax, A2))
    #slope, intercept, r_value, p_value, std_err = stats.linregress(A, y)
    #tfd = slope
    #lsq = lsq_linear(A,y)
	#const = np.exp(lsq.x[0])
	#tfd = lsq.x[1]
    print("TFD found = ",tfd)
    """
	fitted=[k*(1.0/lbox)**tfd for lbox in lboxes]
    results=open('TFD/'+filename,"w")
	results.write(str(tfd)+"\n")
	results.write(str(lbmax)+"\n")
	results.write(str(nb)+"\n")
	results.write(str(fitted)+"\n")
        results.close()

    """
