import os
import linecache
for filename in os.listdir('TFD2'):
	nb = linecache.getline('TFD2/'+filename, 3)
        nb2 = linecache.getline('TFD2/'+filename, 4)
        if nb2[0]!='[':
		nb+=nb2
	nb=nb.replace('[','').replace('.','').replace(']','').replace(',','').split()
        g=open('NL/'+filename,'w')
	ll=len(nb)+1
	#print(nb)
        for i in range (1,ll):
        	g.write(str(i)+' '+nb[i-1]+'\n')
	g.close()
