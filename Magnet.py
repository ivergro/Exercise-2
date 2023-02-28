import numpy as np

class Magnet:
    def __init__(self, vector, pos):
        if np.linalg.norm(vector) != 1:
            self.vector = np.array(vector)/np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)          #Magnet vector in 3D
        else:
            self.vector = np.array(vector)
        self.pos = np.array(pos)                  #Magnet position in 3D

    #Set each coordinate exclusively?
    #@setter
    #Normaliserer vektoren som settes
    def set_vector(self, vector):
        if np.linalg.norm(vector) != 1:
            self.vector = np.array(vector)/np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)          #Magnet vector in 3D
        else:
            self.vector = np.array(vector)
    
    def set_position(self, pos):
        self.pos = np.array(pos)