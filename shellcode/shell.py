

import numpy as np
import itertools

#filename=str(raw_input("enter the filename \n"))


#sp_states = np.loadtxt("{}".format(filename), skiprows=1)

sp_states = np.loadtxt("usdbint.txt", skiprows=1)
mels = np.loadtxt("melsusdbint.txt", skiprows=1)

Index_inp = []
n_inp = []
l_inp = []
tj_inp = []
tm_inp = []
sp_energies = []

pqrs = []



for i in range(0,len(sp_states)): 
    Index_inp.append(sp_states[i][0])
    n_inp.append(sp_states[i][1])
    l_inp.append(sp_states[i][2])
    tj_inp.append(sp_states[i][3])
    tm_inp.append(sp_states[i][4])
    sp_energies.append(sp_states[i][5])

for i in range(0, len(mels)):
   pqrs.append((mels[i][0], mels[i][1], mels[i][2], mels[i][3], mels[i][4]))




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

 
N_part = int(raw_input("enter the number of particles \n"))

if (N_part > N_sp):
  print "FATAL ERROR: NUMBER OF PARTICLES IS GREATER THAN THE NUMBER OF SP STATES. PROGRAM STOPS"
  quit()

#Construct all the Slater determinants 

SD = list(itertools.combinations(Index_inp, N_part))

print SD
print 
print  
print  "There are ", len(SD), "Slater Determinants in a space with ", len(Index_inp), "sp states and with ", N_part, "particles"
print 
print 



#Set up M-scheme

#M_fix = 0 #float(raw_input("enter M \n"))  #Fix total M

SD_M_fix = []   #Slater Determinants with fixed M 

#Taking into account only sum of m

for M_fix in range(-8,8):
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

#Taking into account also different n

#### We can only include states with same n, here we retrieve states with the same (n,l,j) from all the SD with M=0

if (N_part % 2 == 0):

 #for i in SD_M_fix: 
 # for j in range(N_part/2):
 #   if (n_inp[Index_inp.index(np.split(np.asarray(i),2)[j][0])] == n_inp[Index_inp.index(np.split(np.asarray(i),2)[j][1])] and 
 #       l_inp[Index_inp.index(np.split(np.asarray(i),2)[j][0])] == l_inp[Index_inp.index(np.split(np.asarray(i),2)[j][1])] and
 #       j_inp[Index_inp.index(np.split(np.asarray(i),2)[j][0])] == j_inp[Index_inp.index(np.split(np.asarray(i),2)[j][1])]):
 #           SD_M_fix_new.append(np.split(np.asarray(i),2)[j])


 for i in SD_M_fix: 
  for j in range(N_part/2):
               SD_M_fix_new.append(np.split(np.asarray(i),N_part/2)[j])


 #print SD_M_fix_new

 SD_M_fix_new = [tuple(i) for i in SD_M_fix_new]

 SD_M_fix_new = list(set(SD_M_fix_new))

 
  ####### WE HAVE TO JOIN THE PAIRS IN NPART/2 IN GENERAL WAY!!!!


 SD_trial = list(itertools.combinations(SD_M_fix_new,N_part/2))  #All possible combinations of pairs with same quantum numbers

 SD_trial = [[j for j in i] for i in SD_trial]

 SD_trial2 = []

 for k in range(len(SD_trial)):
  SD_trial2.append(tuple(j for i in SD_trial[k] for j in (i if isinstance(i, tuple) else (i,))))

 SD_trial2.sort()

 SD_M_fix_new1 = []

 for i in SD_trial2:
  if (tuple(sorted(i)) in SD_M_fix):
    SD_M_fix_new1.append(tuple(sorted(i)))

 SD_M_fix_new1.sort()
 

 SD_M_fix = list(set(SD_M_fix_new1))

 SD_M_fix.sort()
 
 print 
 print "CORRECT SD WITH M FIXED AND GOOD QUANTUM NUMBERS FOR PAIRS"
 print 
 print SD_M_fix
 print 
 print "THERE ARE ", len(SD_M_fix) 


###################  

# Functions to compute the matrix elements
  

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
     

  if (SD_new == []):
    return SD_new
      

   

  for i in SD_new: 
    if (i == q or i == p):
      SD_new = []
  SD_new.insert(0,q)
  SD_new.insert(0,p)
  SD_new.sort()
  
  if (len(SD_new) != len(x)):
    SD_new = []
  
  return SD_new

def Update_SD1(x,p,q,s,r):
 #Update SD (x) when we apply the interaction operator ap+ aq+ as ar
  SD_new = x[:]
  perms = []
  for i in range(len(x)): 
   for j in range(i+1,len(x)):
     if ((x[i] == s and x[j] == r) or (x[j] == s and x[i] == r)):
       SD_new[i], SD_new[j] = 0,-1
  
  if (SD_new == x):
    SD_new = []
    return SD_new

  for i in range(len(x)):
    if (SD_new[i] == q or SD_new[i] == p):
      SD_new = []
      break 
    elif (SD_new[i] == 0):
      SD_new[i] = p
    elif (SD_new[i] == -1):
      SD_new[i] = q
  
  return SD_new

def Check_SD(x):
  for i in SD_M_fix:
    if (x == i):
      return [1, SD_M_fix.index(i) ]
      break 
  return [0 ,SD_M_fix.index(i) ]

def perm_sorted2(x):
  s = 0 
  sortflag = False

  while not sortflag: 
    sortflag = True 
    for i in range(len(x)-1): 
      if (x[i] > x[i+1]): 
        sortflag = False 
        s = s + 1 
        x[i], x[i+1] = x[i+1], x[i]

  if (s == 0):
   return True
  elif (s % 2 == 0):
   return True 
  else: 
   return False


SD_M_fix = [list(i) for i in SD_M_fix]

##############################################################################

#### EXAMPLES IN FCI MINTED FOR DIFFERENT INPUT OF SP STATES. CAREFUL, YOU MAY HAVE TO MODIFY THE INPUT CODE TO MAKE IT WORK

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

###################################################################################


###################################################################################

#        SHELL MODEL PROJECT ON SD SHELL WITH A PAIR BASIS STARTS HERE!!!!


###################################################################################


# Build hamiltonian matrix with pairing Hamiltonian FCI-minted pag 29

Hmat = np.zeros((len(SD_M_fix),len(SD_M_fix)))   #Initialize  

g = 1.0   #Strength 

scale_factor = (18.0/(16+N_part)) ** 0.3

#for p in range(len(Index_inp)): 
# for q in range(p+1, len(Index_inp)):
#   for s in range(len(Index_inp)): 
#    for r in range(s+1,len(Index_inp)):
#      for i in range(len(SD_M_fix)):
#        if (Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[0] == 1):
#               Hmat[(i,Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[1])] = -g


#Hamiltonian matrix including the matrix elements from USDB interaction 


for i in range(len(SD_M_fix)):
  updatesort = 0
  for j in pqrs:
    updatesort = sorted(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))
    if (Check_SD(updatesort)[0] == 1):
     if (perm_sorted2(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2])) == True):
   #   Hmat[(i,Check_SD(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1])] += g * j[4]
       Hmat[(i,Check_SD(updatesort)[1])] += g * j[4]
     # if (i != Check_SD(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1]):
     #  Hmat[(Check_SD(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1], i)] = Hmat[(i,Check_SD(Update_SD(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1])]
     elif (perm_sorted2(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2])) == False): 
   #   Hmat[(i,Check_SD(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1])] -= g * j[4]
       Hmat[(i,Check_SD(updatesort)[1])] -= g * j[4]
     # if (i != Check_SD(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1]):
     #  Hmat[(Check_SD(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1], i)] = Hmat[(i,Check_SD(Update_SD(SD_M_fix[i],j[0],j[1],j[3],j[2]))[1])]
       




for i in range(len(SD_M_fix)):
 for j in range(len(SD_M_fix)):
   if (i != j and Hmat[i,j] != 0):
      Hmat[j,i] = Hmat[i,j]


#There is a factor of two in the diagonal from the two body operator 
#for i in range(len(SD_M_fix)):
#  Hmat[(i,i)] = 2 * Hmat[(i,i)] 



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
#    #  print i,j
#        Hmat[(i,i)] += delta * (i+1) / 2.0  

#Include the sp energies in the hamiltonian matrix from the one body operator (diagonal)


for i in range(len(SD_M_fix)):
  for j in range(N_part):
    Hmat[(i,i)] += sp_energies[Index_inp.index(SD_M_fix[i][j])]        


#Check if hamiltonian matrix is symmetric
print 
print "Is Hmat symmetric?"
print
print np.allclose(Hmat, Hmat.T)
print 


#print Hmat
    
eigVal,eigVec = np.linalg.eigh(Hmat)

print 
print "Eigenvalues: "
print
print 
print eigVal


####PROBLEM WITH THE PHASE. IT DOESNT WORK

#print eigVec

np.savetxt("Hmatrix.txt", Hmat, fmt="%.2f")

np.savetxt("Energies.txt", eigVal, fmt="%.4f")


#print SD_M_fix[5]
#print pqrs[2]
#print Update_SD1(SD_M_fix[5],pqrs[2][0],pqrs[2][1],pqrs[2][3],pqrs[2][2])

#print sorted(Update_SD1(SD_M_fix[5],pqrs[2][0],pqrs[2][1],pqrs[2][3],pqrs[2][2]))

#print Check_SD(Update_SD1(SD_M_fix[5],pqrs[2][0],pqrs[2][1],pqrs[2][3],pqrs[2][2]))

#print Check_SD(sorted(Update_SD1(SD_M_fix[5],pqrs[2][0],pqrs[2][1],pqrs[2][3],pqrs[2][2])))


#updatesort = 0

#print "FINAL " 
#print SD_M_fix[5]
#for j in pqrs:
#  updatesort = sorted(Update_SD1(SD_M_fix[5],j[0],j[1],j[3],j[2]))
#  if (Check_SD(updatesort)[0] == 1):
#   if (perm_sorted2(Update_SD1(SD_M_fix[5],j[0],j[1],j[3],j[2])) == True):
#    print Update_SD1(SD_M_fix[5],j[0],j[1],j[3],j[2])
#    print updatesort
#    print j 
#    print Check_SD(Update_SD1(SD_M_fix[5],j[0],j[1],j[3],j[2]))


#print Check_SD(Update_SD1(SD_M_fix[5],j[0],j[1],j[3],j[2]))




## Counting permutations in sorting 

#print SD_M_fix[0]

l = [1, 2, 3, 5, 4, 6]

def perm_sorted(x):
  s = 1
  for item in x:
    if item == s:
      s += 1
  return len(x) - s + 1


def perm_sorted1(x):
  s = 0
  t = 0
  for i in range(len(x)-1): 
    if (x[i] > x[i+1]):
      t = x[i+1] 
      x[i+1] = x[i]
      x[i] = t
      s = s + 1
  return s 
  return x 

#def perm_sorted2(x):
#  s = 0 
#  sortflag = False

#  while not sortflag: 
#    sortflag = True 
#    for i in range(len(x)-1): 
#      if (x[i] > x[i+1]): 
#        sortflag = False 
#        s = s + 1 
#        x[i], x[i+1] = x[i+1], x[i]
#  if (s % 0 == 0):
#   return True
#  else: 
#   return False


s = 1
for item in SD_M_fix[0]:
  if item == s:
    s += 1
#print len(SD_M_fix[0]) - s + 1  


###COMPUTE SD WITHOUT SORTING

def Update_SD1(x,p,q,s,r):
 #Update SD (x) when we apply the interaction operator ap+ aq+ as ar
  SD_new = x[:]
  perms = []
  for i in range(len(x)): 
   for j in range(i+1,len(x)):
     if ((x[i] == s and x[j] == r) or (x[j] == s and x[i] == r)):
       SD_new[i], SD_new[j] = 0,-1
  
  if (SD_new == x):
    SD_new = []
    return SD_new

  for i in range(len(x)):
    if (SD_new[i] == q or SD_new[i] == p):
      SD_new = []
      break 
    elif (SD_new[i] == 0):
      SD_new[i] = p
    elif (SD_new[i] == -1):
      SD_new[i] = q
  
  return SD_new

def Check_SD1(x):
  for i in SD_M_fix:
    if (x == i):
      return [1, SD_M_fix.index(i) ]
      break 
  return [0 ,SD_M_fix.index(i) ]



#print Update_SD1([1,4,3,2],8,9,3,2)

#print perm_sorted2([1,4,8,9])





























