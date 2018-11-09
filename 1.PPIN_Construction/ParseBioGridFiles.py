"""
Script that parses all files from biogrid dataset end does specific things for
all cases, e.g. create edgelists, re-label graph-nodes and produce adjacency matrices.
->The very first task to execute.
"""
import os
from PPINutils  import CreateEdgeList, ChangeLabels, CreateAdjMatrix

InitialFolder = "/auto/dtchome/kalantzisg/Downloads/BIOGRID-ORGANISM-3.5.165.tab2/"
#InitialFolder = "G:/DATASETS/BioGrid/BIOGRID-ORGANISM-tab2/"

allfiles = os.listdir( InitialFolder )
for organismfull in allfiles:
    # "get" organism's name from the given path
    name = organismfull
    while name.find("/") > 0:
        name = name[name.find("/")+1:] # delete the prefix: folders etc
    # delete the suffix:
    shortname = name[ len("BIOGRID-ORGANISM-") :  (len(name)-len("-3.5.165.tab2.txt")) ]
    name = name[ : (len(name) -len(".tab2.txt")) ]

    # Progress Check
    print("Creating PPIN for organism:\n"+shortname)

    BioGridFile = InitialFolder + organismfull
    # this creates new edgelists in "EdgeLists" folder
    CreateEdgeList( BioGridFile, name )

    # The next function takes the "old edgelist" in "EdgeLists" folder
    # and creates a new, re-labeled edgelist as well as a dictionary
    ChangeLabels( 'EdgeLists/' + name + '.edgelist' , shortname )
    # We use only short names as now labels are indepedent of BioGrid.
    # Now we create adjacency matrices. Input can be either type of edgelist
    CreateAdjMatrix( 'EdgeLists/' + name + '.edgelist' , shortname )
    
##############################
