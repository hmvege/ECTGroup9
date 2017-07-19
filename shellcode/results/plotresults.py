
import matplotlib.pyplot as plt
import numpy as np


o18 = np.loadtxt("o18results.txt", skiprows=1)
o20 = np.loadtxt("o20results.txt", skiprows=1)
o22 = np.loadtxt("o22results.txt", skiprows=1)
o24 = np.loadtxt("o24results.txt", skiprows=1)
o26 = np.loadtxt("o26results.txt", skiprows=1)


o18nu = np.loadtxt("o18nushell.txt", usecols=range(5))
o20nu = np.loadtxt("o20nushell.txt", usecols=range(5))
o22nu = np.loadtxt("o22nushell.txt", usecols=range(5))
o24nu = np.loadtxt("o24nushell.txt", usecols=range(5))
o26nu = np.loadtxt("o26nushell.txt", usecols=range(5))

Eo18 = [o18[i][1] for i in range(len(o18))]
Eo20 = [o20[i][1] for i in range(len(o20))]
Eo22 = [o22[i][1] for i in range(len(o22))]
Eo24 = [o24[i][1] for i in range(len(o24))]
Eo26 = [o26[i][1] for i in range(len(o26))]

Eo18nu = [o18nu[i][2] for i in range(len(o18nu))]
Eo20nu = [o20nu[i][2] for i in range(len(o20nu))]
Eo22nu = [o22nu[i][2] for i in range(len(o22nu))]
Eo24nu = [o24nu[i][2] for i in range(len(o24nu))]
Eo26nu = [o26nu[i][2] for i in range(len(o26nu))]

#First five states 

Eo18 = [Eo18[i] for i in range(5)]
Eo20 = [Eo20[i] for i in range(5)]
Eo22 = [Eo22[i] for i in range(5)]
Eo24 = [Eo24[i] for i in range(5)]
Eo26 = [Eo26[i] for i in range(5)]

Eo18nu = [Eo18nu[i] for i in range(5)]
Eo20nu = [Eo20nu[i] for i in range(5)]
Eo22nu = [Eo22nu[i] for i in range(5)]
Eo24nu = [Eo24nu[i] for i in range(5)]
Eo26nu = [Eo26nu[i] for i in range(5)]

#Eo1 = [Eo18[0], Eo20[0], Eo22[0], Eo24[0], Eo26[0]]



plt.plot(range(1,6), (np.asarray(Eo18) - np.asarray(Eo18nu))/np.asarray(Eo18), 'ro-', label = 'O18')
plt.plot(range(1,6), (np.asarray(Eo20) - np.asarray(Eo20nu))/np.asarray(Eo20), 'bo-', label = 'O20')
plt.plot(range(1,6), (np.asarray(Eo22) - np.asarray(Eo22nu))/np.asarray(Eo22), 'go-', label = 'O22')
plt.plot(range(1,6), (np.asarray(Eo24) - np.asarray(Eo24nu))/np.asarray(Eo24), 'mo-', label = 'O24')
plt.plot(range(1,6), (np.asarray(Eo26) - np.asarray(Eo26nu))/np.asarray(Eo26), 'ko-', label = 'O26')


plt.xlabel('Index of state')
plt.ylabel('Relative error')

plt.legend(loc = 2)
plt.show()




#plt.plot(range(17,27,2), Eo1, 'ro-')
#plt.show()



 


