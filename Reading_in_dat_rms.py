import numpy as np
import matplotlib.pyplot as plt  
import pandas as pd 

# reading in file using pandas
# skip first row
Info_rms13 = pd.read_csv ('C:\\aaa\\nushellx\\toi\\mass-data\\rms-data-2013\\rms13.dat',skiprows=[0], delim_whitespace=True, usecols=[0,1,2,3,4,5] )

# here everything is shifted by 1 column
z_info_rms13=Info_rms13['!']
n_info_rms13=Info_rms13['z']
a_info_rms13=Info_rms13['n']
rms_info_rms13=Info_rms13['a']
error_info_rms13=Info_rms13['rms']

n_for_plot=[]
data_for_plot=[]
z_for_plot=[]

for i in range(len(n_info_rms13)-1):
	if n_info_rms13[i]==n_info_rms13[i+1]-1:
	#if z_info_rms13[i]==19: # optional if we want to look at a Z
		dif=rms_info_rms13[i+1]-rms_info_rms13[i]

		data_for_plot.append(dif)
		n_for_plot.append(n_info_rms13[i])
		#plt.text(z_info_rms13[i], dif+0.002, '{}'.format(z_info_rms13[i]))


plt.plot(n_for_plot[:-1] ,data_for_plot[:-1], 'ro', alpha=0.5)
plt.show()