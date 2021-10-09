
class Node: 
  x = 0
  y = 0
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self) -> str:
      return str("x={:.3f} y={:.3f}".format(self.x, self.y))

  def printNode(self):
    print(f'x={self.x} y={self.y}')
