#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 01:29:54 2018

@author: kalagz
"""
# import pandas as pd  # not available in DTC !
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
#from NetworkXmore import read_edgelist
from createPPIN import createAdjMatrix, ChangeNames
import os, csv
import pandas as pd

#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Human_Herpesvirus_6A-3.5.165.tab2.txt"
#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Caenorhabditis_elegans-3.5.165.tab2.txt"
#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.tab2.txt"

#datafile = "EdgeLists/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.tab2.txt.edgelist"
#datafile = "EdgeLists/BIOGRID-ORGANISM-Homo_sapiens-3.5.165.tab2.txt.edgelist"

#FolderToParse = "C:\Users\giork\Dropbox\Oxford Documents\2. Programming\Programming_Project\EdgeLists"
#FolderToParse = "EdgeLists/"

# Work with csv module instead of pandas
datafile = "EdgeLists/BIOGRID-ORGANISM-Homo_sapiens-3.5.165.edgelist"
datafile = "EdgeLists/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.edgelist"
datafile = "../../edge_list.txt"
#print("translate edgelist")
Dictionary = ChangeNames( datafile )

edgelist = open(datafile, 'rb')
G = nx.Graph()
#with open(datafile, 'rb') as edgelist:
#    edge = csv.reader(edgelist, delimiter=' ')
#    G.add_edges_from( edge )

# how to read from "edgelist" files whereas nodes are seperated by commas.
edgelist = pd.read_csv(datafile, delimiter=' ', header = None) 
G.add_edges_from( edgelist.values )

M = G.number_of_edges()
N = G.number_of_nodes()
print("There are {0} nodes and {1} edges in the graph.".format(N,M) )
#S = createAdjMatrix( G, "Sample" )

#### Node Ranking - script in DTC computers


#####################################
## Basic statistics of (all) PPINS ##
#####################################
"""
f = open('PPIN_Latex_Table.txt','w')
allfiles = os.listdir( FolderToParse )
for organism in allfiles:
    FileToLoad = FolderToParse + organism
    # Get the name:
    name = FileToLoad
    while name.find("/") > 0:
        name = name[name.find("/")+1:] # delete the prefix: folders etc
    # delete the suffix:
    shortname = name[ len("BIOGRID-ORGANISM-") :  (len(name)-len("-3.5.165.tab2.txt")) ]
    name = name[ : (len(name) -len(".tab2.txt")) ]
    # Progress Check
    #print("Analyzing PPIN for organism:\n"+shortname)
    # load edgelist - there is no header and '-' is used for separation
    edgelist = pd.read_csv(FileToLoad, header=None, delimiter=' ')
    G = nx.Graph()
    G.add_edges_from( (edgelist.values) )

    N = G.number_of_nodes()
    M = G.number_of_edges()
    print("There are {0} nodes and {1} edges in the graph.".format(N,M) )
    shortname = shortname.replace('_', " \ ") # this is to make gaps for latex

    # Get the number of connected components
    concomps = nx.number_connected_components(G)
    # Get the size of the largest component
    largest = len( sorted(nx.connected_components(G), key = len, reverse=True)[0] )
    # Compute the average degree - take values from dict, then transform to list
    degrees = list( G.degree().values() )

    # nx.degree_centrality(G)).values()
    f.write("$ {0} $ & {1} & {2} & {3:.2f} & {4} & {5} \\\\ \n".format( shortname, N, M, np.mean(degrees), concomps, largest ))
f.close()
"""
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
"""
