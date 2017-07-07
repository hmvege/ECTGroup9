

import numpy 
import itertools

sp_states = numpy.loadtxt("inputsp1.txt", skiprows=1)

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


M_fix = 0 

#Specify the number of particles in our space 
N_part = 5

#Construct all the Slater determinants 

SD = list(itertools.combinations(Index_inp, N_part))

print SD
print 
print  
print  "There are ", len(SD), "Slater Determinants in a space with ", len(Index_inp), "sp states and with ", N_part, "particles"
print 
print 

#print SD[0][0]
#print SD[0][1]

SD_M_fix = []

m_tot_SD = 0

#for i in SD:
#  for j in xrange(N_part):
#     m_tot_SD += m_inp[Index_inp.index(int(SD[i][j]))]
#     if (m_tot_SD == 0):
#       SD_M_fix.append(i)

#print SD_M_fix


#print Index_inp.index(int(SD[0][1]))

#print int(SD[0][1])

#print m_inp[Index_inp.index(int(SD[0][1]))] + m_inp[Index_inp.index(int(SD[0][0]))]


#print SD_M_fix
  












