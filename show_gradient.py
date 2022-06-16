from rectangular_gradient import *
import numpy
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


def NCSUTest():
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
    gradient = calculator.magnitude

    z_min = -1
    z_max = 1

    Z = numpy.clip(gradient, z_min, z_max)

    plt.subplot(1, 2, 2)
    plt.contourf(x_i, y_i, Z, 80, cmap=plt.cm.coolwarm, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.show()

def siteTest():
    # elevations
    obj = InterpolatedGridGradient("data/cloud_simplified.h5")
    X, Y = obj.x_grid, obj.y_grid
    Z = obj.points

    z2 = Z[~numpy.isnan(Z)]

    z_min = z2.min()
    z_max = z2.max()

    plt.subplot(1, 2, 1)
    plt.contourf(X, Y, Z, 40, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
    plt.colorbar()

    # gradient
    gradient = obj.magnitude

    z_min = -1
    z_max = 1

    Z = numpy.clip(gradient, z_min, z_max)

    plt.subplot(1, 2, 2)
    plt.contourf(X, Y, Z, 40, cmap=plt.cm.coolwarm, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.show()


    # TODO complete this. do the same as the above function but just adapt the points to the interpolated ones instead


if __name__ == "__main__":
    siteTest()