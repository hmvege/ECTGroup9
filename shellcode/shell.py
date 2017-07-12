

import numpy as np
import itertools

#filename=str(raw_input("enter the filename \n"))


#sp_states = np.loadtxt("{}".format(filename), skiprows=1)

sp_states = np.loadtxt("inputsp3.txt", skiprows=1)

Index_inp = []
n_inp = []
l_inp = []
tj_inp = []
tm_inp = []



for i in range(0,len(sp_states)): 
    Index_inp.append(sp_states[i][0])
    n_inp.append(sp_states[i][1])
    l_inp.append(sp_states[i][2])
    tj_inp.append(sp_states[i][3])
    tm_inp.append(sp_states[i][4])


Index_inp = [int(i) for i in Index_inp]
j_inp = [0.5 * j for j in tj_inp]
m_inp = [0.5 * j for j in tm_inp]


#Number of sp states


N_sp = len(n_inp)

#Matrix to store the M scheme
#m_scheme = []

#for i in range(0,len(Index_inp)):
#   for j in range(i+1, len(Index_inp)):
#     m_scheme.append( ((i+1,j+1),m_inp[i]+m_inp[j]) )


#print "M SCHEME "
#print m_scheme 
#print "M SCHEME "




#Specify the number of particles in our space

 
N_part = 4 #int(raw_input("enter the number of particles \n"))

#Construct all the Slater determinants 

SD = list(itertools.combinations(Index_inp, N_part))

print SD
print 
print  
print  "There are ", len(SD), "Slater Determinants in a space with ", len(Index_inp), "sp states and with ", N_part, "particles"
print 
print 



#Set up M-scheme

M_fix = 0 #float(raw_input("enter M \n"))  #Fix total M

SD_M_fix = []   #Slater Determinants with fixed M 

#Taking into account only sum of m

#for i in SD:
#  m_tot_SD = 0
#  for j in xrange(N_part):
#     m_tot_SD = m_tot_SD + m_inp[Index_inp.index(int(i[j]))]
#  if (m_tot_SD == M_fix):
#    SD_M_fix.append(i)

#Taking into account also different n



for i in SD:
  m_tot_SD = 0
  for j in xrange(N_part):
    m_tot_SD = m_tot_SD + m_inp[Index_inp.index(int(i[j]))]
  if (m_tot_SD == M_fix):
    SD_M_fix.append(i)


print SD_M_fix
print 
print "There are ", len(SD_M_fix), "Slater Determinants with total M: ", M_fix
print 
print 


SD_M_fix_new = []


#### We can only include states with same n, here we retrieve states with the same n from all the SD with M=0

if (N_part % 2 == 0):

 for i in SD_M_fix: 
  #print np.split(np.asarray(i),2)
  for j in range(N_part/2):
    if (n_inp[Index_inp.index(np.split(np.asarray(i),2)[j][0])] == n_inp[Index_inp.index(np.split(np.asarray(i),2)[j][1])]):
      SD_M_fix_new.append(np.split(np.asarray(i),2)[j])

 SD_M_fix_new = [tuple(i) for i in SD_M_fix_new]

 SD_M_fix_new = list(set(SD_M_fix_new))


 SD_M_fix_new1 = []

 for i in range(len(SD_M_fix_new)):
  for j in range(i+1,len(SD_M_fix_new)):
      SD_M_fix_new1.append(tuple(sorted(list(SD_M_fix_new[i]) + list(SD_M_fix_new[j]))))

 SD_M_fix_new1.sort()

 #print SD_M_fix_new1

 SD_M_fix = SD_M_fix_new1

 print SD_M_fix 


###################  
  

def Update_SD(x,p,q,s,r):
 #Update SD (x) when we apply the interaction operator ap+ aq+ as ar
  SD_new = x[:]
  for i in range(len(x)): 
   for j in range(i+1,len(x)):
     SD_rem = []
     if ((x[i] == s and x[j] == r) or (x[j] == s and x[i] == r)):
      SD_rem.append(s)
      SD_rem.append(r)
      SD_new = list(set(SD_new) ^ set(SD_rem))

  for i in SD_new: 
    if (i == q or i == p):
      SD_new = []
  SD_new.insert(0,q)
  SD_new.insert(0,p)
  SD_new.sort()
  
  if (len(SD_new) != len(x)):
    SD_new = []
  
  return SD_new

def Check_SD(x):
  for i in SD_M_fix:
    if (x == i):
      return [1, SD_M_fix.index(i) ]
      break 
  return [0 ,SD_M_fix.index(i) ]


SD_M_fix = [list(i) for i in SD_M_fix]



#Build the hamiltonian matrix

Hmat = np.zeros((len(SD_M_fix),len(SD_M_fix)))   #Initialize  

g = 2.3   #Strength 

# Build the Hamiltonian matrix for the example of page 28 of FCI-minted

for i in range(len(SD_M_fix)):
 for p in range(len(Index_inp)-1): 
   q = p + 1
   if (j_inp[p] + j_inp[q] != 0):
      pass 
   else: 
     for r in range(len(Index_inp)-1): 
       s = r + 1
       if (j_inp[r] + j_inp[s] != 0):
          pass
       else:
       #   print p+1,q+1,r+1,s+1
        if (Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[0] == 1):
              Hmat[(i,Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[1])] = -g



#print Hmat

eigVal,eigVec = np.linalg.eig(Hmat)

#print eigVal

#print eigVec


# Build hamiltonian matrix with next example 

Hmat = np.zeros((len(SD_M_fix),len(SD_M_fix)))   #Initialize  

g = 2.3   #Strength 



for p in range(len(Index_inp)): 
 for q in range(p+1, len(Index_inp)):
   if (j_inp[p] + j_inp[q] != 0):
    pass 
   else: 
     for s in range(len(Index_inp)): 
      for r in range(s+1,len(Index_inp)):
       if (j_inp[r] + j_inp[s] != 0):
         pass
       else:
         for i in range(len(SD_M_fix)):
          if (Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[0] == 1):
               Hmat[(i,Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[1])] = -g


print
print 
print 
#print Hmat
print 
print 
print 

#Include one body operator term in the hamiltonian matrix

delta = 1.0  #Strength one body operator

#for i in range(len(SD_M_fix)):
#  for j in Index_inp:
#    if (j in SD_M_fix[i]):
      #  print i,j
#        Hmat[(i,i)] += delta * i 


#print Hmat


# Build hamiltonian matrix with pairing Hamiltonian FCI-minted pag 29

Hmat = np.zeros((len(SD_M_fix),len(SD_M_fix)))   #Initialize  

g = 1.0   #Strength 

for p in range(len(Index_inp)): 
 for q in range(p+1, len(Index_inp)):
   for s in range(len(Index_inp)): 
    for r in range(s+1,len(Index_inp)):
      for i in range(len(SD_M_fix)):
        if (Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[0] == 1):
               Hmat[(i,Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[1])] = -g


print SD_M_fix

print
print 
print 
print Hmat
print 
print 
print 

#Include one body operator term in the hamiltonian matrix

delta = 0.0  #Strength one body operator

for i in range(len(SD_M_fix)):
  for j in Index_inp:
    if (j in SD_M_fix[i]):
     #  print i,j
        Hmat[(i,i)] += delta * (i+1) / 2.0


print Hmat
    
eigVal,eigVec = np.linalg.eig(Hmat)

print eigVal

print eigVec


























