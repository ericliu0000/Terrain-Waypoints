from reader import *
import scipy.interpolate
import numpy
import matplotlib.pyplot as plt

scale = 1

data = pandas.read_hdf("data/cloud_simplified.h5", "test").to_numpy()
points, values = data[:, :2], data[:, 2]

x_max, x_min = points[:, 0].max(), points[:, 0].min()
y_max, y_min = points[:, 1].max(), points[:, 1].min()
z_max, z_min = values.max(), values.min()

print(z_max, z_min)
print(z_max - z_min)

x_dim, y_dim = x_max - x_min, y_max - y_min

x_i = numpy.linspace(x_min, x_max, int(x_dim * scale))
y_i = numpy.linspace(y_min, y_max, int(y_dim * scale))

grid = scipy.interpolate.griddata(points, values, (x_i[None, :], y_i[:, None]), method="linear")

print(x_i.shape, y_i.shape, grid.shape)

plt.contourf(x_i, y_i, grid, 100, cmap=plt.cm.rainbow, vmax=z_max, vmin=z_min)

plt.show()