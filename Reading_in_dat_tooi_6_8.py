# Homework
#reading in files with pandas

import numpy as np
import matplotlib.pyplot as plt  
import pandas as pd 
# reading in file using pandas
# skip first row

Info_toi = pd.read_csv ('C:\\Users\\kosor\\Documents\\ECT Talent\\toiee.dat', delim_whitespace=True, usecols=[0,1,2,3,4,5,6,7])


#finfing 6+ states

Info_toi_6_8=Info_toi[(Info_toi['J-pi'].values=='6+') | (Info_toi['J-pi'].values=='8+')]
Info_toi_6_8_even=Info_toi_6_8[(Info_toi_6_8['a'].values%2==0) & (Info_toi_6_8['z'].values%2==0)]
Info_toi_6_8_even=Info_toi_6_8_even.reset_index()

a_info=Info_toi_6_8_even['a'] 
z_info=Info_toi_6_8_even['z']
Jpi_info=Info_toi_6_8_even['J-pi'] 
energy=Info_toi_6_8_even['Ex(MeV)']

element=[]
energy_6_8=[]

for i in range(len(a_info)-1):
	if a_info[i]==a_info[i+1] and z_info[i]==z_info[i+1] and Jpi_info[i]=='6+' and Jpi_info[i+1]=='8+':
		frequency=element.count(z_info[i])
		if frequency<1:
			element.append(z_info[i])
			ener_rat=energy[i]/energy[i+1]	
			energy_6_8.append(energy_6_8)

			plt.plot(z_info[i],ener_rat, 'bo', alpha=0.8)
			plt.text(z_info[i], ener_rat+0.002, '{}'.format(a_info[i]-z_info[i]))
			print(ener_rat, z_info[i], a_info[i], Jpi_info[i], Jpi_info[i+1])
			i+=2
		else:
	
			pass

plt.show()


