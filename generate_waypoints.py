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
            row = []
            for j in range(len(coordinates)):
                # Filter bounds and remove points below 3420 feet
                point = coordinates[j][i]
                if LEFT_BOUND < point[0] < RIGHT_BOUND and lower(point[0]) < point[1] < upper(point[0]) and point[
                        2] > Z_FILTER:
                    row.append([*point, *normal(dy.ev(point[0], point[1]), dx.ev(point[0], point[1]))])
            if row:
                self.filtered.append(row)
                
        inverted = False

        for row in self.filtered:
            line = []

            # Translate each point normal to the surface by clearance distance
            for point in row:
                line.append([point[0] + point[3] * aclearance, point[1] + point[4] * aclearance,
                             point[2] + point[5] * CLEARANCE])

            # Reverse the order of every other line
            if inverted:
                self.waypoints.append(line[::-1])
            else:
                self.waypoints.append(line)
            inverted = not inverted

    def export(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")
        return export(self.waypoints)

    def export_latlong(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")

        return export_latlong(self.waypoints)


class WaypointPlotter(WaypointGenerator):
    def __init__(self, doc: str, plot_surface=False, lim=None) -> None:
        super().__init__(doc)
        # Plot terrain
        x, y = self.x_grid, self.y_grid
        z = self.height

        graph = plt.axes(projection="3d")
        graph.view_init(elev=10, azim=-110)
        graph.set_xlabel("Easting (x)")
        graph.set_ylabel("Northing (y)")
        graph.set_zlabel("Altitude (z)")

        # Set limits to fix bound
        if lim is not None:
            graph.set_xlim(lim[0])
            graph.set_ylim(lim[1])
            graph.set_zlim(lim[2])

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
    # a = WaypointGenerator(FILE)
    # a.export()
    # print(CAMERA_H)
    # print(CAMERA_V)
    # print(CLEARANCE)
    # print(Z_FILTER)

    a = WaypointPlotter(FILE, True)
    plt.savefig("a.png")
    b = WaypointPlotter(FILE, False)
    plt.savefig("b.png")
