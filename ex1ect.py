
#First exercise ECT

import numpy as np, matplotlib.pyplot as plt

#Upload data from aud16

aud16 = np.loadtxt("../nushellx/toi/mass-data/aud16.dat", skiprows=2, usecols=(0,1,2,3,4,5))

ia = aud16[:,0]
iz = aud16[:,1]
BE = aud16[:,2]
error = aud16[:,3]
i_n = aud16[:,4]

#Upload data from rms13

rms13 = np.loadtxt("../nushellx/toi/mass-data/rms13.dat", skiprows=2, usecols=(0,1,2,3,4))

z = rms13[:,0]
n = rms13[:,1]
a = rms13[:,2]
rms = rms13[:,3]
error = rms13[:,4]

# Plotting the variations
# plt.errorbar(z, rms, yerr=error, fmt=".", ecolor="r", label="rms")
plt.plot(iz,BE)
plt.xlabel(r"$Z$",fontsize=20)
plt.ylabel(r"$\bar{r}_s$",fontsize=20)
plt.legend()
plt.show()
