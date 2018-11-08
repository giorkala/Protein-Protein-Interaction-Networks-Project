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
import os, csv, operator, collections
#import pandas as pd

filetab2 = "BioGrid files/BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.tab2.txt"
#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Caenorhabditis_elegans-3.5.165.tab2.txt"
#filetab2 = "BioGrid files/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.tab2.txt"

datafile = "Dictionaries/edge.egdelist"
datafile = "EdgeLists/BIOGRID-ORGANISM-Homo_sapiens-3.5.165.edgelist"
datafile = "EdgeLists/BIOGRID-ORGANISM-Human_Herpesvirus_6B-3.5.165.edgelist"
datafile = "EdgeLists/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.edgelist"
#"EdgeLists/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.edgelist"
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
###############
## Visualise ##
###############
    # Visualize graph
    # first, take a 2D array from dataframe - these are numerics only
    #G = nx.Graph()
    #G.add_edges_from( data.values[:,[1,2] ] )
fig = plt.figure()#figsize=(8, 8))
pos = nx.spring_layout(G)  # compute graph layout
#pos = nx.shell_layout(G)
plt.axis('off')
nx.draw(G, pos, node_size=10 )
#components = [list(x) for x in nx.connected_components(G)]
#nx.draw_networkx_nodes(G, pos, node_size=500, node_color=['r','r','g','b','r','g','b'] ) #cmap=plt.cm.RdYlBu,
#nx.draw_networkx_edges(G, pos, alpha=0.6)
pos_higher = {}
for k, v in pos.items():
    more = 1.25*(v[0]**2 + v[1]**2)**0.22
    #pos_higher[k] = (v[0]*x_off, v[1]*y_off)
    pos_higher[k] = (v[0]*more, v[1]*more)
#nx.draw_networkx_labels(G, pos_higher, font_size=11, font_weight='bold')
plt.savefig('Visuals/'+name+'-graph.eps', bbox_inches = 'tight')
plt.show()
"""
#########################
## Degree Distribution ##
#########################
degs = dict( G.degree() )
degrees = sorted( degs.values(), reverse=True )

fig = plt.figure()
plt.subplot(1,3,2)
plt.plot(range(len(degrees)), degrees, 'ro') #,'b-'
plt.subplot(1,3,1)
plt.hist( degs.values(),bins=50, rwidth=0.6 ) #, cnt, width=0.80, color='b')
plt.subplot(1,3,3)
plt.loglog(range(len(degrees)), degrees, 'bo') #,'b-'
#plt.title( "Log-Log Degree Distribution - {0}".format(name) )

fig.savefig( name+"-DD.png" )
plt.show()

###########################
## Centrality estimation ##
###########################

# Select k for top-k showing
topk = 15
RankingMethods = {"Degree":"nx.degree_centrality(G)", "PageRank":"nx.algorithms.pagerank_scipy(G)"}
RankingMethods["HITS-Auth"] = "nx.algorithms.hits_scipy(G)[1]"
#RankingMethods["Katz centrality"] = "nx.algorithms.hits_scipy(G)"
#RankingMethods["Betweeness Centrality"] = "nx.betweenness_centrality(G)"
#NotableNodes = np.zeros( [topk, 3] )
Results = []

for method in RankingMethods.keys():
    print( "Getting the {0} most central elements wrt {1}...".format( topk, method) )
    ranking = eval( RankingMethods[method] )
    sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
    for x in range( topk ):
        print( sorted_dict[x] )
        #NotableNodes[ x , case ] = sorted_dict[x][0]
        Results.append( sorted_dict[x][0] )

best = { x: Results.count(x) for x in set(Results) }
best = sorted(best.items(), key=operator.itemgetter(1), reverse=True)
print("The most frequent nodes are:")
for x in range( 5 ):
    print( best[x][0] )
"""
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
###############
## NON SENSE ##
###############
"""
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

    distmat = open(FileToLoad, 'r')
    nRows = sum(1 for line in distmat)
    new = scipy.sparse.csr_matrix( [ nRows,nRows ], dtype=np.int8 ).toarray()
    for line in distmat:
        table[line,:] = [int(num) for num in line.split()]
    #table = [[int(num) for num in line.split()] for line in distmat ]
    distmat.close()
    np.save(organism+'-array', table)
"""
