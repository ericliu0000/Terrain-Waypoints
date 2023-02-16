import numpy
import matplotlib.pyplot as plt
import pandas
from constants import *

# the point of this file is to see whether i can spin a grid of points around
# the origin and then move it to the site


def rotation_test() -> None:
    # just for proof of concept of spinning points, i think
    points = numpy.meshgrid(numpy.linspace(-5, 5, 10), numpy.linspace(-5, 5, 10))
    spin = numpy.radians(5)
    rotation = numpy.array([[numpy.cos(spin), -numpy.sin(spin)],
                            [numpy.sin(spin), numpy.cos(spin)]])

    # i do not know what einstein summation is
    res = numpy.einsum("ji, mni -> jmn", rotation, numpy.dstack(points))

    plt.scatter(points[0], points[1])
    plt.scatter(res[0], res[1], color='r')
    plt.show()


def rotation_translation_test() -> None:
    # take a set of points, move it to origin, rotate it, move it back
    # just has to be "good enough", i think -- margins provided by the terrain
    # filter should pick everything else away
    # trying to rotate around whatever isn't the origin

    x, y = numpy.meshgrid(numpy.linspace(15, 25, 10), numpy.linspace(15, 25, 10))

    # pick center i think, then move it
    x_center, y_center = 23, 18
    x1, y1 = x - x_center, y - y_center

    # spin!!
    spin = numpy.radians(25)
    rotation = numpy.array([[numpy.cos(spin), -numpy.sin(spin)],
                            [numpy.sin(spin), numpy.cos(spin)]])

    res = numpy.einsum("ji, mni -> jmn", rotation, numpy.dstack([x1, y1]))

    # okay move it back
    res_x, res_y = res[0] + x_center, res[1] + y_center
    marker_size = 0.75

    plt.plot(x_center, y_center, marker="*", markersize=15)

    # original
    plt.scatter(x, y, color='b', s=marker_size)
    # shift to origin
    plt.scatter(x1, y1, color='orange', s=marker_size)
    # spin it!
    plt.scatter(res[0], res[1], color='r', s=marker_size)
    # move it back
    plt.scatter(res_x, res_y, color='purple', s=marker_size)

    # try the function
    func_x, func_y = spin_around_point(x, y, x_center, y_center, spin)
    plt.scatter(func_x, func_y, s=2.1)

    print(res_x == func_x, res_y == func_y)

    # make plot square
    plt.xlim(-15, 26)
    plt.ylim(-9, 32)

    plt.show()


def spin_around_point(x, y, x_center, y_center, r) -> numpy.ndarray:
    r = numpy.radians(r)
    origin_graph = x - x_center, y - y_center
    rotation = numpy.array([[numpy.cos(r), -numpy.sin(r)],
                            [numpy.sin(r), numpy.cos(r)]])
    rotated_x, rotated_y = numpy.einsum("ji, mni -> jmn", rotation, numpy.dstack(origin_graph))

    output = rotated_x + x_center, rotated_y + y_center
    return output

# rotation_translation_test()


class SiteTest:
    def __init__(self, doc) -> None:
        self.data = pandas.read_hdf(doc, "a").to_numpy()
        self.spacing, self.values = self.data[..., :2], self.data[..., 2]

        self.x_grid = numpy.arange(self.spacing[:, 0].min(), self.spacing[:, 0].max(), CAMERA_V,
                                   dtype=numpy.float64)
        self.y_grid = numpy.arange(self.spacing[:, 1].min(), self.spacing[:, 1].max(), CAMERA_H,
                                   dtype=numpy.float64)

        a, b = numpy.meshgrid(self.x_grid, self.y_grid)

        self.rotated = spin_around_point(a, b, 950500, 799500, 10)

        plt.scatter(a, b)
        plt.scatter(self.rotated[0], self.rotated[1])

        plt.axis("square")
        plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])

        plt.show()


if __name__ == "__main__":
    SiteTest(FILE)