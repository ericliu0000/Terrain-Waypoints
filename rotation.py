import numpy
import matplotlib.pyplot as plt

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

    # make plot square
    plt.xlim(-15, 26)
    plt.ylim(-9, 32)
    
    plt.show()


rotation_translation_test()