from rectangular_gradient import InterpolatedGridGradient
import numpy
import matplotlib.pyplot as plt


def filter_slope(z_min, z_max):
    ground = InterpolatedGridGradient("data/cloud_lasground.h5")
    x, y = ground.x_grid, ground.y_grid

    gradient = ground.magnitude

    gradient[(gradient < z_min) | (gradient > z_max)] = numpy.nan

    plt.contourf(x, y, gradient, 50, cmap=plt.cm.Reds, vmin=0, vmax=2)
    plt.colorbar()

    plt.show()


def filter_layer(z_filter):
    ground = InterpolatedGridGradient("data/cloud_lasground.h5")
    x, y = ground.x_grid, ground.y_grid
    tol = 1

    z = ground.points

    z[(z > z_filter + tol) | (z < z_filter - tol)] = numpy.nan

    plt.contourf(x, y, z, 1, cmap=plt.cm.Reds, vmin=3310, vmax=3707)
    plt.colorbar()

    plt.show()


if __name__ == "__main__":
    plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])

    # plt.imread("data/site.png")
    filter_layer(3600)


