"""
Script that parses all the files end does specific things for all the cases
e.g. creating latex tables or re-labeling graph-nodes
"""
import os
#import pandas as pd
import networkx as nx
from createPPIN import ChangeNames

FolderToParse = "EdgeLists/"
#f = open('PPIN_Latex_Table.txt','w')

allfiles = os.listdir( FolderToParse )
for organism in allfiles:
    FileToLoad = FolderToParse + organism
    ChangeNames( FileToLoad )


"""
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
