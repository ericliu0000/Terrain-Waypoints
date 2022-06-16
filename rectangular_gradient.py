from reader import *
import numpy
import scipy.interpolate


class SlopeGradient:
    def __init__(self):
        # Calculate x and y partial derivative from every single point in points from XYZReader
        reader = XYZReader("data/ncsutest.xyz")
        points = reader.points

        gradients = []

        for i in range(1, len(points) - 1):
            for j in range(1, len(points[i]) - 1):
                # Calculate partial derivative
                x_deriv = (points[i][j + 1][2] - points[i][j - 1][2]) / (points[i][j + 1][0] - points[i][j - 1][0])
                y_deriv = (points[i + 1][j][2] - points[i - 1][j][2]) / (points[i + 1][j][1] - points[i - 1][j][1])

                # print(x_deriv, y_deriv)
                print(f"z1 {points[i][j + 1][2]} z2 {points[i][j - 1][2]}\nx1 {points[i][j + 1][0]} x2 {points[i][j - 1][0]} xderiv {x_deriv}\ny1 {points[i + 1][j][1]} y2 {points[i - 1][j][1]} yderiv {y_deriv}")
                print(numpy.cross((1, 0, x_deriv), (0, 1, y_deriv)))

                # Get normal vector from x and y partial derivative
                normal = numpy.cross((1, 0, x_deriv), (0, 1, y_deriv))

                # get unit normal
                normal = normal / numpy.linalg.norm(normal)

                print(normal)
                # add to gradients
                gradients.append(normal)


class NumpyGradient:
    def __init__(self):
        reader = PandasReader("data/ncsutest.h5")
        self.spacing, self.values = reader.spacing, reader.values

        # x and y partials
        self.gradient = numpy.gradient(self.values, self.spacing[0][..., 0], self.spacing[..., 1][:, 0])

        # get magnitude gradient
        self.magnitude = ((self.gradient[0] ** 2) + (self.gradient[1] ** 2)) ** 0.5


        print(self.values, self.values.shape)
        print("\n\nx")
        print(self.spacing[0][..., 0], self.spacing[0][..., 0].shape)
        print("\n\ny")
        print(self.spacing[..., 1][:, 0], self.spacing[..., 1][:, 0].shape)
        print()

        # print(self.gradient)
        # print(self.gradient[0].shape)

class InterpolatedGridGradient:
    scale = 1

    def __init__(self, file):
        self.data = pandas.read_hdf(file, "test").to_numpy()
        self.spacing, self.values = self.data[..., :2], self.data[..., 2]

        x_max, x_min = self.spacing[:, 0].max(), self.spacing[:, 0].min()
        y_max, y_min = self.spacing[:, 1].max(), self.spacing[:, 1].min()
        x_length, y_length = x_max - x_min, y_max - y_min

        # create grid
        x_grid = numpy.linspace(x_min, x_max, int(x_length * self.scale))
        y_grid = numpy.linspace(y_min, y_max, int(y_length * self.scale))

        self.points = numpy.nan_to_num(scipy.interpolate.griddata(self.spacing, self.values, (x_grid[None, :], y_grid[:, None]), method="linear"))
        
        print(self.points, self.points.shape)
        print("\n\nx")
        print(x_grid, x_grid.shape)
        print("\n\ny")
        print(y_grid, y_grid.shape)
        print()
        self.gradient = numpy.gradient(self.points, x_grid, y_grid)


if __name__ == "__main__":
    # gradient = SlopeGradient()
    # gradient = NumpyGradient()
    # print(gradient.magnitude)

    gradient = InterpolatedGridGradient("data/cloud_simplified.h5")
    # print(gradient.gradient)