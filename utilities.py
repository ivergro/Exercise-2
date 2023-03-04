import numpy as np
import random as r
import scipy.constants as sp

#------Constants-------
J     = 0.00    #[eV]
d_z   = 0.003   #[eV] 
kB_T  = 0.000   #[eV]
uB_0  = 0.003   #[eV]
gamma = 1.6*10**11 #[Hz/T]
u     = 5.8*10**(-5) #[eV/T]
alpha = 0.0
temp  = kB_T/sp.k
#----------------------
#-------Vectors--------
B = np.array([0.0,0.0,0*uB_0/u]) #Dele på u?
e_z = np.array([0.0,0.0,1.0])
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


#Returns a random vector with numbers between -1 and 1
def gamma_vector(t):
    return np.random.normal(0, 1, 3)

def gaussian_thermal_noise(t, delta_t):
    return gamma_vector(t) * np.sqrt((2*alpha*kB_T*temp) / (gamma*u*delta_t))


#Prøver å gjøre om så funksjonene kjører over hele lista med atomer, og returner y_n, matrise over alle spins

#Help equation for LLG, returns a vector
def H_eff(y_n, j, t, delta_t, include_Zeeman_term = True):

    #--------Sums----------
    coupling = np.array([0.0, 0.0, 0.0])
    anisotropy = np.array([0.0, 0.0, 0.0])
    field = np.array([0.0, 0.0, 0.0])

    #Periodic BC and nearest neighbour interactions included
    if len(y_n) == 1:
        coupling = 0
    elif j == len(y_n):
      coupling += -J/2*(y_n[0] + y_n[j-1])
    elif j == 0:
        coupling += -J/2*(y_n[j+1] + y_n[-1])
    else:
        coupling += -J/2*(y_n[j+1] + y_n[j-1])

    anisotropy += -2*d_z*np.dot(y_n[j], e_z)*e_z

    if include_Zeeman_term:
        field += -uB_0*B
    
    return -1/gamma*(coupling + anisotropy + field) + gaussian_thermal_noise(t, delta_t)

    
#LLG, returns an array of derivated magnet vectors
def dt_sj(t, delta_t, y_n):
    f_t_n = np.empty((len(y_n), 3))
    for j in range(len(y_n)):
        H_eff_j = H_eff(y_n, j, t, delta_t)
        s_j     = y_n[j]
        f_t_n[j]  = -gamma/(1+alpha**2) * (np.cross(s_j,H_eff_j) + alpha*np.cross(s_j, (np.cross(s_j, H_eff_j))))
    return f_t_n

#y_0 = initial magnets (not spins but objects)
#y_n => array with all magnets
#timesteps = number of timesteps
#n and t is the same here

def Heun(y_0, t_0, t_n, delta_t = 1):
    y_n = y_0
    #Tegn første steg her
    #Funker kun for en magnet nå
    spin_values = np.empty((int((t_n - t_0)/delta_t) + 1, 3))
    spin_values[0] = y_0
    for n in range(t_0, t_n , delta_t):
        y_n = Heun_step(y_n, n, delta_t)

        #---normalisering---
        # for i in range(len(y_n)):
        # if np.linalg.norm(y_n) != 1:
        #     y_n = y_n/ np.linalg.norm(y_n)        
        #-------------------

        spin_values[int(n/delta_t) + 1] = y_n
        #tegn de nye posisjonene
    return spin_values


def Heun_step(y_n, t_n, delta_t):
    f_y_n = np.empty((len(y_n), 3))
    f_y_next = np.empty((len(y_n), 3))

    #Calculating f(t_n, y_n) to use in both y_p_next and y_next
    for j in range(len(y_n)):
        f_y_n[j] = dt_sj(t_n, delta_t, y_n)

    y_p_next = y_n + delta_t*f_y_n

    for j in range(len(y_n)):
        f_y_next[j] = dt_sj(t_n + delta_t, delta_t, y_p_next)
    
    return y_n + delta_t/2 * (f_y_n + f_y_next)



