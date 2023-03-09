import numpy
import pandas
import scipy.interpolate
from constants import *
import matplotlib.pyplot as plt


# CAMERA_H *= 2
# CAMERA_V *= 2

class WaypointGenerator:
    def __init__(self, doc: str, aclearance=CLEARANCE) -> None:
        self.filtered = []
        self.waypoints = []

        # Read data from h5 file
        self.data = pandas.read_hdf(doc, "a").to_numpy()
        self.spacing, self.values = self.data[..., :2], self.data[..., 2]

        # bring all of the points to the origin
        # spin them all around
        # and then move them out
        # then do griddata on that

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
        print(coordinates[..., 2].T)
        # okay we can't use this, we need to use griddata with a list of points. they aren't going to be ordered if they
        # are not in a grid, but i think we can deal with that by generating the lists of points (3rd parameter) in the
        # order beforehand and then doing all the calculation at the end. this might have dramatic side effects though
        # maybe there is an alternative to griddata (like the bivariate splines) that works in 2d? 
        # TODO look into above
        h = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, coordinates[..., 2].T, s=100)

        hev = lambda x, y: h.ev(x, y)
        height_result = []
        for y in self.y_grid:
            row = []
            for x in self.x_grid:
                row.append(hev(x, y))
            height_result.append(row)
        # plot dx and dy
        plt.contourf(self.x_grid, self.y_grid, height_result, 20, cmap=plt.cm.Reds, vmin=3000, vmax=3800)
        plt.colorbar()
        # print(height_result)

        plt.show()


if __name__ == "__main__":
    WaypointGenerator("data/cloud_simplified_2.h5")
