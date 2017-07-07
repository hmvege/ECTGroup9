
#First exercise ECT

import numpy as np
import matplotlib.pyplot as plt

#Upload data from aud16

aud16 = np.loadtxt("aud16.dat", skiprows=2)

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

rms13 = np.loadtxt("rms13.dat", skiprows=2, usecols=(0,1,2,3,4))

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


#2) Neutron dripline with semiempirical mass formula

aV = 15.8 
aS = 18.3
aC = 0.714
aA = 23.2
aP = 12

#If we include the pairing term

def Pairing_Term(A,Z):
   "It defines the Pairing term according to Wikipedia"
   if (Z % 2 == 0 and A % 2 == 0):
      return aP/(A ** (1/2))
   elif (A % 2 == 0 and Z % 2 != 0):
      return -aP/(A ** (1/2))
   else: 
      return 0 

#Binding energy in BW formula is the sum of all the terms with correct signs

def BEBW(A,Z):
   return aV*A-aS*A**(2.0/3)-aC*Z**2/(A**(1.0/3))-aA*(A-2*Z)**2/A

#We need to define the neutron separation energy for the calculation of the neutron dripline

def SN(A,Z):
   return BEBW(A,Z) - BEBW(A-1,Z)

#Range of nuclei requested

Z_Range = [36, 37, 38, 39, 40, 41, 42, 43, 44]

#Neutron dripline occurs when SN < 0. Break and print the results when it happens

for Z in Z_Range: 
  for A in range(Z,200):
    if (SN(A,Z) < 0):
      print "For ", Z, "protons, the dripline is ", A-Z, "neutrons. BE: ", BEBW(A,Z)
      break


Ndrip = [78, 81, 83, 85, 88, 90, 93, 95, 97]
fit, cov = np.polyfit(Z_Range, Ndrip,1,cov=True)
errors = np.sqrt(np.diag(cov))
x = np.linspace(Z_Range[0],Z_Range[-1],100)
y = np.polyval(fit,x)

print "a = %g, b = %g" % (fit[0], fit[1])
print "a_err = %.6g, b_err = %.6g" % (errors[0],errors[1])

plt.plot(Z_Range, Ndrip,"o",label="Dripline")
plt.hold(True)
plt.grid(True)
plt.plot(x,y,label=r"$a = %.2f \pm %.2f, b = %.2f \pm %.2f$" % (fit[0], errors[0], fit[1], errors[1]))
plt.legend(loc="best",numpoints=1)
plt.xlabel(r'Proton number, $Z$')
plt.ylabel(r'Neutrons, $N$')
plt.title('Neutron dripline using BW semiempirical mass formula')
plt.savefig("dripline.png",dpi=400)
plt.show()

exit(1)


##############################################################

#3) Differences in rms nuclei with N and N-1

diffrms = []

#For which nuclei do we compute the differences in rms with respect the number of neutrons?
Z_El = 80

N_El = []

N_Elindex = []

#We find the indices where Z_El is in rms13

for i in range(0,len(z)):
   if (z[i] == Z_El):
    N_Elindex.append(i)
    N_El.append(n[i])

#Compute the differences according to the indices computed before

for i in N_Elindex:
  diffrms.append(rms[i+1] - rms[i])

#We delete the last point because we do the differences

del diffrms[-1]
del N_El[-1]


#Plot

#plt.scatter(N_El, diffrms)
#plt.show()


##################################################################################

#1) Nuclei bound to beta decay but unbound to double beta decay 

iz_index1p = []
iz_index0p = []
ZA_bound_1p = []
ZA_bound_2p = []

Q1p = 0
Q2p = 0

iz_nodupe = list(set(iz))

for i in range(0,len(iz)):
  for j in range(i, len(iz)):
     if (iz[j] == iz[i] + 1 and ia[j] == ia[i] + 1):
       Q1p = BE[i] - BE[j]
       if (Q1p < 0):
         ZA_bound_1p.append((iz[j], ia[j]))

for i in range(0,len(iz)):
  for j in range(i, len(iz)):
     if (iz[j] == iz[i] + 2 and ia[j] == ia[i] + 2):
       Q2p = BE[i] - BE[j]
       if (Q2p > 0):
         ZA_bound_2p.append((iz[j], ia[j]))

#print len(list(set( ZA_bound_1p )))
#print len(list(set( ZA_bound_2p )))

total_nuclei = 0

for i in list(set( ZA_bound_1p )):
  for j in list(set( ZA_bound_2p )):
     if (i == j):
       total_nuclei = total_nuclei + 1
 #      print "This nucleus is bound 1p decay and unbound 2p decay: ", i


#print "Total number of nuclei bound 1p decay and unbound 2p decay: ", total_nuclei














