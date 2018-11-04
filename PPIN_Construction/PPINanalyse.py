#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 21:56:07 2018

@author: kalagz
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os, time
#import csv
import numpy as np
from scipy import stats
#from sklearn.linear_model import LogisticRegression as LogReg

#FolderToParse = "G:\DATASETS\BioGrid\BIOGRID-ORGANISM-tab2/" #"BioGrid files/"
FolderToParse = "EdgeLists/"
Time = []
nNodes = []
nEdges = []
f = open('PPIN_Latex_Table.txt','w')
for organism in os.listdir( FolderToParse ):
    FileToLoad = FolderToParse + organism
    G = nx.Graph() # Initialise graph

    cases = len(os.listdir( FolderToParse ))
    #####################
    # OPEN without pandas
    start = time.clock()
#    with open(FileToLoad, 'rb') as edgelist:
#        edge = csv.reader(edgelist, delimiter=' ')
#        G.add_edges_from( edge )
    
    # OPEN with pandas
    edgelist = pd.read_csv(FileToLoad, delimiter=' ', header = None)
    G.add_edges_from( edgelist.values )
    Time.append( time.clock() - start )
    
    M = G.number_of_edges()
    N = G.number_of_nodes()
    nNodes.append( N )
    nEdges.append( M )
    
    ######################
    # Get organism's name:
    name = FileToLoad
    while name.find("/") > 0:
        name = name[name.find("/")+1:] # delete the prefix: folders etc
    # delete the suffix:
    name = name[ len("BIOGRID-ORGANISM-") :  (len(name)-len("-3.5.165.tab2.txt")) ]
    shortname = name.replace('_', " \ ") # this is to make gaps for latex
    # Progress Check
    print("\nThere are {0} nodes and {1} edges in the graph of \n{2}\n".format(N, M, name) )

    # Get the number of connected components
    concomps = nx.number_connected_components(G)
    # Get the size of the largest component
    largest = len( sorted(nx.connected_components(G), key = len, reverse=True)[0] )/float(N)
    # Compute the average degree - take values from dict, then transform to list
    degrees = sorted( G.degree().values(), reverse=True )

    # nx.degree_centrality(G)).values()
    f.write("$ {0} $ & {1} & {2} & {3:.2f} & {4} & {5:.2f} \\\\ \n".format( shortname, N, M, np.mean(degrees), concomps, largest ))

    ##################
    # Visualize graph:
    #plt.show()
    plt.figure()
    nx.draw(G,node_size=10, pos=nx.spring_layout(G))
    plt.savefig('Visuals/'+name+'-Graph.png')
    plt.close()

    ###########################
    # Plot Degree Distribution:
    fig = plt.figure()
    plt.subplot(1,3,2)
    plt.plot(range(len(degrees)), degrees, 'ro') #,'b-'
    plt.subplot(1,3,1)
    plt.hist( degrees, bins=50, rwidth=0.6 ) #, cnt, width=0.80, color='b')
    plt.subplot(1,3,3)
    plt.loglog(range(len(degrees)), degrees, 'bo') #,'b-'
    fig.savefig( 'Visuals/'+name+"-DD.png" )
    plt.close()
    #plt.show()
    
f.close()
##########################
## Analyse Time VS nNodes:
tosort = np.argsort(nNodes)
X = [ nNodes[x] for x in tosort ]
Y = [ Time[x] for x in tosort ]
X = np.log( X )
Y = np.log( Y )
plt.figure()
plt.plot(X, Y, 'ro', label='original data')
slope, intercept, r_value, p_value, std_err = stats.linregress( X, Y )
Z = [ slope*x + intercept for x in X ]
#print(slope, intercept)
plt.plot(X, Z, '-', label=r'$y={:.2f}x {:.2f}$'.format(slope,intercept))
plt.legend(fontsize=11, loc= 'upper left')
plt.title("Time vs Number of Nodes & Logistic Regression")
plt.xlabel(r"Log - Number of Nodes $N$", fontweight="bold")
plt.ylabel("Log - Time to Create", fontweight="bold")
plt.savefig("TimeVsNodes.eps")
plt.savefig("TimeVsNodes.png")
plt.show()
##########################
## Analyse Time VS nEdges:
plt.figure()
tosort = np.argsort(nEdges)
X = [ nEdges[x] for x in tosort ]
Y = [ Time[x] for x in tosort ]
X = np.log( X )
Y = np.log( Y )
plt.plot(X, Y, 'ro', label='original data')
slope, intercept, r_value, p_value, std_err = stats.linregress( X, Y )
Z = [ slope*x + intercept for x in X ]
plt.plot(X, Z, '-', label=r'$y={:.2f}x {:.2f}$'.format(slope,intercept))
#plt.plot(X, Z, '-', label=r'$\sin(X) \cdot e^x$')
plt.legend(fontsize=11, loc='upper left')
plt.title("Time vs Number of Edges & Logistic Regression")
plt.xlabel(r"Log - Number of Edges $M$", fontweight="bold")
plt.ylabel("Log - Time to Create", fontweight="bold")
plt.savefig("TimeVsEdges.eps")
plt.savefig("TimeVsEdges.png")
plt.show()
###########################
"""
X = np.array(nNodes).reshape(-1,1)
Y = np.array( TimePlot ) #, dtype=np.float64)

fit = LogReg().fit(X , Y)
Z = fit.predict( X )
plt.plot(nNodes, Z, 'g-')
"""
