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
def CreateEdgeList( pathtofile, name ):
    import pandas as pd
    import matplotlib.pyplot as plt
    import warnings

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

    print("Job done: .edgelist, .official_symbols and visuals are all created!\n")

def CreateAdjMatrix( edgelist , name ):
    """
    This function creates a sparse matrix with the adjacencies and saves it
    as a *.npy file. <? Check if it needs scipy.sparse.save_npz() ?>
    Inputs:
        edgelist : path to file with the edge-list
        name  : string with the name of the graph to save. It could be derived
                from the path, but the function is more general this way.
    Output:
        *.npy file with csr array and
    """
    import numpy as np
    import networkx as nx

    G = nx.Graph()

    if path.exists(edgelist):
        #data = pd.read_csv(oldedgelist, delimiter=' ', header=None)
        # OR
        with open(edgelist, 'rb') as edgelist:
            edge = csv.reader(edgelist, delimiter=' ')
            G.add_edges_from( edge )
        S = nx.to_scipy_sparse_matrix(Graph, format='csr')
        np.save( Name + 'Adjmatrix.csr', S )
        return S
    else:
        warnings.warn("File not found!")
        return 0

def ChangeLabels( oldedgelist, name ):
    """
    This function translates the huge numbers used for labels in BioGrid datasets
    to naming from 1,2,... . First it loads a file with edgelists, then translate
    to "small" labels and save a new edgelist file as well as the dictionary.
    It also removes multiple copies of the same edge or self-loops. This is
    implemented by adding ony "min(a,b) - max(a,b)" for any (a,b) or (b,a) edge
    in a set data structure.
    """
    #import pandas as pd
    # OR
    import csv
    import networkx as nx
    import matplotlib.pyplot as plt
    import sys, warnings

    if path.exists(oldedgelist):
        #data = pd.read_csv(oldedgelist, delimiter=' ', header=None)
        # OR
        data = open(oldedgelist, 'rb')
    else:
        warnings.warn("File not found!")
        return 0

    C1 = list( (data.values)[:,0] )
    C2 = list( (data.values)[:,1] )
    counter = 1
    Dict = {}
    EdgeList = set()
    for x in range( len(data) ):
        # translate
        if C1[x] not in Dict:
            Dict[ C1[x] ] = counter
            counter += 1
        if C2[x] not in Dict:
            Dict[ C2[x] ] = counter
            counter += 1
        # register edge in edgelist - we ommit if it is a self-loop
        if C1[x] != C2[x]:
            # f.write("{0} {1}\n".format( Dict[ C1[x] ] , Dict[ C2[x] ] ))
            # EdgeList.add("{0} {1}\n".format( Dict[ C1[x] ] , Dict[ C2[x] ] ))
            a = min( Dict[ C1[x] ] , Dict[ C2[x] ] )
            b = max( Dict[ C1[x] ] , Dict[ C2[x] ] )
            EdgeList.add("{0} {1}\n".format( a, b ))
    # save in the edgelist file
    f = open('Dictionaries/'+name+'.edgelist','w')
    for x in EdgeList:
        f.write( x )
    f.close()
    # now save the dictionary for translation
    f = open('Dictionaries/'+name+'.dictionary','w')
    for key in Dict.keys():
        f.write("{0}:{1}\n".format( Dict[ key ], key ) )
    f.close()

    return Dict

#if __name__ == '__main__':
#return
    #pathtofile = sys.argv[-1]
    #createPPIN( pathtofile )
