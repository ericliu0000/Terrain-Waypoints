from rectangular_gradient import *
import numpy
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# elevation
elevations = PandasReader("data/ncsutest.h5").points
X, Y = elevations[..., 0].flatten(), elevations[..., 1].flatten()
Z = elevations[..., 2]

x_i = numpy.linspace(X.min(), X.max(), 1600)
y_i = numpy.linspace(Y.min(), Y.max(), 1600)

z_min = Z.min()
z_max = Z.max()

plt.subplot(1, 2, 1)
plt.contourf(x_i, y_i, Z, 160, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
plt.colorbar()

# gradient
calculator = NumpyGradient()
gradient = calculator.gradient
# gradient, points = calculator.gradient, calculator.spacing

# X, Y = points[..., 0].flatten(), points[..., 1].flatten()
z_min = -1
z_max = 1

Z = numpy.clip(gradient[0], z_min, z_max)
print(type(Z))

# x_i = numpy.linspace(X.min(), X.max(), 1600)
# y_i = numpy.linspace(Y.min(), Y.max(), 1600)

# print(gradient[0].max(), gradient[0].min())


plt.subplot(1, 2, 2)
plt.contourf(x_i, y_i, Z, 80, cmap=plt.cm.coolwarm, vmin=z_min, vmax=z_max)
plt.colorbar()


plt.show()
