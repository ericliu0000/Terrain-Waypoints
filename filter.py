import matplotlib.pyplot as plt
import numpy
import pandas

from rectangular_gradient import InterpolatedGridGradient


class SiteFilter:
    tol = 0.5
    left = 950310
    coords = {}

    def __init__(self, doc, values, show=False):
        data = pandas.read_hdf(doc, "a").to_numpy()
        xy, heights = data[..., :2], data[..., 2]

        for value in values:
            # copy and filter out height
            temp_heights = numpy.copy(heights)
            temp_heights[(temp_heights > value + self.tol) | (temp_heights < value - self.tol)] = numpy.nan
            coordinates = xy[~numpy.isnan(temp_heights)]
            
            self.coords[value] = numpy.array([]).reshape(0, 2)

            # only add those within boundaries
            for row in coordinates:
                x = row[0]
                if (x > self.left) and (self.lower(x) <= row[1] <= self.upper(x)):
                    self.coords[value] = numpy.append(self.coords[value], numpy.array([[row[0], row[1]]]), axis=0)

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

    def upper(self, coord):
        return min((6.7 * (coord - 950310) + 799640), 800310)

    def lower(self, coord):
        return max((-3.3077 * (coord - 950310) + 799400), 798970)


if __name__ == "__main__":
    test = SiteFilter("data/cloud_lasground.h5", [3360, 3400, 3460], True)
