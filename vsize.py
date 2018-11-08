#plots tfd with respect to number of nodes, both in the original graph
import os
import linecache
import matplotlib.pyplot as plt
sizes=[]
tfds=[]
for filename in os.listdir('TFD'):
	sizes.append(int(linecache.getline('Sizes/'+filename, 1).split(": ")[1]))
	tfds.append(float(linecache.getline('TFD/'+filename, 1)))
plt.plot(sizes,tfds)
plt.show()
