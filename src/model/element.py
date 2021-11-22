class Element: 
    def __init__(self, id):
        size = 4
        self.ID = id
        self.H = [[0 for x in range(size)] for y in range(size)] 
        self.H_bc = [[0 for x in range(size)] for y in range(size)]

    def set_H(self, H):
        self.H = H

    def __str__(self) -> str:
        return str(f"id1={self.ID[0]} id2={self.ID[1]} id3={self.ID[2]} id4={self.ID[3]}")