import numpy as np, matplotlib.pyplot as plt, sys

# Constants
deltaHc=7.2890
deltanc=8.0713
c = 1e8 # m/s
e = 1 # eV
hbar = 6.582119514*1e-16 # Ev * s / rad

# Protons
Z_Ra223 = 88
Z_C14 = 6
Z_Pb209 = 82

# Total number of neutrons
N_Ra223 = 135
N_C14 = 8
N_Pb209 = 127

# Masses
m_Ra223 = 223.0185022 # u
m_C14 = 14.003241 # u
m_Pb209 = 208.98109012 # u

# Binding energies, Radon 223, Carbon 14, Lead 209
BE_Ra223 = 1710.106 # MeV
delta_BE_Ra223 = 0.009
BE_C14 = 105.284
delta_BE_C14 = 0.0
BE_Pb209 = 1640.367
delta_BE_Pb209 = 0.002

def BE(N,Z,deltaNZ):
	# Gets the binding energy
	return Z*deltaHc**2 + N*deltanc - deltaNZ*c*c

def Q(BE_initial=[], BE_final=[], BE_initial_std=[], BE_final_std=[]):
	if len(BE_initial) != len(BE_initial_std):
		raise IndexError("Initial binding energy lists of not equal length.")
	if len(BE_final) != len(BE_final_std):
		raise IndexError("Final binding energy lists of not equal length.")
	sum_before = 0
	sum_before_std = 0
	sum_after = 0
	sum_after_std = 0
	for i in xrange(len(BE_initial)):
		sum_before += BE_initial[i]
		sum_before_std += (BE_initial_std[i]/BE_initial[i])**2
	for i in xrange(len(BE_final)):
		sum_after += BE_final[i]
		sum_after_std += (BE_final_std[i]/BE_final[i])**2
	Q_val = sum_after - sum_before
	Q_val_std = np.sqrt(sum_before_std + sum_after_std)
	return Q_val, Q_val_std

Q_value, Q_value_std = Q([BE_Ra223], [BE_C14, BE_Pb209], [delta_BE_Ra223], [delta_BE_C14,delta_BE_Pb209])

print Q_value

# Strong interaction potential radius
Rd = 1.2*(Z_Pb209+N_Pb209)**(1./3)
Rt = 1.2*(Z_Ra223+N_Ra223)**(1./3)
Rc = 2*Z_Ra223*e**2/Q_value
x = np.sqrt(Rt/Rc)


mu = m_Pb209*m_C14/(m_Pb209+m_C14) # Reduced mass
W_C = np.sqrt(Q_value/(2*mu*Rt**2))
P = np.exp(-4*Z_C14*e*e*np.sqrt(2*mu/(Q_value*hbar**2))*(np.arccos(x)-x*np.sqrt(1-x**2)))

T_half_life = np.log(2)/(W_C*P)
print T_half_life