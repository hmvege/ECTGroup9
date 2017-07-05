import numpy as np, matplotlib.pyplot as plt, sys

deltaHc=7.2890
deltanc=8.0713
c = 1e8 

def BE(N,Z,deltaNZ):
	Z*deltaHc**2 + N*deltanc - deltaNZ*c*c


BE_ra223 = 1710.106
delta_BE_ra223 = 0.009

BE_C14 = 105.284
delta_BE_C14 = 0.0

BE_Pb209 = 1640.367
delta_BE_Pb209 = 0.002

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
	Q_val = sum_before - sum_after
	Q_val_std = np.sqrt(sum_before_std + sum_after_std)
	return Q_val, Q_val_std

print Q([BE_ra223], [BE_C14, BE_Pb209], [delta_BE_ra223], [delta_BE_C14,delta_BE_Pb209])

