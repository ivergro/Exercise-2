import numpy as np

class Magnet:
    def __init__(self, vector, pos):
        self.vector = np.array(vector)            #Magnet vector in 3D
        self.pos = np.array(pos)                  #Magnet position in 3D

    #Set each coordinate exclusively?
    #@setter
    def set_vector(self, vector):
        self.vector = np.array(vector)
    
    def set_position(self, pos):
        self.pos = np.array(pos)