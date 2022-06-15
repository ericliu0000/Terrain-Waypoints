from reader import XYZReader
import numpy

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