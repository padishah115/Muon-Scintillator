import numpy as np

matrix = np.zeros((2,5,5))

position = np.array([1,2,3])

print(np.max(position))

for i, num in enumerate(position):
    print(f'{i} {num}')