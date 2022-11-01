import os
import matplotlib.pyplot as plt
import numpy
import pandas
import scipy.interpolate

from constants import *


def normal(x, y):
    # Return upward unit normal vector from dx, dy
    return [-x, -y, 1] / numpy.linalg.norm([-x, -y, 1])


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
        dx = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, gradient[0].T, s=100)
        dy = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, gradient[1].T, s=100)

        # For each point, place in filtered (x, y, z, [unit normal -- dy, dx, dz])
        for i in range(len(coordinates[0]) - 1, -1, -1):
            for j in range(len(coordinates)):
                # Filter bounds and remove points below z filter
                point = coordinates[j][i]
                if LEFT_BOUND < point[0] < RIGHT_BOUND and lower(point[0]) < point[1] < upper(point[0]) and point[
                        2] > Z_FILTER:
                    self.filtered.append([*point, *normal(dy.ev(point[0], point[1]), dx.ev(point[0], point[1]))])

        # Give offsets to each point and add to waypoints list
        for point in self.filtered:
            self.waypoints.append([point[0] + point[3] * aclearance, point[1] + point[4] * aclearance,
                                   point[2] + point[5] * CLEARANCE])
        
        # Sort waypoints by z, then by x
        self.waypoints.sort(key=lambda x: (x[2], x[0]))

        # Split waypoints into 10 rows
        self.waypoints = numpy.array_split(self.waypoints, 5)

        # Split waypoints every 50 feet (z axis)

        # self.waypoints =         
        
        invert = False
        # Sort each row by x
        for i in range(len(self.waypoints)):
            self.waypoints[i] = sorted(self.waypoints[i].tolist(), key=lambda x: x[0])
            # self.waypoints[i].tolist().sort(key=lambda x: x[0])
            if invert:
                self.waypoints[i] = self.waypoints[i][::-1]
            invert = not invert

        # print(self.waypoints)

    def export(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")
        return export(self.waypoints)

    def export_latlong(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")

        return export_latlong(self.waypoints)


class WaypointPlotter(WaypointGenerator):
    def __init__(self, doc: str, plot_surface=True) -> None:
        super().__init__(doc)
        # Plot terrain
        x, y = self.x_grid, self.y_grid
        z = self.height

        graph = plt.axes(projection="3d")
        graph.set_xlabel("Easting (x)")
        graph.set_ylabel("Northing (y)")
        graph.set_zlabel("Altitude (z)")

        x, y = numpy.meshgrid(x, y)

        if plot_surface:
            graph.plot_surface(x, y, z, linewidth=0, cmap=plt.cm.terrain)

        # Plot waypoints
        last = (self.waypoints[0][0][0], self.waypoints[0][0][1], self.waypoints[0][0][2])

        for row in self.waypoints:
            for point in row:
                plt.plot([point[0], last[0]], [point[1], last[1]], [point[2], last[2]], "r")
                last = (point[0], point[1], point[2])
                plt.plot(*last, "bo")

        plt.show()


if __name__ == "__main__":
    a = WaypointGenerator(FILE)
    a.export()
    # print(CAMERA_H)
    # print(CAMERA_V)
    # print(CLEARANCE)
    # print(Z_FILTER)
