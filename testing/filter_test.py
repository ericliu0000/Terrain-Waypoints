import numpy
import pandas
import scipy.interpolate
import matplotlib.pyplot as plt


def get_gradient():
    # read in the las processed data
    data = pandas.read_hdf("data/cloud_lasground.h5", "a").to_numpy()
    spacing, values = data[..., :2], data[..., 2]

    # get the x and y bounds and length
    x_max, x_min = spacing[:, 0].max(), spacing[:, 0].min()
    y_max, y_min = spacing[:, 1].max(), spacing[:, 1].min()
    x_length, y_length = x_max - x_min, y_max - y_min

    # create grid
    x_grid = numpy.linspace(x_min, x_max, int(x_length * 2))
    y_grid = numpy.linspace(y_min, y_max, int(y_length * 2))

    # interpolate
    points = scipy.interpolate.griddata(spacing, values, (x_grid[None, :], y_grid[:, None]), method="linear")

    gradient = numpy.gradient(points, x_grid[1] - x_grid[0], y_grid[1] - y_grid[0])
    magnitude = ((gradient[0] ** 2) + (gradient[1] ** 2)) ** 0.5

    return x_grid, y_grid, magnitude, points


def filter_slope(z_min, z_max):
    x, y, gradient, points = get_gradient()

    gradient[(gradient < z_min) | (gradient > z_max)] = numpy.nan

    plt.contourf(x, y, gradient, 50, cmap=plt.cm.Reds, vmin=0, vmax=2)
    plt.colorbar()

    plt.show()


def filter_layer(z_filter):
    x, y, gradient, z = get_gradient()
    tol = 1

    z[(z > z_filter + tol) | (z < z_filter - tol)] = numpy.nan

    plt.contourf(x, y, z, 1, cmap=plt.cm.Reds, vmin=3310, vmax=3707)
    plt.colorbar()

    plt.show()


if __name__ == "__main__":
    plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])

    # plt.imread("data/site.png")
    filter_layer(3600)
