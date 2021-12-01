import numpy as np
class Element: 
    def __init__(self, id):
        self.ID = id
        self.H =  np.zeros((4, 4))
        self.H_bc = np.zeros((4, 4))

    def set_H(self, H):
        self.H = H

    def set_Hbc(self, Hbc):
        self.H_bc = Hbc

    def __str__(self) -> str:
        return str(f"id1={self.ID[0]} id2={self.ID[1]} id3={self.ID[2]} id4={self.ID[3]}")