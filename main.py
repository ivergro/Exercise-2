import Magnet
import plotly.graph_objects as go
import numpy as np

def one_magnet():
    spin_vector = [0.3, 0.3, np.sqrt(1 - 0.3**2 - 0.3**2)]
    mag_position = [0, 0, 0]
    mag_list = [Magnet.Magnet(spin_vector, mag_position)]
    return mag_list

print(one_magnet()[0].vector)



