#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 23:44:29 2018

@author: kalagz
"""
from os import path
#from numba import jit
import sys

#@jit(nopython = True) #, parallel = True)
def createPPIN(pathtofile):
    import pandas as pd
    import networkx as nx
    import matplotlib.pyplot as plt
    import warnings
    # "get" the name from the given path
#    temp = "BioGrid files/"
#    name = pathtofile[len(temp):] # delete the prefix
#    temp = ".tab2.txt"
#    name = name[ : (len(pathtofile) -len(temp)) ] # delete the suffix
    name = pathtofile
    while name.find("/") > 0:
        name = name[name.find("/")+1:] # delete the prefix: folders etc
    # delete the suffix:
    shortname = name[ len("BIOGRID-ORGANISM-") :  (len(name)-len("-3.5.165.tab2.txt")) ]
    name = name[ : (len(name) -len(".tab2.txt")) ]
    # Progress Check
    print("Creating PPIN for organism:\n"+shortname)

    if path.exists(pathtofile):
        data = pd.read_csv(pathtofile, delimiter='\t')
    else:
        warnings.warn("File not found!")
        return 0

    # We select the columns of BIOGRID IDs only
    # 0: interaction ID, 3: Interactor A, 4: Interactor B
    # 7,8: Official symbols - to be saved separately
    ColumnsToKeep = [ list(data)[c] for c in [0,3,4,7,8] ]
    ColumnsToDrop =  set(list(data)) - set(ColumnsToKeep)
    for col in ColumnsToDrop:
        data = data.drop( col , axis = 1 )

    # Progress Check
    print("Data is parsed! Creating new files...")
    # extract official symbols & edgelists to separate files
    f1 = open('EdgeLists/'+name+'.edgelist','w')
    f2 = open('OfficialSymbols/'+name+'.official_symbols.csv','w')
    C1 = list( (data.values)[:,1] )
    C2 = list( (data.values)[:,2] )
    C3 = list( (data.values)[:,3] )
    C4 = list( (data.values)[:,4] )
    for x in range( len(data) ):
        f1.write("{0} {1}\n".format( C1[x], C2[x] ))
        f2.write("{0},{1}\n".format( C3[x], C4[x] ))
    f1.close()
    f2.close()

    # Visualize graph
    # first, take a 2D array from dataframe - these are numerics only
    #G = nx.Graph()
    #G.add_edges_from( data.values[:,[1,2] ] )
    #plt.show()
    #nx.draw_random(G)
    #nx.draw(G,node_size=10, pos=nx.spring_layout(G))
    #plt.savefig('Visuals/'+name+'graph.png')

    print("Job done: .edgelist, .official_symbols and visuals are all created!\n")

def createAdjMatrix( Graph, Name ):
    """
    This function a NetoworkX graph creates a sparse matrix with the adjacencies
    and saves it as a *.npy file. Check if it needs scipy.sparse.save_npz()
    Inputs:
        Graph : NetoworkX graph object
        Name  : string with the name of the graph to save
    Output:
        *.npy file with csr array and
    # it could load edgelists instead... which is assumed as a "node node" (tab) list,
    # The only input is the path to the edgelist.
    """
    import numpy as np
    import networkx as nx

    S = nx.to_scipy_sparse_matrix(Graph, format='csr')
    np.save( Name+'Adjmatrix.csr', S )
    return S

def ChangeNames( oldedgelist ):
    """
    This function translates the huge numbers used for names in BioGrid datasets
    to naming from 1,2,... . First it loads a file with edgelists, then translate
    to "small" names and save a new edgelist file as well as the dictionary.
    """
    import pandas as pd
    import networkx as nx
    import matplotlib.pyplot as plt
    import sys, warnings

    name = oldedgelist
    while name.find("/") > 0:
        name = name[name.find("/")+1:] # delete the prefix: folders etc
    # delete the suffix:
    # shortname = name[ len("BIOGRID-ORGANISM-") :  (len(name)-len("-3.5.165.tab2.txt")) ]
    name = name[ : (len(name) -len(".tab2.txt")) ]
    if path.exists(oldedgelist):
        data = pd.read_csv(oldedgelist, delimiter=' ', header=None)
    else:
        warnings.warn("File not found!")
        return 0

    f = open('Dictionaries/'+name+'.edgelist','w')
    C1 = list( (data.values)[:,0] )
    C2 = list( (data.values)[:,1] )
    counter = 1
    Dict = {}
    for x in range( len(data) ):
        # translate
        if C1[x] not in Dict:
            Dict[ C1[x] ] = counter
            counter += 1
        if C2[x] not in Dict:
            Dict[ C2[x] ] = counter
            counter += 1
        # register edge in edgelist
        f.write("{0} {1}\n".format( Dict[ C1[x] ] , Dict[ C2[x] ] ))
    f.close()
    # now save the dictionary
    f = open('Dictionaries/'+name+'.dictionary','w')
    for key in Dict.keys():
        f.write("{0}:{1}\n".format( Dict[ key ], key ) )
    f.close()

    return Dict

if __name__ == '__main__':
    pathtofile = sys.argv[-1]
    createPPIN( pathtofile )
