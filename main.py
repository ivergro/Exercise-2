import utilities as u
import plotly.graph_objects as go
import numpy as np


def one_magnet():
    spin_vector = np.array([0.3, 0.3, np.sqrt(1 - 0.3**2 - 0.3**2)])
    if  np.linalg.norm(spin_vector) != 1:
        spin_vector = spin_vector/np.linalg.norm(spin_vector)
    mag_list = np.array([spin_vector])
    return mag_list

def two_magnet():
    spin_vector = np.array([0.3, 0.3, np.sqrt(1 - 0.3**2 - 0.3**2)])
    spin_vector2 = np.array([0.2, -0.2, 0.8])
    if  np.linalg.norm(spin_vector) != 1:
        spin_vector = spin_vector/np.linalg.norm(spin_vector)
    if  np.linalg.norm(spin_vector2) != 1:
        spin_vector2 = spin_vector2/np.linalg.norm(spin_vector2)
    mag_list = np.array([spin_vector, spin_vector2])
    return mag_list


def draw_spins_one_mag(spin_values):
    X = []
    Y = []
    Z = []
    U = []
    V = []
    W = []
    for i in range(len(spin_values)):
        X.append(0 + i)
        Y.append(0)
        Z.append(0)
        U.append(spin_values[i][0])
        V.append(spin_values[i][1])
        W.append(spin_values[i][2]) 
    
    fig = go.Figure(data=go.Cone(x = X, y = Y, z = Z, u = U, v = V, w = W,
                                 sizemode="absolute", anchor="tail", sizeref=2))
    fig.show()
        


delta_t = 10*(-8)
timesteps = 1000
mag_list = one_magnet()
timestep = np.linspace(0, timesteps*delta_t, num=timesteps)
spin_values = u.Heun(mag_list, timestep)#10**(-7), 10**(-8))

f = open("vector_data.txt", "w")
for el in spin_values:
    for vector in el:
        f.write(str(vector) + " ")
    f.write("\n")
f.close()

#draw_spins_one_mag(spin_values)

#animation.vector_plot(spin_values)