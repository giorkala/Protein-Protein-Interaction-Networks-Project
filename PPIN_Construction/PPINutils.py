#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 23:44:29 2018
@author: giorkala

Functions useful for the first task of the project. That is creating edgelists from
TAB2 files, re-labeling, creating adjacency matrices (and save in *.npy) and computing 
closeness cetrality after providing all the distances.
"""
from os import path

def CreateEdgeList( pathtofile, name ):
    import pandas as pd
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
    # In order to skip multiple copies of the same edge, we use Python's set structure
    EdgeList = set()
    for x in range( len(data) ):
        if C1[x] != C2[x]:
            # in order to avoid self-loops and multiple edges,
            # we consider only min(a,b) - max(a,b)
            edge = "{0} {1}\n".format( min( C1[x], C2[x] ), max( C1[x], C2[x] ))
            if edge not in EdgeList:
                f1.write( "{0} {1}\n".format( C1[x], C2[x] )) # extract the edgelist
                # Extract edge in the official symbols - these might be reversed!
                f2.write( "{0},{1}\n".format( C3[x], C4[x] ))
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
    import pandas as pd
    import warnings

    if path.exists(oldedgelist):
        data = pd.read_csv(oldedgelist, delimiter=' ', header=None)

    else:
        warnings.warn("File not found!")
        return 0

    C1 = list( (data.values)[:,0] )
    C2 = list( (data.values)[:,1] )
    counter = 0
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
    f = open('EdgeLists_Relabeled/'+name+'.edgelist','w')
    for x in EdgeList:
        f.write( x )
    f.close()
    # now save the dictionary for translation
    f = open('EdgeLists_Relabeled/Dictionaries/'+name+'.dictionary','w')
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
    import csv, warnings
    #from scipy import sparse as ssp

    G = nx.Graph()

    if path.exists(edgelist):
        #data = pd.read_csv(oldedgelist, delimiter=' ', header=None)
        # OR
        with open(edgelist, 'r') as edgelist:
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

def MyCloseness( distances , dictionary):
    """
    Function that computes the closeness centality for all the nodes of a graph,
    given the distances between each pair.
    Input:
        distances : Path to file that contains distances between pair of nodes
                    with tab-separated values. It has been constructed in C.
        dictionary: Python dict containing the re-labeling translation
    Output:
        closeness : Dictionary with keys the ID of edges and values the respective
                    closeness centrality.
    """
    import pandas as pd
    import numpy as np
    import csv

   # load the dictionary and bring it in usefull form:
    translator = pd.read_csv(dictionary, delimiter=':', header=None).values
    tosort = np.argsort(translator[:,0])
    #translator[:,0] = translator[ tosort, 0] # this is useless, it's 0,1,2,...
    translator[:,1] = translator[ tosort, 1]

    closeness = {}
    node = 0
    edges = 0
    with open(distances, 'r') as f:
        data = csv.reader(f, delimiter = ' ')
        for row in data:
            dists = np.array( row[:-1] )
            # Last row contains NaNs, so we ommit it
            dists = [int(k) for k in dists]
            # we check if current node is connected with other
            if sum( dists )>0:
                k = np.count_nonzero(dists)
                # k is actually the number of nodes in current component -1 !
                # and len(dists) is the total number of nodes in the graph
                closeness[ str(translator[node,1]) ] =  k**2 /sum( dists )/( len(dists)-1 )
                node += 1
                edges += list(dists).count(1)
                #if dists[node] == 1:
                #    print("Auto-loop found! Node = ", node)
            else:
                # isolated node
                closeness[ str(translator[node,1]) ] =  0
            if ( node%4000 == 0):
                print("More than {0} nodes are processed!".format(node) )
            if node > len(translator):
                print("Fualty nodes were spotted!")
                break

    print("Total nodes found = {0} and total number of edges = {1}".format( node, int(edges/2) ) )
    return closeness

#if __name__ == '__main__':
#return
    #pathtofile = sys.argv[-1]
    #createPPIN( pathtofile )
