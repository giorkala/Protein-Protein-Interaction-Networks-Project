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
    #data.close()

    # Progress Check
    print("Data is parsed! Creating new files...")
    C1 = list( (data.values)[:,1] )
    C2 = list( (data.values)[:,2] )
    C3 = list( (data.values)[:,3] )
    C4 = list( (data.values)[:,4] )
    f1 = open('EdgeLists/'+name+'.edgelist','w')
    f2 = open('OfficialSymbols/'+name+'.official_symbols.csv','w')
    # In order to skip multiple copies of the same edge, we use
    # Python's set structure
    EdgeList = set()
    for x in range( len(data) ):
        if C1[x] != C2[x]:
            # in order to avoid self-loops and multiple edges,
            # we consider only min(a,b) - max(a,b)
            edge = "{0} {1}\n".format( min( C1[x], C2[x] ), max( C1[x], C2[x] ))
            if edge not in EdgeList:
                f1.write( edge ) # extract the edgelist
                # Extract edge in the official symbols - these might be reversed!
                f2.write("{0},{1}\n".format( C3[x], C4[x] ))
                EdgeList.add( edge )
    f1.close()
    f2.close()

    print("Job done: .edgelist and .official_symbols have been created!\n")

def ChangeLabels( oldedgelist, name ):
    """
    This function translates the huge numbers used for labels in BioGrid datasets
    to naming from 1,2,... . First it loads a file with edgelists, then translate
    to "small" labels and save a new edgelist file as well as the dictionary.
    It also removes multiple copies of the same edge or self-loops. This is
    implemented by adding ony "min(a,b) - max(a,b)" for any (a,b) or (b,a) edge
    in a set data structure.
    --> The last feature is un-necessary since the same job takes place in
        function CreateEdgeList which preceeds.

    """
    #import pandas as pd
    # OR
    import pandas as pd
    import networkx as nx
    import matplotlib.pyplot as plt
    import sys, warnings

    if path.exists(oldedgelist):
        data = pd.read_csv(oldedgelist, delimiter=' ', header=None)

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
    import csv
    from scipy import sparse as ssp

    G = nx.Graph()

    if path.exists(edgelist):
        #data = pd.read_csv(oldedgelist, delimiter=' ', header=None)
        # OR
        with open(edgelist, 'rb') as edgelist:
            edge = csv.reader(edgelist, delimiter=' ')
            G.add_edges_from( edge )
        S = nx.to_scipy_sparse_matrix(G, format='csr')
        np.save( 'AdjMatrices/'+ name + 'Adjmatrix.csr', S )
        # the above might be problematic. save with SSP if possible:
        #ssp.save_npz( 'AdjMatrices/'+ name + 'Adjmatrix.csr', S )
        return S
    else:
        warnings.warn("File not found!")
        return 0
#if __name__ == '__main__':
#return
    #pathtofile = sys.argv[-1]
    #createPPIN( pathtofile )
