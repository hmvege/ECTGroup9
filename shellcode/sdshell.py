##############################################################################
#
#
#       SHELL CODE CALCULATION OF THE ENERGIES OF THE STATES OF OXIGEN 
#        ISOTOPES 18^O-26^O USING THE M-SCHEME 
#
##############################################################################
#       
#
#     INPUT:    - FILENAME WITH THE SP STATES OF SD SHELL
#               - FILENAME WITH MATRIX ELEMENTS OF INTERACTION (USDB)
#               - NUMBER OF PARTICLES ON TOP OF 16^O (4 PARTICLES FOR 20^O,
#                  5 PARTICLES FOR 21^O...)
#
##############################################################################
#
#
#     OUTPUT:   - FILENAME WITH THE HAMILTONIAN MATRIX
#               - FILENAME WITH THE ENERGIES OF THE STATES OF CERTAIN OXYGEN
#                  ISOTOPE   
#
##############################################################################
#
#
#   ENERGIES OF THE STATES OF OXYGEN ISOTOPES ARE COMPUTED DIAGONALIZING A 
#   HAMILTONIAN MATRIX BUILT FROM A GENERAL TWO BODY HAMILTONIAN IN A BASIS
#   OF SLATER DETERMINANTS. ONE BODY ELEMENTS ARE THE SINGLE PARTICLE ENERGIES
#   OF THE STATES IN SD SHELL AND TWO BODY ELEMENTS ARE GIVEN BY THE USDB INT
#
#    BEWARE OF THE REESCALING FACTOR (18/(16+N)) ** 0.3 FOR THE TWO BODY ELS!
#
#
#
#     WORKS PERFECTLY FOR A EVEN. FOR A ODD YOU HAVE TO CHANGE THE TOTAL M IN
#     THE M SCHEME (NOW ONE UNPAIRED PARTICLE)
#
###############################################################################



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


#Specify the number of particles in our space

 
N_part = int(raw_input("enter the number of particles \n"))

scale_factor = (18/(16+N_part)) ** 0.3 

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


SD_M_fix = []   #Slater Determinants with fixed M 

#Taking into account only sum of m

for M_fix in range(-8,8):
 for i in SD:
   m_tot_SD = 0
   for j in xrange(N_part):
     m_tot_SD = m_tot_SD + m_inp[Index_inp.index(int(i[j]))]
   if (m_tot_SD == M_fix):
     SD_M_fix.append(i)


SD_M_fix_new = []

if (N_part % 2 == 0):


 for i in SD_M_fix: 
  for j in range(N_part/2):
               SD_M_fix_new.append(np.split(np.asarray(i),N_part/2)[j])

 SD_M_fix_new = [tuple(i) for i in SD_M_fix_new]

 SD_M_fix_new = list(set(SD_M_fix_new))

 
  ####### WE HAVE TO JOIN THE PAIRS IN NPART/2 IN GENERAL WAY !!!


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



###################################################################################


###################################################################################

#        SHELL MODEL PROJECT ON SD SHELL WITH A PAIR BASIS STARTS HERE!!!!


###################################################################################


# Build hamiltonian matrix with pairing Hamiltonian FCI-minted pag 29

Hmat = np.zeros((len(SD_M_fix),len(SD_M_fix)))   #Initialize  

g = 1.0   #Strength 

scale_factor = (18.0/(16+N_part)) ** 0.3


#Hamiltonian matrix including the matrix elements from USDB interaction 


for i in range(len(SD_M_fix)):
  updatesort = 0
  for j in pqrs:
    updatesort = sorted(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2]))
    if (Check_SD(updatesort)[0] == 1):
     if (perm_sorted2(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2])) == True):
       Hmat[(i,Check_SD(updatesort)[1])] += g * j[4]
     elif (perm_sorted2(Update_SD1(SD_M_fix[i],j[0],j[1],j[3],j[2])) == False): 
       Hmat[(i,Check_SD(updatesort)[1])] -= g * j[4]




for i in range(len(SD_M_fix)):
 for j in range(len(SD_M_fix)):
   if (i != j and Hmat[i,j] != 0):
      Hmat[j,i] = Hmat[i,j]


#Reescale the two body matrix elements only!!!!

for i in range(len(SD_M_fix)):
 for j in range(len(SD_M_fix)):
      Hmat[i,j] = scale_factor * Hmat[i,j]



print
print 
print 
print 
print 
print 

#Include one body operator term in the hamiltonian matrix

delta = 1.0  #Strength one body operator


#Include the sp energies in the hamiltonian matrix from the one body operator (diagonal)


for i in range(len(SD_M_fix)):
  for j in range(N_part):
    Hmat[(i,i)] += delta * sp_energies[Index_inp.index(SD_M_fix[i][j])]        


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

#print eigVec

np.savetxt("Hmatrix.txt", Hmat, fmt="%.2f")

np.savetxt("Energies.txt", eigVal, fmt="%.4f")

