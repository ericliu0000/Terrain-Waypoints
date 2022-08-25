import numpy
import pandas
import scipy.interpolate


class InterpolatedGridGradient:
    """Extracts las data and attempts to interpolate to create an elevation model and the corresponding gradient."""
    scale = 2

    def __init__(self, doc: str, method: str = "linear", calculate_gradient: bool = True) -> None:
        # Read data from h5 file
        self.data = pandas.read_hdf(doc, "a").to_numpy()
        self.spacing, self.values = self.data[..., :2], self.data[..., 2]

        # Get bounds and length for x and y axes
        x_max, x_min = self.spacing[:, 0].max(), self.spacing[:, 0].min()
        y_max, y_min = self.spacing[:, 1].max(), self.spacing[:, 1].min()
        x_length, y_length = x_max - x_min, y_max - y_min

        # Create grid and interpolate values
        self.x_grid = numpy.linspace(x_min, x_max, int(x_length * self.scale))
        self.y_grid = numpy.linspace(y_min, y_max, int(y_length * self.scale))
        self.points = scipy.interpolate.griddata(self.spacing, self.values,
                                                 (self.x_grid[None, :], self.y_grid[:, None]), method=method)

        if calculate_gradient:
            self.gradient = numpy.gradient(self.points, self.x_grid[1] - self.x_grid[0],
                                           self.y_grid[1] - self.y_grid[0])
            self.magnitude = ((self.gradient[0] ** 2) + (self.gradient[1] ** 2)) ** 0.5