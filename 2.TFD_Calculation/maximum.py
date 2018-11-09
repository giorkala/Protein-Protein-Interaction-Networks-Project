import numpy as np
import os
for filename in os.listdir('Distmat'):
	f = open ("Distmat/"+filename , 'r')
	g = open ("Maxima/"+filename , 'w')
	l = [[int(num) for num in line.split()] for line in f ]
	m=np.max(l)
	g.write(str(m))
	f.close()
	g.close()
