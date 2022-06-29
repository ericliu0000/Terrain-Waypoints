import matplotlib.pyplot as plt
import numpy
import scipy.interpolate

from rectangular_gradient import InterpolatedGridGradient


# Only take restrictive set (rock face points only) for regression limits
def upper(coord):
    return min((6.0268 * (coord - 950288) + 799669), 800344)


def lower(coord):
    return max((-16.8125 * (coord - 950304) + 799400), (-3.6393 * (coord - 950304) + 799400), 798956)


def normal(x, y):
    # Return upward unit normal vector from dx, dy
    return ([-x, -y, 1] / numpy.linalg.norm([-x, -y, 1]))


class SiteFilter:
    """Extracts the coordinates of the site from a las file and constrains it to the site"""
    tol: float = 0.5
    left: float = 950310
    right: float = 950600
    buf: float = 30.48
    coords: dict = {}
    obj: InterpolatedGridGradient = InterpolatedGridGradient("data/cloud_lasground.h5")

    def __init__(self, doc: str, values: list, show: bool = False) -> None:
        xy, heights = self.obj.spacing, self.obj.values
        gradient = self.obj.gradient

        # get interpolated generators of partial derivatives
        # since gradient returns y, x, take the transform of each axis
        dx = scipy.interpolate.RectBivariateSpline(self.obj.x_grid, self.obj.y_grid, gradient[0].T)
        dy = scipy.interpolate.RectBivariateSpline(self.obj.x_grid, self.obj.y_grid, gradient[1].T)

        for value in values:
            # copy and filter out height
            temp_heights = numpy.copy(heights)
            temp_heights[(temp_heights > value + self.tol) | (temp_heights < value - self.tol)] = numpy.nan
            coordinates = numpy.hstack((xy[~numpy.isnan(temp_heights)], heights[~numpy.isnan(temp_heights), numpy.newaxis]))

            # x, y, z, unit
            self.coords[value] = numpy.array([]).reshape(0, 6)

            # only add those within boundaries
            for row in coordinates:
                x, y = row[0], row[1]
                if lower(x) <= y <= upper(x):
                    a, b = dx(x, y), dy(x, y)
                    norm = normal(dx(x, y)[0][0], dy(x, y)[0][0])
                    self.coords[value] = numpy.append(self.coords[value], numpy.atleast_2d(numpy.append(row, norm)), axis=0)

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
    test = SiteFilter("data/cloud_lasground.h5", [3500, 3600, 3700], False)
