import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#For 5x5 array
dimension = 5
height = 1
colors = ['black', 'dimgray']

for i in range(dimension):
    for j in range(dimension):
        #color_index = (i+j) % 2
        color_index = 0
        ax.bar3d(0, i, j, 1, 1, 1, color=colors[color_index], edgecolor='w')

ax.set_zlabel('Height above ground')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.title('3D Rendering of Scintillator Array')
plt.savefig('3d_photo')
plt.show()