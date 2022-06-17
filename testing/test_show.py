# from https://stackoverflow.com/a/39401259gi

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Load data from CSV
dat = np.genfromtxt('data/cloud_simplified.txt', delimiter=',', skip_header=1)
X_dat = dat[:, 0]
Y_dat = dat[:, 1]
Z_dat = dat[:, 2]
print(X_dat, Y_dat, Z_dat)

print("done 1")

# Convert from pandas dataframes to numpy arrays
X, Y, Z, = np.array([]), np.array([]), np.array([])
for i in range(len(X_dat)):
    X = np.append(X, X_dat[i])
    Y = np.append(Y, Y_dat[i])
    Z = np.append(Z, Z_dat[i])

print("done 2")

# create x-y points to be used in heatmap
xi = np.linspace(X.min(), X.max(), 1000)
yi = np.linspace(Y.min(), Y.max(), 1000)

print(Z.min(), Z.max())

print("done 3")

# Interpolate for plotting
zi = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method='linear')

print("done 4")

# I control the range of my colorbar by removing data
# outside of my range of interest
zmin = 3300
zmax = 3700
zi[(zi < zmin) | (zi > zmax)] = None
print(zi[1])


print("done 5")

# Create the contour plot
CS = plt.contourf(xi, yi, zi, 10, cmap=plt.cm.rainbow,
                  vmax=zmax, vmin=zmin)

print("done 6")
plt.colorbar()
plt.show()
