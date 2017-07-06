

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


M_fix = 0 
N_part = 2




#Construct all the Slater determinants 

N_sp_string = ''

for i in Index_inp:
    N_sp_string += str(int(i))

SD = list(map("".join, itertools.combinations(N_sp_string, N_part)))

print SD 

#print SD[0][0]
#print SD[0][1]

#SD_M_fix

for i in SD:
  for j in N_part-1:
     int(i[j])


#print SD_M_fix
  












