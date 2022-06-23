from rectangular_gradient import InterpolatedGridGradient
import numpy
import pandas
import matplotlib.pyplot as plt
import time

class ElevationFilter:
    tol = 0.5

    def __init__(self, doc, value):
        start = time.time_ns()

        data = pandas.read_hdf(doc, "a").to_numpy()
        
        print((time.time_ns() - start) / 10 ** 9)

        spacing, values = data[..., :2], data[..., 2]

        x_max, x_min = spacing[:, 0].max(), spacing[:, 0].min()
        y_max, y_min = spacing[:, 1].max(), spacing[:, 1].min()
        x_length, y_length = x_max - x_min, y_max - y_min

        values[(values > value + self.tol) | (values < value - self.tol)] = numpy.nan
        spacing = spacing[~numpy.isnan(values)]
        values = values[~numpy.isnan(values)]

        ### testing

        # create grid
        x_grid = numpy.linspace(x_min, x_max, int(x_length))
        y_grid = numpy.linspace(y_min, y_max, int(y_length))

        plt.axis([x_min, x_max, y_min, y_max])
        plt.plot(spacing[:, 0], spacing[:, 1], "ro")

        obj = InterpolatedGridGradient("data/cloud_lasground.h5")
        x, y = obj.x_grid, obj.y_grid
        z = obj.points

        z2 = z[~numpy.isnan(z)]

        z_min = z2.min()
        z_max = z2.max()

        plt.contourf(x, y, z, 20, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
        plt.colorbar()

        plt.show()


print((time.time_ns() - start) / 10 ** 9)

if __name__ == "__main__":
    filter = ElevationFilter("data/cloud_lasground.h5", 3360)
