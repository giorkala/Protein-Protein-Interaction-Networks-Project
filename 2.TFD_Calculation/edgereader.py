import os
import glob
if not os.path.exists("Renumbered"):
    	os.makedirs("Renumbered")
if not os.path.exists("Sizes"):
    	os.makedirs("Sizes")
for filename in glob.glob('./*.edgelist'):
        nn=filename.split("-")
        renum=open("Renumbered/"+nn[2],"w")
        sizes=open("Sizes/"+nn[2],"w")
        used=[]
        nodes=0
        edges=0
	with open(filename, "r") as file:	
    		for line in file:
                        edges+=1
       			ls=line.split()
        		if ls[0] not in used:
				used.append(ls[0])
                                nodes+=1
        		qstring=str(used.index(ls[0]))
   			if ls[1] not in used:
				used.append(ls[1])
                                nodes+=1
        		qstring+=(' '+str(used.index(ls[1]))+'\n')
        		renum.write(qstring)
	sizes.write("Number of nodes: "+str(nodes)+"\nNumber of edges: "+str(edges))	
    	renum.close()
	sizes.close()
