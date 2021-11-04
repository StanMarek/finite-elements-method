import math

twoPointKeys = [(-1/math.sqrt(3)), (1/math.sqrt(3))]
threePointKeys = [(-math.sqrt(3/5)), (0), (math.sqrt(3/5))]

twoPointValues = [1, 1]
threePointValues = [(5/9), (8/9), (5/9)]

def fun_x(x): 
  return 5*x**2+3*x+6

def fun_xy(x, y):
  return 5*x**2*y**2+3*x*y+6


def gauss_1dim(points):
  if points == 2:
    outcome = twoPointValues[0]*fun_x(twoPointKeys[0]) + twoPointValues[1]*fun_x(twoPointKeys[1]) 
    return outcome

  elif points == 3:
    outcome = threePointValues[0]*fun_x(threePointKeys[0]) + threePointValues[1]*fun_x(threePointKeys[1]) + threePointValues[2]*fun_x(threePointKeys[2])
    return outcome

  else:
    print('Wrong points input')
    return -math.inf

def gauss_2dim(points):
  if points == 2: #4
    outcome = 0
    for y in range(points):
      for x in range(points):
        outcome += twoPointValues[x] * twoPointValues[y] * fun_xy(x = twoPointKeys[x], y = twoPointKeys[y])
    return outcome  

  elif points == 3: #9
    outcome = 0
    for y in range(points):
      for x in range(points):
        outcome += threePointValues[x] * threePointValues[y] * fun_xy(x = threePointKeys[x], y = threePointKeys[y])
    return outcome
    
  else:
    print('Wrong points input')
    return -math.inf