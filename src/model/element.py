class Element:
    ID = []
    
    def __init__(self, id):
        self.ID = id

    def __str__(self) -> str:
        return str(f"id1={self.ID[0]} id2={self.ID[1]} id3={self.ID[2]} id4={self.ID[3]}")