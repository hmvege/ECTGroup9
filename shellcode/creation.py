import numpy as np
import itertools

sp_states = np.loadtxt("sdshell.txt", skiprows=1)
#print(sp_states)


# # limit the space 


model_space='full'

if model_space=='d5_2':
	sp_states_d1=sp_states[:7]
elif model_space=='d5_2s1_2':
	sp_states_d1=sp_states[:9]
elif model_space=='full':
	sp_states_d1=sp_states
	print(sp_states_d1)