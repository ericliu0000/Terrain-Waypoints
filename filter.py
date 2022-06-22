from rectangular_gradient import *
import numpy
import pandas

import matplotlib.pyplot as plt


class ElevationFilter:
    tol = 1

    # def __init__(self, value):
    #     coords = []
    #     grid = InterpolatedGridGradient("data/cloud_lasground.h5", gradient=False)

    #     print(grid.spacing)
    #     x, y = grid.spacing[:, 0], grid.spacing[:, 1]
    #     z = grid.values

    #     # If z is within tolerance, add xy values to list
    #     z[(z < value - self.tolerance) | (z > value + self.tolerance)] = numpy.nan

    #     print(z)
    #     # Iterate through every value of z. If it is not nan, add xy values to coords
    #     for i in range(len(z)):
    #         if not numpy.isnan(z[i][j]):
    #             coords.append((x[i][j], y[i][j]))

    #     print(coords)
    def __init__(self, doc, value):
        data = pandas.read_hdf(doc, "a").to_numpy()
        spacing, values = data[..., :2], data[..., 2]

        x_max, x_min = spacing[:, 0].max(), spacing[:, 0].min()
        y_max, y_min = spacing[:, 1].max(), spacing[:, 1].min()
        x_length, y_length = x_max - x_min, y_max - y_min

        # create grid
        x_grid = numpy.linspace(x_min, x_max, int(x_length))
        y_grid = numpy.linspace(y_min, y_max, int(y_length))

        values[(values > value + self.tol) | (values < value - self.tol)] = numpy.nan
        spacing = spacing[~numpy.isnan(values)]
        values = values[~numpy.isnan(values)]


        ### testing
        # print(spacing)
        print(spacing.shape)
        # print(values)
        print(values.shape)

        # after removal, interpolate points
        points = scipy.interpolate.griddata(spacing, values, (x_grid[None, :], y_grid[:, None]), method="linear")

        plt.axis([x_min, x_max, y_min, y_max])
        plt.plot(spacing[:, 0], spacing[:, 1], "ro")

        # very testing
        obj = InterpolatedGridGradient("data/cloud_lasground.h5")
        x, y = obj.x_grid, obj.y_grid
        z = obj.points

        z2 = z[~numpy.isnan(z)]

        # z_min = z2.min()
        z_min = 3375
        z_max = z2.max()

        plt.contourf(x, y, z, 20, cmap=plt.cm.terrain, vmin=z_min, vmax=z_max)
        plt.colorbar()

        plt.show()



if __name__ == "__main__":
    filter = ElevationFilter("data/cloud_lasground.h5", 3400)
