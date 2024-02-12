import numpy as np

x = [1,2,3,4]
y = [1,4,9,16]

y_fit = np.polyfit(x, y, 2)

print(y_fit)