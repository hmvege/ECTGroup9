# Homework
#reading in files with pandas

import numpy as np
import matplotlib.pyplot as plt  
import pandas as pd 

# reading in file using pandas
# skip first row

Info_audi16 = pd.read_csv ('C:\\aaa\\nushellx\\toi\\mass-data\\mass-data-2016\\aud16.dat', skiprows=[0], delim_whitespace=True, usecols=[0,1,2,3])

iz_info=Info_audi16['iz'] # number of protons
ia_info=Info_audi16['ia'] #  mass
BE_info=Info_audi16['BE'] # binding energy
keV_info=Info_audi16['(keV)'] # error


neutron_number=ia_info-iz_info # annoying because of the two (keV) columns. should be fixed
Info_audi16=Info_audi16.assign(neutron_number=neutron_number.values)
Info_audi16.sort_values(['neutron_number','iz'], ascending=[True, True], inplace=True)
Info_audi16=Info_audi16.reset_index(drop=True)
print(Info_audi16)

#could be done in smarter way... 
iz_info=Info_audi16['iz'] # number of protons
ia_info=Info_audi16['ia'] #  mass
BE_info=Info_audi16['BE'] # binding energy
keV_info=Info_audi16['(keV)'] # error
neutron_number=Info_audi16['neutron_number']

one_proton_be=[]
two_protons_be=[]
protons_one=[]
neutrons_one=[]

for i in range(len(BE_info)-2):
		if neutron_number[i]==neutron_number[i+2]:
			e1=BE_info[i+1]-BE_info[i]
			e2=BE_info[i+2]-BE_info[i]
			if e1>0 and e2<0:
				plt.plot(neutron_number[i],e1, 'ro')
				plt.plot(neutron_number[i],e2, 'bo')
plt.show()