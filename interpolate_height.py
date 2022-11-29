import numpy
import pandas
import scipy.interpolate
from constants import *
import matplotlib.pyplot as plt

CAMERA_H *= 3
CAMERA_V *= 3

class WaypointGenerator:
    def __init__(self, doc: str, aclearance=CLEARANCE) -> None:
        self.filtered = []
        self.waypoints = []

        # Read data from h5 file
        self.data = pandas.read_hdf(doc, "a").to_numpy()
        self.spacing, self.values = self.data[..., :2], self.data[..., 2]

        # Create grid
        self.x_grid = numpy.arange(self.spacing[:, 0].min(), self.spacing[:, 0].max(), CAMERA_V,
                                   dtype=numpy.float64)
        self.y_grid = numpy.arange(self.spacing[:, 1].min(), self.spacing[:, 1].max(), CAMERA_H,
                                   dtype=numpy.float64)

        # Interpolate values and calculate gradient
        self.height = scipy.interpolate.griddata(self.spacing, self.values,
                                                 (self.x_grid[None, :], self.y_grid[:, None]), method="linear")
        self.gradient = numpy.gradient(self.height, self.x_grid[1] - self.x_grid[0], self.y_grid[1] - self.y_grid[0])
        a, b = numpy.meshgrid(self.x_grid, self.y_grid)

        # Create a grid of coordinates with corresponding gradient values
        coordinates = numpy.dstack((a, b, self.height))
        gradient = numpy.nan_to_num(self.gradient)

        # Smooth values
        # dx = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, gradient[0].T, s=100)
        # dy = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, gradient[1].T, s=100)
        h = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, coordinates[..., 2].T, s=100)

        hev = lambda x, y: h.ev(x, y)
        height_result = hev(self.x_grid, self.y_grid)
        # plot dx and dy
        plt.contourf(self.x_grid, self.y_grid, height_result, 20, cmap=plt.cm.Reds, vmin=3000, vmax=3800)
        plt.colorbar()

        plt.show()

if __name__ == "__main__":
    WaypointGenerator("data/cloud_simplified_2.h5")