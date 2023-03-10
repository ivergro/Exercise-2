import utilities as u
import plotly.graph_objects as go
import numpy as np
import random as r


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

def multi_magnet(N):
    mag_list = []
    #generere tilfeldige tall på en bedre måte? Flere på en gang for eksempel
    for i in range(N):
        x = r.random()*2 - 1
        y = r.random()*2 - 1
        z = r.random()*2 - 1
        mag_list.append(np.array([x, y, z])/np.linalg.norm([x,y,z]))
    return mag_list
        


delta_t = 10*(-8)
timesteps = 1000
mag_list = multi_magnet(10)
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