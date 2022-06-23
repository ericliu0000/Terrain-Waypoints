import matplotlib.pyplot as plt
import numpy
import pandas

from rectangular_gradient import InterpolatedGridGradient


class ElevationFilter:
    tol = 0.5
    coords = {}

    def __init__(self, doc, values, show=False):
        data = pandas.read_hdf(doc, "a").to_numpy()
        xy, heights = data[..., :2], data[..., 2]

        for value in values:
            temp_heights = numpy.copy(heights)
            temp_heights[(temp_heights > value + self.tol) | (temp_heights < value - self.tol)] = numpy.nan
            self.coords[value] = xy[~numpy.isnan(temp_heights)]

        if show:
            # testing
            x_max, x_min = xy[:, 0].max(), xy[:, 0].min()
            y_max, y_min = xy[:, 1].max(), xy[:, 1].min()

            plt.axis([x_min, x_max, y_min, y_max])

            for value in self.coords.values():
                plt.plot(value[:, 0], value[:, 1], "ro")

            obj = InterpolatedGridGradient("data/cloud_lasground.h5")
            x, y = obj.x_grid, obj.y_grid
            z = obj.points

            z2 = z[~numpy.isnan(z)]

            z_min = z2.min()
            z_max = z2.max()

            plt.contourf(x, y, z, 20, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
            plt.colorbar()

            plt.show()


if __name__ == "__main__":
    test = ElevationFilter("data/cloud_lasground.h5", [3360, 3400, 3460])
