from rectangular_gradient import *
import numpy
import matplotlib.pyplot as plt

ground = InterpolatedGridGradient("data/cloud_lasground.h5")
x, y = ground.x_grid, ground.y_grid

z_min = 0.9
z_max = 1.5
inv_val = -9999

gradient = ground.magnitude

gradient[(gradient < z_min) | (gradient > z_max)] = numpy.nan
print(gradient.min(), gradient.max())

# gradient = numpy.clip(gradient, z_min, z_max)

plt.contourf(x, y, gradient, 50, cmap=plt.cm.Reds, vmin=0, vmax=2)
plt.colorbar()

plt.show()
