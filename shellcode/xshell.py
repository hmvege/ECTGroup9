import numpy as np, itertools

class SingleParticleState:
	def __init__(self, state_index, n, l, j, m, sp_energy = None):
		self.state_index = state_index
		self.n = int(n)
		self.l = l
		self.j = j
		self.m = m
		self.sp_energy = sp_energy

	def __str__(self):
		s = "State index = %2d, n = %2d, l = %4.1f, j = %4.1f, m = %4.1f" % (self.state_index, self.n, self.l, self.j, self.m)
		if self.sp_energy:
			s += ", %4.1f" % sp_energy
		return s


class Hamiltonian:
	def __init__(self):
		None

	def __call__(self, states):
		raise NotImplementedError("Base Hamiltonian class not functioning. Create subclass with inheritance.")

class XShell:
	def __init__(self, input_file, verbose = False):
		"""
		Arguments:
		input_file - file containing quantum numbers (Index, n, l, 2j, 2m)
		(optional) verbose - prints more info
		"""
		data_input = np.loadtxt("inputsp2.txt", skiprows=1, usecols=(0,1,2,3,4))
		self.index_input = map(int,data_input[:,0])
		self.n_input = data_input[:,1]
		self.l_input = data_input[:,2]
		self.j_input = map(lambda x: 0.5*x, data_input[:,3])
		self.m_input = map(lambda x: 0.5*x, data_input[:,4])
		self.N_states = len(self.n_input) # number of single particle states states
		self.states = [SingleParticleState(state_index, n,l,j,m) for state_index,n,l,j,m in zip(range(self.N_states), self.n_input,self.l_input,self.j_input,self.m_input)]
		# Sets verbose to false is desired
		self.verbose = verbose
		# Default Hamiltonian is None, has to be set manually
		self.hamiltonian = None

	def generate_slater_determinants(self, N_particles):
		"""
		Arguments:
		N_particles - number of particles to calculate for
		Generates all the possible N particle Slater determinants to be used from our basis.
		"""
		# self.SD_list = np.asarray(list(itertools.combinations(self.index_input, N_particles))) - 1 # Generating Slater determinants based on indexes
		self.SD_list = np.asarray(list(itertools.combinations(self.states, N_particles))) # Generating Slater determinants based on indexes
		self.N_particles = N_particles
		if self.N_particles > self.N_states:
			raise ValueError("%s particles cannot populate %s single particle states" % (N_particles, self.N_sp))
		if self.verbose:
			print "There are ", len(self.SD_list), "Slater Determinants in a space with ", len(self.index_input), "sp states and with ", N_particles, "particles"
		# Unit test for the number of Slater determinants
		self.N_SD_list = int(np.math.factorial(self.N_states))/(int(np.math.factorial(N_particles))*int(np.math.factorial(self.N_states - N_particles)))
		if self.N_SD_list != len(self.SD_list):
			raise ValueError("Predicted number of Slater determinants not corresponding with those retrieved.")

	def m_scheme_setup(self, M_fixed):
		"""
		Takes a M, and truncates our system based on this value
		"""
		SD_updated = []
		for slater_det in self.SD_list:
			if sum([state.m for state in slater_det]) == M_fixed:
				SD_updated.append(slater_det)
		self.SD_updated = np.asarray(SD_updated) # Updated states that have good M
		self.N_states = len(self.SD_updated)
		self._build_pair_list()
		self.M_fixed = M_fixed
		if self.verbose:
			print "There are ", self.N_states, "Slater Determinants with total M: ", M_fixed

	def _build_pair_list(self):
		# Builds pair list
		self.pair_list = [set([i,j]) for i,j in zip(range(0,self.N_states-3,2),range(1,self.N_states-2,2))] # minus 3 and 2 in order to avoid overstepping!

	def _print_slater_determinants(self, slater_determinants):
		"""
		Prints all the slater determinants.
		"""
		for sd,i in zip(slater_determinants,range(len(slater_determinants))):
			print "Slater determinant: %d" % (i+1)
			self._print_sd(sd)

	def _print_sd(self,sd):
		"""
		Prints the states of a single slater determinant.
		"""
		for state in sd:
			print state		

	def _get_state_index(self,state):
		"""
		Returns a list of the index states
		"""
		return [i.state_index for i in state]

	def build_hamiltonian(self):
		"""
		Builds Hamiltonian interaction matrix.
		"""
		states = self.SD_updated
		H_matrix = np.zeros((self.N_states,self.N_states))

		for alpha in xrange(self.N_states):
			H_matrix[alpha,alpha] = self.applyHamiltonian(alpha,alpha)
			for beta in xrange(alpha+1, self.N_states):
				H_matrix[alpha,beta] = self.applyHamiltonian(alpha,beta)
				H_matrix[beta,alpha] = H_matrix[alpha,beta]
		self.H_matrix = H_matrix

	def solve_interaction_matrix(self):
		"""
		Uses numpy to solve the interaction matrix
		"""
		self.eigen_values, self.eigen_vectors = np.linalg.eigh(self.H_matrix)
		return self.eigen_values, self.eigen_vectors

	def applyHamiltonian(self, alpha, beta):
		G = 1
		alpha_state = self.SD_updated[alpha]
		beta_state = self.SD_updated[beta]
		beta_state_indexes = set(state.state_index for state in beta_state) # Puts state indexes into a set to perform bitwise operations on
		alpha_state_indexes = set(state.state_index for state in alpha_state) 
		annihilation_states = []
		creation_states = []

		# Apply annihilation operators
		for pair in self.pair_list:
			if len(pair & beta_state_indexes) == 2: # If two elements coincide, we can destroy a pair of particles
				annihilation_states.append(beta_state_indexes ^ pair) # Appends only if pair does not exist in beta_state_indexes

		# Apply creation operators
		for pair in self.pair_list:
			for state in annihilation_states:
				if len(pair & state) == 0: # If no elements coincide, we can create a pair of particles
					creation_states.append(state ^ pair)

		return sum([G for state in creation_states if state == alpha_state_indexes])


def test1():
	N_part = 3
	M_value = 0.5
	input_file = "inputsp2.txt"
	shell = XShell(input_file, True)
	shell.generate_slater_determinants(N_part)
	shell.m_scheme_setup(M_value)
	shell.build_hamiltonian()
	shell.solve_interaction_matrix()
	print shell.eigen_values

if __name__ == '__main__':
	print """Questions:
* What is the triangle condition?
* What is meant by 'isobaric states'? 'Isobaric analogue state'
* Spectroscopic factor
* |||a^dagger_k||| notation means...?
	"""
	test1()