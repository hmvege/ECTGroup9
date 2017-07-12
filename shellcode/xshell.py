import numpy as np, itertools

class State:
	def __init__(self, n, l, j, m):
		self.n = n
		self.l = l
		self.j = j
		self.m = m

class Hamiltonian:
	def __init__(self):
		None

	def __call__(self, states):
		raise NotImplementedError("Base Hamiltonian class not functioning. Create subclass with inheritance.")

class XShell:
	def __init__(self, input_file, verbose = False):
		data_input = np.loadtxt("inputsp2.txt", skiprows=1, usecols=(0,1,2,3,4))
		self.index_input = map(int,data_input[:,0])
		self.n_input = data_input[:,1]
		self.l_input = data_input[:,2]
		self.j_input = map(lambda x: 0.5*x, data_input[:,3])
		self.m_input = map(lambda x: 0.5*x, data_input[:,4])
		self.N_sp = len(self.n_input) # number of single particle states states
		# Sets verbose to false is desired
		self.verbose = verbose
		# Default Hamiltonian is None, has to be set manually
		self.hamiltonian = None

	def generate_slater_determinants(self, N_particles):
		"""
		Generates all the possible N particle Slater determinants to be used from our basis.
		"""
		self.SD_list = np.asarray(list(itertools.combinations(self.index_input, N_particles))) -1 # Generating Slater determinants based on indexes
		self.N_particles = N_particles
		if self.verbose:
			print "There are ", len(self.SD_list), "Slater Determinants in a space with ", len(self.index_input), "sp states and with ", N_particles, "particles"
		
		# Unit test for the number of Slater determinants
		self.N_SD_list = int(np.math.factorial(self.N_sp))/(int(np.math.factorial(N_particles))*int(np.math.factorial(self.N_sp - N_particles)))
		if self.N_SD_list != len(self.SD_list):
			raise ValueError("Predicted number of Slater determinants not corresponding with those retrieved.")

	def m_scheme_setup(self, M_fixed):
		"""
		Takes a M, and truncates our system based on this value
		"""
		SD_updated = []
		for sd in self.SD_list:
			if sum([self.m_input[n] for n in sd]) == M_fixed:
				SD_updated.append(sd)
		self.SD_updated = np.asarray(SD_updated)
		self.N_states = len(self.SD_updated)
		self.M_fixed = M_fixed
		if self.verbose:
			print "There are ", self.N_states, "Slater Determinants with total M: ", M_fixed

	def _update_slater_determinant(self):
		None

	def _annihilate(self):
		None

	def _create(self):
		None

	def set_hamiltonian(self, hamiltonian):
		self.hamiltonian = hamiltonian

	def build_hamiltonian(self):
		"""
		Builds Hamiltonian matrix
		"""
		if not self.hamiltonian:
			raise TypeError("A Hamiltonian has not been provided!")
		QM_numbers = zip([self.index_input,self.n_input,self.l_input,self.j_input,self.m_input])
		# self.H = self.hamiltonian(self.SD_updated,QM_numbers)
		H = np.zeros((self.N_states,self.N_states))
		G = 1
		for i in xrange(self.N_states):


		

def simple_hamiltonian(SD_updated, QM_numbers):
	G = 1.0
	return H


def Update_SD(x,p,q,s,r):
 #Update SD (x) when we apply the interaction operator ap+ aq+ as ar
  SD_new = x[:]
  for i in range(len(x)): 
   for j in range(i+1,len(x)):
     SD_rem = []
     if ((x[i] == s and x[j] == r) or (x[j] == s and x[i] == r)):
      SD_rem.append(s)
      SD_rem.append(r)
      SD_new = list(set(SD_new) ^ set(SD_rem))
  for i in SD_new: 
    if (i == q or i == p):
      SD_new = []
  SD_new.insert(0,q)
  SD_new.insert(0,p)
  SD_new.sort()
  if (len(SD_new) != len(x)):
    SD_new = []  
  return SD_new

def Check_SD(x):
  for i in SD_M_fix:
    if (x == i):
      return [1, SD_M_fix.index(i) ]
      break 
  return [0 ,SD_M_fix.index(i) ]

SD_M_fix = [list(i) for i in SD_M_fix]

#Build the hamiltonian matrix
Hmat = np.zeros((len(SD_M_fix),len(SD_M_fix)))   #Initialize  
g = 2.3   #Strength 
# Build the Hamiltonian matrix for the example of page 28 of FCI-minted
for i in range(len(SD_M_fix)):
 for p in range(len(index_input)-1): 
   q = p + 1
   if (j_input[p] + j_input[q] != 0):
      pass 
   else: 
     for r in range(len(index_input)-1): 
       s = r + 1
       if (j_input[r] + j_input[s] != 0):
          pass
       else:
       #   print p+1,q+1,r+1,s+1
        if (Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[0] == 1):
              Hmat[(i,Check_SD(Update_SD(SD_M_fix[i],p+1,q+1,r+1,s+1))[1])] = -g

print Hmat


if __name__ == '__main__':
	N_part = 3
	M_value = 0.5
	input_file = "inputsp2.txt"
	shell = XShell(input_file, True)
	shell.generate_slater_determinants(N_part)
	shell.m_scheme_setup(M_value)
	shell.set_hamiltonian(simple_hamiltonian)