

import numpy 
import itertools

sp_states = numpy.loadtxt("inputsp.txt", skiprows=1)

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

j_inp = [0.5 * j for j in tj_inp]
m_inp = [0.5 * j for j in tm_inp]


#Number of sp states
N_sp = len(n_inp)

#Matrix to store the M scheme
m_scheme = []

for i in range(0,len(Index_inp)):
   for j in range(i+1, len(Index_inp)):
     m_scheme.append( ((i+1,j+1),m_inp[i]+m_inp[j]) )




#Specify the number of particles in our space 
N_part = 4

#Construct all the Slater determinants 

SD = list(itertools.combinations(Index_inp, N_part))

print SD
print 
print  
print  "There are ", len(SD), "Slater Determinants in a space with ", len(Index_inp), "sp states and with ", N_part, "particles"
print 
print 



#Set up M-scheme

M_fix = 0  #Fix total M

SD_M_fix = []   #Slater Determinants with fixed M 


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
  












