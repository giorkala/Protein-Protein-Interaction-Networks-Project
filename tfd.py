import time

t0 = time.time()


import numpy.random as nr
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from math import log
from networkx import shortest_path_length as grdist
nodes=200
#G=nx.Graph()
#G.add_nodes_from(range(0,nodes))
#G.add_edges_from([(1,2),(7,4),(14,13),(14,15),(6,8),(9,12),(4,15),(15,16),(18,3),(10,7),(15,5),(2,3),(2,7),(7,9),(11,18),(4,10),(10,17),(8,17),(19,3),(0,14),(0,7),(1,18)])
G=nx.erdos_renyi_graph(nodes,0.2)

lbmax=30

lb=1
cil=np.zeros([nodes,lbmax])
colors=list(np.random.random(size=nodes) * 256)
used=np.zeros(shape=(lbmax,nodes,nodes))

for lb in range (0,lbmax):
    for i in range (1,nodes):
        for j in range(0,i):
            if nx.has_path(G,i,j):
                if grdist(G,i,j)>lb:
                    used[lb,i,int(cil[j][lb])]=1
            else:
               used[lb,i,int(cil[j][lb])]=1
        for col in range(0,nodes):
            if used[lb,i,col]==0:
                cil[i][lb]=col
                break     

#Number of boxes required
nb=np.amax(cil,0)+1
lboxes=range(1,lbmax+1)
#invlb=[30*(1.0/x)**0.8 for x in lboxes]
invlb=[1.0/x for x in lboxes]
tfd=0
for i in range(1,lbmax):
    tfd+=(log(nb[i]/nodes))/log(invlb[i])
tfd/=lbmax

fitted=[nodes*(1.0/x)**tfd for x in lboxes]

  
print(nb)
print(fitted)

plt.figure(1)
plt.plot(lboxes,nb)
plt.plot(lboxes,fitted)


plt.figure(2)
color_map = []
for node in G:
    color_map.append(colors[int(cil[node][lbmax-1])])
nx.draw(G,node_color = color_map,with_labels = True)
t1 = time.time()
total = t1-t0
print(total)
plt.show()
