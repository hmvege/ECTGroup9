import numpy as np, itertools

class SingleParticleState:
	"""
	Class for a single particle state. Stores usefull quantum numbers, can easily be extended.
	"""
	def __init__(self, state_index, n, l, j, m, sp_energy = None):
		self.state_index = state_index - 1 # Minus one in order to bring it to Python list syntax
		self.n = int(n)
		self.l = l
		self.j = j
		self.m = m
		self.sp_energy = sp_energy

	def __str__(self):
		s = "State index = %2d, n = %2d, l = %4.1f, j = %4.1f, m = %4.1f" % (self.state_index, self.n, self.l, self.j, self.m)
		if self.sp_energy:
			s += ", energy = %4.1f" % self.sp_energy
		return s

class Hamiltonian:
	"""
	Class for making general Hamiltonian operators. NOT IMPLEMENTED YET
	"""
	def __init__(self):
		self.slater_determinants = None
		self.pair_list = None

	def __call__(self, states):
		raise NotImplementedError("Base Hamiltonian class not functioning. Create subclass with inheritance.")

	def check_pairing(self,sd):
		"""
		Takes a possible slater determinant, sd.
		Used for checking other possible pairing criterias.
		"""
		return True

	def setup_msg(self):
		"""
		Returns other possible setup-criterias
		"""
		return ""

	def set_sd_list(self, sd_list, N_sd_list):
		self.slater_determinants = sd_list
		self.N_sd_list = N_sd_list

	def set_pair_list(self, pair_list):
		self.pair_list = pair_list

	def pair_annihilation(self,annihilation_states,creation_states,beta_state):
		"""
		Apply annihilation operators one a set of states.
		"""
		for pair in self.pair_list:
			if len(pair & beta_state) == 2: # If two elements coincide, we can destroy a pair of particles
				annihilation_states.append(beta_state ^ pair) # Appends only if pair does not exist in beta_state_indexes
		return annihilation_states

	def pair_creation(self,annihilation_states,creation_states,beta_state):
		"""
		Apply creation operators.
		"""
		for pair in self.pair_list:
			for state in annihilation_states:
				if len(pair & state) == 0: # If no elements coincide, we can create a pair of particles
					creation_states.append(state ^ pair)
		return creation_states

	def annihilate_state(self, start_states, state):
		raise NotImplementedError("State annihilation not implemented.")

	def create_state(self, start_states, state):
		raise NotImplementedError("State creation not implemented.")

class BasicHamiltonian(Hamiltonian):
	def __init__(self, G):
		Hamiltonian.__init__(self)
		self.G = G

	def __call__(self,alpha,beta):
		alpha_state = self.slater_determinants[alpha]
		beta_state = self.slater_determinants[beta]
		beta_state_indexes = set(state.state_index for state in beta_state) # Puts state indexes into a set to perform bitwise operations on
		alpha_state_indexes = set(state.state_index for state in alpha_state) 
		annihilation_states = []
		creation_states = []
		# Apply operatores
		annihilation_states = self.pair_annihilation(annihilation_states,creation_states,beta_state_indexes)
		creation_states = self.pair_creation(annihilation_states,creation_states,beta_state_indexes)
		return sum([self.G for state in creation_states if state == alpha_state_indexes])

class PairingHamiltonian(Hamiltonian):
	def __init__(self, G):
		Hamiltonian.__init__(self)
		self.G = G

	def __call__(self, alpha, beta):
		sp_e = self._sp_energy(alpha,beta)
		pot = self._potential(alpha,beta)
		# print "pot = ", pot
		# raise NotImplementedError("Not implemented pairing hamiltonian!!")
		return sp_e
		# return self._sp_energy(alpha,beta) + self._potential(alpha,beta)

	def _sp_energy(self, alpha, beta):
		# N OPERATOR IS DIFFERENT THAN JUST THE LENGTH
		val = 0
		for n in self.n_list:
			for state in self.n_list[n]:
				val += state.sp_energy
			val *= n*len(self.n_list[n]) # Might need to do n=n+1?
		return val

	def _potential(self, alpha, beta):
		# POTENTIAN DIFFERENT FROM BASIC HAMILTONIAN! LOOPS OVER N AND SPIN
		alpha_state = self.slater_determinants[alpha]
		beta_state = self.slater_determinants[beta]
		beta_state_indexes = set(state.state_index for state in beta_state) # Puts state indexes into a set to perform bitwise operations on
		alpha_state_indexes = set(state.state_index for state in alpha_state) 
		annihilation_states = []
		creation_states = []
		# Apply operatores
		annihilation_states = self.pair_annihilation(annihilation_states,creation_states,beta_state_indexes)
		creation_states = self.pair_creation(annihilation_states,creation_states,beta_state_indexes)
		return sum([self.G for state in creation_states if state == alpha_state_indexes])

	def set_sd_list(self, sd_list, N_sd_list):
		self.slater_determinants = sd_list
		self.N_sd_list = N_sd_list
		self.n_list = {}
		for sd in self.slater_determinants: # Building a dictionary of all n-states
			for state in sd:
				if not state.n in self.n_list:
					self.n_list[state.n] = []
		for sd in self.slater_determinants: # Populating the dictonary with corresponding n-states
			for state in sd:
				if state not in self.n_list[state.n]:
					self.n_list[state.n].append(state)

	def setup_msg(self):
		"""
		Returns other possible setup-criterias
		"""
		return " and for pairs with equal n"

	def check_pairing(self, sd):
		# possible_pairs = np.asarray(list(itertools.combinations(sd, 2)))
		# GOAL: return only possible pairs
		count = 0
		for i in range(0,len(sd),2):
			if sd[i].n == sd[i+1].n:
				count += 1
		if count == len(sd)/2:
			return True
		else:
			return False

class XShell:
	def __init__(self, input_file, hamiltonian, verbose = False):
		"""
		Arguments:
		input_file - file containing quantum numbers (Index, n, l, 2j, 2m)
		(optional) verbose - prints more info
		"""
		data_input = np.loadtxt(input_file, skiprows=1) # Assuming form of index,n,l,j,m_j,energy
		self.index_input = map(int,data_input[:,0])
		self.n_input = data_input[:,1]
		self.l_input = data_input[:,2]
		self.j_input = map(lambda x: 0.5*x, data_input[:,3])
		self.m_input = map(lambda x: 0.5*x, data_input[:,4])
		self.N_sp_states = len(self.n_input) # number of single particle states states
		if data_input.shape[1] > 5:
			self.sp_energy = map(float,data_input[:,5])
		else:
			self.sp_energy = np.ones(data_input.shape[0])
		self.states = [SingleParticleState(state_index,n,l,j,m,sp_energy) for state_index,n,l,j,m,sp_energy in zip(self.index_input, self.n_input,self.l_input,self.j_input,self.m_input,self.sp_energy)]
		print "Data from file %s loaded." % input_file
		# Sets verbose to false is desired
		self.verbose = verbose
		# Default Hamiltonian is None, has to be set manually
		self.hamiltonian = hamiltonian

	def generate_slater_determinants(self, N_particles):
		"""
		Arguments:
		N_particles - number of particles to calculate for
		Generates all the possible N particle Slater determinants to be used from our basis.
		"""
		self.SD_list = np.asarray(list(itertools.combinations(self.states, N_particles))) # Generating Slater determinants based on indexes
		self.N_particles = N_particles

		if self.N_particles > self.N_sp_states:
			raise ValueError("%s particles cannot populate %s single particle states" % (N_particles, self.N_sp_states))
		
		if self.verbose:
			print "There are ", len(self.SD_list), "Slater Determinants in a space with ", self.N_sp_states, "sp states and with ", N_particles, "particles"
		
		# Unit test for the number of Slater determinants
		self.N_SD_list = int(np.math.factorial(self.N_sp_states))/(int(np.math.factorial(N_particles))*int(np.math.factorial(self.N_sp_states - N_particles)))

		if self.N_SD_list != len(self.SD_list):
			raise ValueError("Predicted number of Slater determinants not corresponding with those retrieved.")

	def m_scheme_setup(self, M_fixed):
		"""
		Takes a M, and truncates our system based on this value
		"""
		SD_updated = []
		for slater_det in self.SD_list:
			if sum([state.m for state in slater_det]) == M_fixed:
				if self.hamiltonian.check_pairing(slater_det):
					SD_updated.append(slater_det)
		self.SD_updated = np.asarray(SD_updated) # Updated states that have good M
		self.N_slater_determinants = len(self.SD_updated)
		self.hamiltonian.set_sd_list(self.SD_updated,self.N_slater_determinants)
		self._build_pair_list()
		self.M_fixed = M_fixed
		if self.verbose:
			msg = "There are %d Slater Determinants with total M: %g" % (self.N_slater_determinants, M_fixed)
			print msg + self.hamiltonian.setup_msg()

	def _build_pair_list(self):
		# Builds pair list
		self.pair_list = [set([i,j]) for i,j in zip(range(0,self.N_sp_states-1,2),range(1,self.N_sp_states,2))]
		self.hamiltonian.set_pair_list(self.pair_list)
		# print self.pair_list

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
		if not self.hamiltonian: raise AttributeError("Hamiltonian not set.")
		states = self.SD_updated
		H_matrix = np.zeros((self.N_slater_determinants,self.N_slater_determinants))
		# Loops over interaction matrix
		# self.hamiltonian.internal()

		for alpha in xrange(self.N_slater_determinants):
			H_matrix[alpha,alpha] = self.hamiltonian(alpha,alpha)
			# H_matrix[alpha,alpha] = self.apply_hamiltonian(alpha,alpha)
			for beta in xrange(alpha+1, self.N_slater_determinants):
				H_matrix[alpha,beta] = self.hamiltonian(alpha,beta)
				# H_matrix[alpha,beta] = self.apply_hamiltonian(alpha,beta)
				H_matrix[beta,alpha] = H_matrix[alpha,beta]
		print H_matrix
		self.H_matrix = H_matrix

	def solve_interaction_matrix(self):
		"""
		Uses numpy to solve the interaction matrix
		"""
		self.eigen_values, self.eigen_vectors = np.linalg.eigh(self.H_matrix)
		return self.eigen_values, self.eigen_vectors

	# def apply_hamiltonian(self, alpha, beta):
	# 	"""
	# 	WILL BE MOVED INTO A GENERAL CLASS STRUCTURE W/POLYMORPHISM LATER ON
	# 	"""
	# 	G = -1
	# 	alpha_state = self.SD_updated[alpha]
	# 	beta_state = self.SD_updated[beta]
	# 	beta_state_indexes = set(state.state_index for state in beta_state) # Puts state indexes into a set to perform bitwise operations on
	# 	alpha_state_indexes = set(state.state_index for state in alpha_state) 
	# 	annihilation_states = []
	# 	creation_states = []

	# 	# Apply annihilation operators
	# 	for pair in self.pair_list:
	# 		if len(pair & beta_state_indexes) == 2: # If two elements coincide, we can destroy a pair of particles
	# 			annihilation_states.append(beta_state_indexes ^ pair) # Appends only if pair does not exist in beta_state_indexes
	# 	# Apply creation operators
	# 	for pair in self.pair_list:
	# 		for state in annihilation_states:
	# 			if len(pair & state) == 0: # If no elements coincide, we can create a pair of particles
	# 				creation_states.append(state ^ pair)

	# 	return sum([G for state in creation_states if state == alpha_state_indexes])

def test1():
	N_part = 3
	M_value = 0.5
	G = - 1
	input_file = "inputsp2.txt"
	H = BasicHamiltonian(G)
	shell = XShell(input_file, H, True)
	shell.generate_slater_determinants(N_part)
	shell.m_scheme_setup(M_value)
	shell.build_hamiltonian()
	shell.solve_interaction_matrix()

def test2():
	N_part = 4
	M_value = 0
	G = -1
	input_file = "inputsp3.txt"
	H = PairingHamiltonian(G)
	shell = XShell(input_file, H, True)
	shell.generate_slater_determinants(N_part)
	shell.m_scheme_setup(M_value)
	shell.build_hamiltonian()
	# shell.solve_interaction_matrix()

# def test3():
# 	N_part = 4
# 	M_value = 0
# 	G = -1
# 	input_file = "usdbint.txt"
# 	H = PairingHamiltonian(G)
# 	shell = XShell(input_file, H, True)
# 	shell.generate_slater_determinants(N_part)
# 	shell.m_scheme_setup(M_value)
# 	shell.build_hamiltonian()
# 	# shell.solve_interaction_matrix()

if __name__ == '__main__':
	print """Questions:
* What is the triangle condition?
* What is meant by 'isobaric states'? 'Isobaric analogue state'
* Spectroscopic factor
* |||a^dagger_k||| notation means...?
	"""
	# test1()
	test2()
	# test3()