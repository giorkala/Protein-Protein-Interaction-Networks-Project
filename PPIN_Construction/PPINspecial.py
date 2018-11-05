# -*- coding: utf-8 -*-
"""
Centrality and other analysis for specific PPINs
"""
datafile = "EdgeLists/BIOGRID-ORGANISM-Homo_sapiens-3.5.165.edgelist"
#datafile = "EdgeLists/BIOGRID-ORGANISM-Human_Immunodeficiency_Virus_1-3.5.165.edgelist"
#datafile = "EdgeLists/BIOGRID-ORGANISM-Escherichia_coli_K12_W3110-3.5.165.edgelist"
#datafile = "EdgeLists/BIOGRID-ORGANISM-Human_Herpesvirus_6A-3.5.165.edgelist"

#distances = "H:/Distmat/Human_Herpesvirus_6A"
#dictionary = "Dictionaries/Human_Herpesvirus_6A.dictionary"

# import pandas as pd  # IF available !
import numpy as np
import networkx as nx
#from NetworkXmore import read_edgelists
import csv, operator, time
import scipy.stats
from PPINutils import MyCloseness

# Get the name:
name = datafile
while name.find("/") > 0:
    name = name[name.find("/")+1:] # delete the prefix: folders etc
# delete the suffix:
name = name[ len("BIOGRID-ORGANISM-") :  (len(name)-len("-3.5.165.tab2.txt")) ]

# OPEN without pandas
G = nx.Graph()
with open(datafile, 'r') as edgelist:
    edge = csv.reader(edgelist, delimiter=' ')
    G.add_edges_from( edge )

M = G.number_of_edges()
N = G.number_of_nodes()
# Progress Check
print("\nThere are {0} nodes and {1} edges in the graph of \n{2}\n".format(N, M, name) )
###########################
## Centrality estimation ##
###########################
# Select k for top-k showing
topk = 15;
distances = "/auto/dtchome/kalantzisg/Distmat/"+name; dictionary = "Dictionaries/"+name+".dictionary"
RankingMethods = {}
RankingMethods["Degree"] = "nx.degree_centrality(G)"
RankingMethods["PageRank"] = "nx.algorithms.pagerank_scipy(G)"
RankingMethods["HITS-Hubs"] = "nx.algorithms.hits_scipy(G)[0]"
RankingMethods["Katz centrality"] = "nx.algorithms.katz_centrality_numpy(G)"
#RankingMethods["Betweeness Centrality"] = "nx.betweenness_centrality(G)"
#RankingMethods["Closeness Centrality"] = "nx.closeness_centrality(G)"
RankingMethods["My Closeness Centrality"] = "MyCloseness( distances, dictionary )"

Results = []; Rankings = np.zeros( [N, len(RankingMethods)] )
case = 0 # index that counts the number of ranking methods
Order = [] # List to "save" the order that ranking methods are implemented
TotalTime = []
for method in RankingMethods.keys():
    print( "Getting the {0} most central elements wrt {1}...".format( topk, method) )
    start = time.clock()
    ranking = eval( RankingMethods[method] )
    TotalTime.append( time.clock() - start )
    Rankings[ :, case] = list( ranking.values() )
    sorted_dict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
    for x in range( topk ):
        print( sorted_dict[x] )
        #NotableNodes[ x , case ] = sorted_dict[x][0]
        Results.append( sorted_dict[x][0] )
    Order.append( method )
    print("Time duration for {0} = {1}".format(method, TotalTime[case]) )
    case += 1

best = { x: Results.count(x) for x in set(Results) }
best = sorted(best.items(), key=operator.itemgetter(1), reverse=True)
print("The most frequent nodes are:")
for x in range( 5 ):
    print( best[x][0] )
np.save(name+'-'+str(case)+'-Centralities.npy', Rankings[:,:case])

Kendalltaus = np.zeros([case,case])
SpearmanRs = np.zeros([case,case])
for i in range(case):
    for j in range( i+1, case):
        Kendalltaus[i,j] = scipy.stats.kendalltau(Rankings[:, i] , Rankings[:, j])[0]
        Kendalltaus[j,i] = scipy.stats.kendalltau(Rankings[:, i] , Rankings[:, j])[0]
        SpearmanRs[i,j] = scipy.stats.spearmanr(Rankings[:, i] , Rankings[:, j])[0]
        SpearmanRs[j,i] = scipy.stats.spearmanr(Rankings[:, i] , Rankings[:, j])[0]
"""
#########################
## Degree Distribution ##
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
fig.savefig( name+"-DD.eps" )
plt.show()
"""
