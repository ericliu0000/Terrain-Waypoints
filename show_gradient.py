from rectangular_gradient import *
import numpy
import matplotlib.pyplot as plt


def ncsu_test():
    # elevations
    obj = NumpyGradient("data/ncsutest.h5")
    elevations = obj.points
    x, y = elevations[..., 0].flatten(), elevations[..., 1].flatten()
    z = elevations[..., 2]

    x_i = numpy.linspace(x.min(), x.max(), 1600)
    y_i = numpy.linspace(y.min(), y.max(), 1600)

    z_min = z.min()
    z_max = z.max()

    plt.subplot(1, 2, 1)
    plt.contourf(x_i, y_i, z, 160, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
    plt.colorbar()

    # gradient
    gradient = obj.magnitude

    z_min = -1
    z_max = 1

    z = numpy.clip(gradient, z_min, z_max)

    plt.subplot(1, 2, 2)
    plt.contourf(x_i, y_i, z, 80, cmap=plt.cm.coolwarm, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.show()


def site_test():
    # elevations
    obj = InterpolatedGridGradient("data/cloud_lasground.h5")
    x, y = obj.x_grid, obj.y_grid
    z = obj.points

    z2 = z[~numpy.isnan(z)]

    # z_min = z2.min()
    z_min = 3375
    z_max = z2.max()

    plt.subplot(1, 2, 1)
    plt.title("Elevation")

    plt.contourf(x, y, z, 20, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
    plt.colorbar()

    # gradient
    gradient = obj.magnitude

    z_min = 0
    z_max = 2

    z = numpy.clip(gradient, z_min, z_max)

    plt.subplot(1, 2, 2)
    plt.title("Slope")

    plt.contourf(x, y, z, 20, cmap=plt.cm.Reds, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.show()


def lasground_test():
    # normal
    obj = InterpolatedGridGradient("data/cloud_simplified_2.h5")
    x, y = obj.x_grid, obj.y_grid
    gradient = obj.magnitude

    z_min = 0
    z_max = 5

    z = numpy.clip(gradient, z_min, z_max)

    plt.subplot(1, 2, 1)
    plt.title("Original data")

    plt.contourf(x, y, z, 20, cmap=plt.cm.Reds, vmin=z_min, vmax=z_max)
    plt.colorbar()

    # lasground
    obj = InterpolatedGridGradient("data/cloud_lasground.h5")
    x, y = obj.x_grid, obj.y_grid
    gradient = obj.magnitude

    print(numpy.nan_to_num(gradient, nan=0).max())
    z = numpy.clip(gradient, z_min, z_max)

    plt.subplot(1, 2, 2)
    plt.title("Surface objects removed")

    plt.contourf(x, y, z, 20, cmap=plt.cm.Reds, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.show()


def site_slope_only():
    obj = InterpolatedGridGradient("data/cloud_lasground.h5")
    x, y = obj.x_grid, obj.y_grid
    gradient = obj.magnitude

    z_min = 0
    z_max = 2

    z = numpy.clip(gradient, z_min, z_max)

    plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])

    plt.contourf(x, y, z, 50, cmap=plt.cm.Reds, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.show()


def quadrant():
    elevation_steps = 40
    slope_steps = 40

    # elevations
    original = InterpolatedGridGradient("data/cloud_simplified_2.h5")
    x1, y1 = original.x_grid, original.y_grid
    z1 = original.points

    ground = InterpolatedGridGradient("data/cloud_lasground.h5")
    x2, y2 = ground.x_grid, ground.y_grid
    z2 = ground.points

    z_min = 3350
    z_max = 3720

    plt.subplot(2, 2, 1)
    plt.title("Original elevation")

    plt.contourf(x1, y1, z1, elevation_steps, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.subplot(2, 2, 3)
    plt.title("LASground elevation")

    plt.contourf(x2, y2, z2, elevation_steps, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
    plt.colorbar()

    # gradient
    z_min = 0
    z_max = 2

    z1 = numpy.clip(original.magnitude, z_min, z_max)
    z2 = numpy.clip(ground.magnitude, z_min, z_max)

    plt.subplot(2, 2, 2)
    plt.title("Original slope")

    plt.contourf(x1, y1, z1, slope_steps, cmap=plt.cm.Reds, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.subplot(2, 2, 4)
    plt.title("LASground slope")

    plt.contourf(x2, y2, z2, slope_steps, cmap=plt.cm.Reds, vmin=z_min, vmax=z_max)
    plt.colorbar()

    plt.show()


if __name__ == "__main__":
    # ncsu_test()
    # site_test()
    lasground_test()
    # site_slope_only()
    # quadrant()
