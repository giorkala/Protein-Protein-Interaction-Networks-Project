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
import os, csv, operator
#import pandas as pd

#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Human_Herpesvirus_6A-3.5.165.tab2.txt"
#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Caenorhabditis_elegans-3.5.165.tab2.txt"
#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.tab2.txt"

datafile = "Dictionaries/edge.egdelist"
datafile = "EdgeLists/BIOGRID-ORGANISM-Homo_sapiens-3.5.165.edgelist"
#datafile = "EdgeLists/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.edgelist"
#datafile = "EdgeLists/BIOGRID-ORGANISM-Escherichia_coli_K12_W3110-3.5.165.edgelist"

# Get the name:
name = datafile
while name.find("/") > 0:
    name = name[name.find("/")+1:] # delete the prefix: folders etc
# delete the suffix:
name = name[ len("BIOGRID-ORGANISM-") :  (len(name)-len("-3.5.165.tab2.txt")) ]
#print("translate edgelist")
#Dictionary = ChangeNames( datafile )

# OPEN without pandas
edgelist = open(datafile, 'rb')
G = nx.Graph()
with open(datafile, 'rb') as edgelist:
    edge = csv.reader(edgelist, delimiter=' ')
    G.add_edges_from( edge )

# OPEN with pandas
#edgelist = pd.read_csv(datafile, delimiter=' ', header = None)
#G.add_edges_from( edgelist.values )

M = G.number_of_edges()
N = G.number_of_nodes()
print("\nThere are {0} nodes and {1} edges in the graph of \n{2}\n".format(N, M, name) )
#S = createAdjMatrix( G, "Sample" )

###########################
## Centrality estimation ##
###########################
# max(stats.iteritems(), key=operator.itemgetter(1))[0]
# instead of sorting and taking the 5 largest elements, we search for the largest
# item five times, instead.

# Select k for top-k showing
topk = 15
RankingMethods = {"Degree":"nx.degree_centrality(G)", "PageRank":"nx.algorithms.pagerank_scipy(G)"}
RankingMethods["HITS-Auth"] = "nx.algorithms.hits_scipy(G)[1]"
#RankingMethods["Katz centrality"] = "nx.algorithms.hits_scipy(G)"
#RankingMethods["Betweeness Centrality"] = "nx.betweenness_centrality(G)"
#NotableNodes = np.zeros( [topk, 3] )
Results = []
case = 0
for method in RankingMethods.keys():
    print( "Getting the {0} most central elements wrt {1}...".format( topk, method) )
    ranking = eval( RankingMethods[method] )
    sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
    for x in range( topk ):
        print( sorted_dict[x] )
        #NotableNodes[ x , case ] = sorted_dict[x][0]
        Results.append( sorted_dict[x][0] )
    #case += 1

best = { x: Results.count(x) for x in set(Results) }
best = sorted(best.items(), key=operator.itemgetter(1), reverse=True)
print("The most frequent nodes are:")
for x in range( 5 ):
    print( best[x][0] )

"""
# 1. Degree Centrality
print( "Getting the {0} most central elements wrt degree...".format(topk) )
ranking = nx.degree_centrality(G)
sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
for x in range( topk ):
    print( sorted_dict[x] )

# 2. PageRank
print("Getting the {0} most central elements wrt PageRank...".format(topk) )
ranking = nx.algorithms.pagerank_scipy(G, alpha=0.85, max_iter=1000)
sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
for x in range( topk ):
    print( sorted_dict[x] )

# 3. HITS authorities
print("Getting the {0} most central elements wrt HITS-Auth...".format(topk) )
nothing , ranking = nx.algorithms.hits_scipy( G )
sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
for x in range( topk ):
    print( sorted_dict[x] )

# 4. Katz centrality
print("Getting the {0} most central elements wrt Katz...".format(topk) )
ranking = nx.algorithms.katz_centrality_numpy( G ) #, max_iter=2500)
sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
for x in range( topk ):
    print sorted_dict[x]

# 5. Betweeness Centrality
print("Getting the {0} most central elements wrt Betweeness Centrality...".format(topk) )
ranking = nx.betweenness_centrality(G)
sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
for x in range( topk ):
    print( sorted_dict[x] )

# 6. Closeness Centrality
print("Getting the {0} most central elements wrt Closeness Centrality...".format(topk) )
ranking = nx.networkx.algorithms.centrality.closeness_centrality(G)
sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True )
for x in range( topk ):
    print( sorted_dict[x] )
"""
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
