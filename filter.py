import matplotlib.pyplot as plt
import numpy
import scipy.interpolate

from rectangular_gradient import InterpolatedGridGradient


# Only take restrictive set (rock face points only) for regression limits
def upper(coord):
    return min((6.0268 * (coord - 950288) + 799669), 800344)


def lower(coord):
    return max((-16.8125 * (coord - 950304) + 799400), (-3.6393 * (coord - 950304) + 799400), 798956)


class SiteFilter:
    """Extracts the coordinates of the site from a las file and constrains it to the site"""
    tol: float = 0.5
    left: float = 950310
    right: float = 950600
    buf: float = 30.48
    coords: dict = {}
    obj: InterpolatedGridGradient = InterpolatedGridGradient("data/cloud_lasground.h5")

    def __init__(self, doc: str, values: list, show: bool = False) -> None:
        # data = self.grad.points
        xy, heights = self.obj.spacing, self.obj.values
        gradient = numpy.nan_to_num(self.obj.gradient)
        print(self.obj.magnitude[1000][1000])
        print(self.obj.x_grid[1000], self.obj.y_grid[1000])

        # Get interpolated generators of partial derivatives
        # Since gradient returns y, x, take the transform of each axis
        dx = scipy.interpolate.RectBivariateSpline(self.obj.x_grid, self.obj.y_grid, gradient[0].T)
        dy = scipy.interpolate.RectBivariateSpline(self.obj.x_grid, self.obj.y_grid, gradient[1].T)

        # root mean square of dx and dy at 1000, 1000
        print(dx.ev(1000, 1000))
        print(dy.ev(1000, 1000))
        print(numpy.sqrt(dx.ev(1000, 1000) ** 2 + dy.ev(1000, 1000) ** 2))

        for value in values:
            # copy and filter out height
            temp_heights = numpy.copy(heights)
            temp_heights[(temp_heights > value + self.tol) | (temp_heights < value - self.tol)] = numpy.nan
            coordinates = numpy.hstack((xy[~numpy.isnan(temp_heights)], heights[~numpy.isnan(temp_heights), numpy.newaxis]))

            self.coords[value] = numpy.array([]).reshape(0, 3)

            # only add those within boundaries
            for row in coordinates:
                x = row[0]
                if lower(x) <= row[1] <= upper(x):
                    self.coords[value] = numpy.append(self.coords[value], numpy.atleast_2d(row), axis=0)

        # display the filtered coordinates
        if show:
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
    test = SiteFilter("data/cloud_lasground.h5", [3500, 3600, 3700], True)
