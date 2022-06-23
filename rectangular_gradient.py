import numpy
import pandas
import scipy.interpolate


class NumpyGradient:
    def __init__(self, doc):
        self.points = pandas.read_hdf(doc, "a").to_numpy()

        # only works if data is square
        s = self.points.shape[0] ** 0.5
        assert s == int(s), f"Data is not square: {self.points.shape}"
        self.points = numpy.reshape(self.points, (int(s), int(s), 3))

        self.spacing = self.points[..., :2]
        self.values = self.points[..., 2]

        # x and y partials
        self.gradient = numpy.gradient(self.values, self.spacing[0][..., 0], self.spacing[..., 1][:, 0])

        # get magnitude of gradient
        self.magnitude = ((self.gradient[0] ** 2) + (self.gradient[1] ** 2)) ** 0.5


class InterpolatedGridGradient:
    scale = 1

    def __init__(self, doc, method="linear", calculate_gradient=True):
        self.data = pandas.read_hdf(doc, "a").to_numpy()
        self.spacing, self.values = self.data[..., :2], self.data[..., 2]

        x_max, x_min = self.spacing[:, 0].max(), self.spacing[:, 0].min()
        y_max, y_min = self.spacing[:, 1].max(), self.spacing[:, 1].min()
        x_length, y_length = x_max - x_min, y_max - y_min

        # create grid
        self.x_grid = numpy.linspace(x_min, x_max, int(x_length * self.scale))
        self.y_grid = numpy.linspace(y_min, y_max, int(y_length * self.scale))

        self.points = scipy.interpolate.griddata(self.spacing, self.values,
                                                 (self.x_grid[None, :], self.y_grid[:, None]), method=method)

        if calculate_gradient:
            self.gradient = numpy.gradient(self.points, self.x_grid[1] - self.x_grid[0],
                                           self.y_grid[1] - self.y_grid[0])
            self.magnitude = ((self.gradient[0] ** 2) + (self.gradient[1] ** 2)) ** 0.5


if __name__ == "__main__":
    # gradient = NumpyGradient()
    # print(gradient.magnitude)

    gradient = InterpolatedGridGradient("data/cloud_simplified_2.h5")
