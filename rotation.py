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
    res = numpy.einsum('ji, mni -> jmn', rotation, numpy.dstack(points))

    plt.scatter(points[0], points[1])
    plt.scatter(res[0], res[1], color='r')
    plt.show()

