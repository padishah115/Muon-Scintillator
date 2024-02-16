import numpy as np

matrix = np.zeros((5,1))
matrix[1] = 1

matrix2 = np.array([0,0,0])

x = np.random.normal(3,1)

if any(matrix):
    print('yes')
else:
    print('no')

#print(matrix)