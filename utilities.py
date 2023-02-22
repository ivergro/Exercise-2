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

#Hamiltonian for a 1D model and nearest neighbour interactions
def H(atom_spins):
    #-------Vectors--------
    B = np.array(0,0,*uB_0) #Dele på u?
    e_z = np.array(0,0,1)

    #--------Sums----------
    sum_coupling       = 0
    sum_anisotropy     = 0
    sum_external_field = 0

    for j in range(len(atom_spins)):
        sum_coupling += J*(np.dot(atom_spins[j],atom_spins[j - 1]) + np.dot(atom_spins[j], atom_spins[j + 1]))

        sum_anisotropy += d_z*np.dot(atom_spins[j], e_z)**2

        sum_external_field += uB_0*np.dot(atom_spins[j], B)

    

    return -sum_coupling-sum_anisotropy-sum_external_field

#Help equation for LLG
def H_eff(atom_list, j, include_Zeeman_term = True):
    #-------Vectors--------
    B = np.array(0,0,*uB_0/u) #Dele på u?
    e_z = np.array(0,0,1)

    #--------Sums----------
    coupling = np.array(0,0,0)
    anisotropy = np.array(0,0,0)
    field = np.array(0,0,0)

    for k in range(len(atom_list)):
        if k != j:
            coupling += atom_list[k]
    coupling *= -J

    anisotropy += -2*d_z*np.dot(atom_list[j], e_z)*e_z

    if include_Zeeman_term:
        field += -uB_0*B
    
    return coupling + anisotropy + field

    
#LLG
def dt_sj(atom_list, j):

    sj = atom_list[j]
    H_eff_j = H_eff(atom_list, j)
    return -gamma/(1+alpha**2) * (np.cross(sj,H_eff_j) + alpha*np.cross(sj, (np.cross(sj, H_eff_j))))

def gamma_vector():
    return -1 + (1 + 1)*r.random()

def gaussian_thermal_noise(delta_t):
    return gamma_vector() * np.sqrt((2*alpha*kB_T*temp) / (gamma*u))