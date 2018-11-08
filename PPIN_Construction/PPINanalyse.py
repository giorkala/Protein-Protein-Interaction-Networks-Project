#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 21:56:07 2018
@author: giorkala
Script that parses every available edgelist (in "FolderToParse"), computes basic measures,
exports these to LaTeX format, visualises graphs (via NetworkX) and, finally, tests the time
versus #Nodes or #Edges complexity.
"""
import pandas as pd # OR:
#import csv
import networkx as nx
import matplotlib.pyplot as plt
import os, time
import numpy as np
from scipy import stats

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
    if concomps==1:
        largest = float(1.0) # here we cheat since we know it's 100%
        # Get the diameter
        diam = nx.algorithms.distance_measures.diameter(G)
    else:
        # work on the largest connected component
        LCC = max(nx.connected_component_subgraphs(G), key=len )
        largest = len(LCC)/float(N)
        # Get the diameter of the LGC
        diam = nx.algorithms.distance_measures.diameter(LCC)
    # Compute the average degree - take values from dict, then transform to list
    degrees = G.degree().values()
    # export measurements
    f.write("$ {0} $ & {1} & {2} & {3:.2f} & {4} & {5:.3f} & {6} \\\\ \n".format( shortname, N, M, np.mean(degrees), concomps, largest, diam ))
<<<<<<< HEAD

=======
 
>>>>>>> 959bbcebdd17a531c156bf988c69574b6f60120e
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
plt.plot(X, Z, '-', label=r'$y={:.2f}x {:.2f}$'.format(slope,intercept))
plt.legend(fontsize=11, loc= 'upper left')
#plt.title("Time vs Number of Nodes & Logistic Regression")
plt.xlabel(r"Log - Number of Nodes $N$", fontweight="bold")
plt.ylabel("Log - Time to Create", fontweight="bold")
plt.savefig("TimeVsNodes.eps")
plt.savefig("TimeVsNodes.png")
#plt.show()
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
plt.legend(fontsize=11, loc='upper left')
#plt.title("Time vs Number of Edges & Logistic Regression")
plt.xlabel(r"Log - Number of Edges $M$", fontweight="bold")
plt.ylabel("Log - Time to Create", fontweight="bold")
plt.savefig("TimeVsEdges.eps")
plt.savefig("TimeVsEdges.png")
#plt.show()
###########################
###########################
