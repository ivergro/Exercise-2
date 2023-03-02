import Magnet
import utilities as u
import plotly.graph_objects as go
import numpy as np


def one_magnet():
    spin_vector = np.array([0.3, 0.3, np.sqrt(1 - 0.3**2 - 0.3**2)])
    mag_position = [0, 0, 0]
    mag_list = [Magnet.Magnet(spin_vector, mag_position)]
    return mag_list, spin_vector

#print(one_magnet()[0].vector)
mag_list, spin_list = one_magnet()


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
        

spin_values = u.Heun([spin_list], 0, 10000, 100)#10**(-7), 10**(-8))

f = open("vector_data.txt", "w")
for vector in spin_values:
    f.write(str(vector) + "\n")
f.close()

#draw_spins_one_mag(spin_values)

#animation.vector_plot(spin_values)