import os
import linecache
import matplotlib.pyplot as plt
for filename in os.listdir('TFD2'):
	nb = linecache.getline('TFD2/'+filename, 3)
        nb2 = linecache.getline('TFD2/'+filename, 4)
        if nb2[0]!='[':
		nb+=nb2
		fitted=linecache.getline('TFD2/'+filename, 5)
	else:
		fitted=nb2
        nb=nb.replace('[','').replace('. ','').replace(']','').replace(',','').split()
	fitted=fitted.replace('[','').replace('. ','').replace(']','').replace(',','').split()
        nb=[float(i) for i in nb]
	fitted=[float(i) for i in fitted]
        lboxes=range(1,len(nb)+1)
        #print (nb)
        #print (fitted)
	plt.plot(lboxes,nb,'.-',label='Actual number of boxes')
	plt.plot(lboxes,fitted,'.-',label='Fitted number of boxes')
	plt.xlabel('Length of boxes')
	plt.ylabel('Number of boxes')
	plt.legend(loc='best')
        plt.savefig('Plots/'+filename+'.png')
	plt.clf()
       
