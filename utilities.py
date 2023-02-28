import numpy as np
import random as r
import scipy.constants as sp

#------Constants-------
J     = 0.01    #[eV]
d_z   = 0.003   #[eV] 
kB_T  = 0.001   #[eV]
uB_0  = 0.003   #[eV]
gamma = 1.6*10**11 #[Hz/T]
u     = 5.8*10**(-5) #[eV/T]
alpha = 0.0
temp  = kB_T/sp.k
#----------------------
#-------Vectors--------
B = np.array(0,0,*uB_0) #Dele på u?
e_z = np.array(0,0,1)
#----------------------


#Hamiltonian for a 1D model and nearest neighbour interactions
def H(atom_spins):
    #--------Sums----------
    sum_coupling       = 0
    sum_anisotropy     = 0
    sum_external_field = 0

    for j in range(len(atom_spins)):
        sum_coupling += J*(np.dot(atom_spins[j],atom_spins[j - 1]) + np.dot(atom_spins[j], atom_spins[j + 1]))

        sum_anisotropy += d_z*np.dot(atom_spins[j], e_z)**2

        sum_external_field += uB_0*np.dot(atom_spins[j], B)

    return -sum_coupling-sum_anisotropy-sum_external_field

#Help equation for LLG, returns a vector
def H_eff(atom_list, j, t, delta_t, include_Zeeman_term = True):

    #--------Sums----------
    coupling = np.array(0,0,0)
    anisotropy = np.array(0,0,0)
    field = np.array(0,0,0)

    #Periodic BC and nearest neighbour interactions included
    if j == len(atom_list):
      coupling += -J/2(atom_list[0].vector + atom_list[j-1].vector)
    elif j == 0:
        coupling += -J/2(atom_list[j+1].vector + atom_list[-1].vector)
    else:
        coupling += -J/2(atom_list[j+1].vector + atom_list[j-1].vector)

    anisotropy += -2*d_z*np.dot(atom_list[j].vector, e_z)*e_z

    if include_Zeeman_term:
        field += -uB_0*B
    
    return -1/gamma*(coupling + anisotropy + field) + gaussian_thermal_noise(t, delta_t)

    
#LLG, returns a vector
def dt_sj(atom_list, s_j, j, t, delta_t):
    H_eff_j = H_eff(atom_list, j, t, delta_t)
    return -gamma/(1+alpha**2) * (np.cross(s_j,H_eff_j) + alpha*np.cross(s_j, (np.cross(s_j, H_eff_j))))

#Returns a random vector with numbers between -1 and 1
def gamma_vector(t):
    return np.random.normal(0, 1, 3)

def gaussian_thermal_noise(t, delta_t):
    return gamma_vector(t) * np.sqrt((2*alpha*kB_T*temp) / (gamma*u*delta_t))


def Heun(S_j0, timesteps, magnet_list):
    S = np.zeros(len(magnet_list))
    delta_t = (timesteps[-1] - timesteps[0])/len(timesteps)
    for j in range(magnet_list):
        S_j = np.zeros(timesteps) #vektor array?
        S_j[0] = S_j0  #Første S verdi for en magnet?
        for n in range(timesteps - 1):
            #Ikke sende inn indekseringa, men den nåværende spin verdien til magnet j
            dt_Sj = dt_sj(magnet_list, j, timesteps[n], delta_t)
            S_jn = S_j[n]
            S_j[n+1] = S_jn + delta_t/2*(dt_Sj   + dt_sj(magnet_list, j +1, timesteps[n+1], ))    

        S[j].append(S_j) #Lager den en grei 2D matrise?