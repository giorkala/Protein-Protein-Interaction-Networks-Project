import os
bfs=open("bfs_template.txt","r")
bfs_template=bfs.read();

# select folder to save file with distances
DistFolder = "/tmp/DistanceFiles"
DistFolder = "DistMats/"
for organism in os.listdir('../PPIN_Construction/EdgeLists_Relabeled/Dictionaries'):
	# get the number of nodes from the re-labeling dictionary
	dictionary = open('../PPIN_Construction/EdgeLists_Relabeled/Dictionaries/'+organism,'r')
	nNodes = 0
	for node in dictionary:
		nNodes += 1
	print("Number of nodes found = ", nNodes )
	# get only the name of the organism
	filename = organism.replace('.dictionary','')
	# file to save C code:
	newbfs = open('BFS_' + filename + '.c','w')

	bfsi=bfs_template.replace("#define N", "#define N " + str(nNodes) )
	# we need the edgelist file
	edgelist = filename + '.edgelist'
	bfsi=bfsi.replace( 'edges=fopen', 'edges=fopen("../PPIN_Construction/EdgeLists_Relabeled/'+edgelist+'","r");' ) 
	distfile = DistFolder + filename + '-Distances.txt'
	bfsi=bfsi.replace( 'distances=fopen', 'distances=fopen("'+distfile+'","w");') 
	# write all C codes
	newbfs.write(bfsi)
	newbfs.close()
bfs.close()
