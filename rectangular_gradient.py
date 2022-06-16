from reader import *
import numpy


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

                print()
                input()


class NumpyGradient:
    def __init__(self):
        reader = PandasReader("data/ncsutest.h5")
        self.spacing, self.values = reader.spacing, reader.values

        # print(spacing)
        # print(spacing[0][..., 0])

        self.gradient = numpy.gradient(self.values, self.spacing[0][..., 0], self.spacing[..., 1][:, 0])

        # print(self.gradient)
        # print(self.gradient[0].shape)

if __name__ == "__main__":
    # gradient = SlopeGradient()
    gradient = NumpyGradient()
    print(gradient.gradient)