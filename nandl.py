import os
import linecache
def writefile (folder):
	newfolder=folder.replace('TFD','NL')
	print(newfolder)
	if not os.path.exists(newfolder):
		os.makedirs(newfolder)
	nb = linecache.getline(folder+filename, 3)
	nb = linecache.getline(folder+filename, 3)
        nextline = linecache.getline(folder+filename, 4)
	i=4
        while len(nextline)>0 and nextline[0]!='[':
		nb+=nextline
		i+=1
		nextline = linecache.getline(folder+filename, i)
	nb=nb.replace('[','').replace('.','').replace(']','').replace(',','').split()
        g=open(newfolder+filename,'w')
	ll=len(nb)+1
        for i in range (1,ll):
        	g.write(str(i)+' '+nb[i-1]+'\n')
	g.close()
for filename in os.listdir('Distmat'):
	writefile('TFD/')
	writefile('TFD_LCC/')
	
