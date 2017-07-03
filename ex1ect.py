
#First exercise ECT

import numpy 

#Upload data from aud16

aud16 = numpy.loadtxt("aud16.dat", skiprows=1)

ia = []
iz = []
BE = []
error = []
i_n = []

for i in range(0,len(aud16)): 
    iz.append(aud16[i][0])
    ia.append(aud16[i][1])
    BE.append(aud16[i][2])
    error.append(aud16[i][3])
    i_n.append(aud16[i][5])


#Upload data from rms13

rms13 = numpy.loadtxt("rms13.dat", skiprows=2, usecols=(0,1,2,3,4))

z = []
n = []
a = []
rms = []
error = []

for i in range(0,len(rms13)):
   z.append(rms13[i][0])  
   n.append(rms13[i][1])  
   a.append(rms13[i][2])  
   rms.append(rms13[i][3])  
   error.append(rms13[i][4])























