#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 21:56:07 2018

@author: kalagz
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from createPPIN import createPPIN
import os

FolderToParse = "G:\DATASETS\BioGrid\BIOGRID-ORGANISM-tab2/" #"BioGrid files/"
allfiles = os.listdir( FolderToParse )
for organism in allfiles:
    FileToLoad = FolderToParse + organism
    createPPIN( FileToLoad )

filetab2 = "BioGrid files/BIOGRID-ORGANISM-Human_Herpesvirus_6A-3.5.165.tab2.txt"
filetab2 = "BIOGRID-ORGANISM-Caenorhabditis_elegans-3.5.165.tab2.txt"
filetab2 = "BIOGRID-ORGANISM-Homo_sapiens-3.5.165.tab2.txt"
filetab2 = 'sample.txt'

#datafile = csv.reader(filetab2, delimiter='\t')

# load all the file as a data frame
data = pd.read_csv(filetab2, delimiter='\t')

# We select the columns of BIOGRID IDs only
# 0: interaction ID, 3: Interactor A, 4: Interactor B
# 7,8: Official symbols - to be saved separately
ColumnsToKeep = [ list(data)[c] for c in [0,3,4,7,8] ]
ColumnsToDrop =  set(list(data)) - set(ColumnsToKeep)
for col in ColumnsToDrop:
    data = data.drop( col , axis = 1 )

# extract official symbols to a separate file
f1 = open('official_symbols.csv','w')
f2 = open('edge_list.txt','w')
C1 = list( (data.values)[:,1] )
C2 = list( (data.values)[:,2] )
C3 = list( (data.values)[:,3] )
C4 = list( (data.values)[:,4] )
for x in range( len(data) ):
    f1.write("{0},{1}\n".format( C3[x], C3[x] ))
    f2.write("{0} {1}\n".format( C1[x], C2[x] ))
    #temp = (data.values)[x,[3,4]]
    #print("{0},{1}".format( temp[0], temp[1] ))
    #f.write("{0},{1}\n".format( temp[0], temp[1] ))
f1.close()
f2.close()

# Visualize graph
# first, take a 2D array from dataframe - these are numerics only
#edges = (data.values)[:,[1,2]]
G = nx.Graph()
G.add_edges_from( (data.values)[:,[1,2]] )
plt.show()
nx.draw_circular(G)
#plt.savefig('example123.pdf')
####################
## Nonsense stuff ##
####################
"""
# load all the file as a data frame
data = pd.read_csv(filetab2, delimiter='\t')

# We select the columns of BIOGRID IDs only - erase others to save memory
# 0: interaction ID, 3: Interactor A, 4: Interactor B
# 7,8: Official symbols - to be saved separately
ColumnsToKeep = [ list(data)[c] for c in [0,3,4,7,8] ]
ColumnsToDrop =  set(list(data)) - set(ColumnsToKeep)
for col in ColumnsToDrop:
    data = data.drop( col , axis = 1 )

# how to read from "edgelist" files whereas nodes are seperated by commas.
edgelist = pd.read_csv(datafile, delimiter=',')
G = nx.Graph()
G.add_edges_from( (edgelist.values) )

M = G.number_of_edges()
N = G.number_of_nodes()
print("There are {0} nodes and {1} edges in the graph.".format(M,N) )
nx.draw(G,node_size=10, pos=nx.spring_layout(G))

    distmat = open(FileToLoad, 'r')
    nRows = sum(1 for line in distmat)
    new = scipy.sparse.csr_matrix( [ nRows,nRows ], dtype=np.int8 ).toarray()
    for line in distmat:
        table[line,:] = [int(num) for num in line.split()]
    #table = [[int(num) for num in line.split()] for line in distmat ]
    distmat.close()
    np.save(organism+'-array', table)

"""
