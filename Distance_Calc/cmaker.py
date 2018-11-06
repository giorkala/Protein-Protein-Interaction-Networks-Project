import os
bfs=open("bfs_template.c","r")
bfs_template=bfs.read();
i=1
for filename in os.listdir('../Sizes'):
       sizes=open('../Sizes/'+filename,"r")
       newbfs=open('bfs'+str(i)+'.c',"w")
       for line in sizes:
		#print(line.split(': ')[1])
		bfsi=bfs_template.replace("#define N", "#define N "+line.split(': ')[1])
                bfsi=bfsi.replace('edges=fopen', 'edges=fopen("../Renumbered/'+filename+'","r");') 
		bfsi=bfsi.replace('distances=fopen', 'distances=fopen("../Distmat/'+filename+'","w");') 
                break
       newbfs.write(bfsi)
       newbfs.close()
       sizes.close()
       i+=1

bfs.close()
