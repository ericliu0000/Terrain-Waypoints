import os
import matplotlib.pyplot as plt
import numpy
import pandas
import scipy.interpolate

from constants import *


class WaypointGenerator:
    def __init__(self, doc: str, aclearance=CLEARANCE) -> None:
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

        # Create interpolator
        h_interp = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, self.height.T)

        print(a.shape, b.shape)
        # Test points based on existing info
        with open("test.txt", "w") as n:
            for x in range(a.shape[0]):
                ln = ""
                for y in range(a.shape[1]):
                    # print(a[x, y], b[x, y])
                    ln += str(h_interp.ev(a[x, y], b[x, y]))
                    # input("STOP")
                n.write(ln + "\n")
        # while True:
        #     x, y = input("GO ").split()
        #     print(h_interp.ev(float(x), float(y)))

    def export(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")
        return export(self.waypoints)

    def export_latlong(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")

        return export_latlong(self.waypoints)


class WaypointPlotter(WaypointGenerator):
    def __init__(self, doc: str, plot_surface=False) -> None:
        super().__init__(doc)
        # Plot terrain
        x, y = self.x_grid, self.y_grid
        z = self.height

        graph = plt.axes(projection="3d")
        graph.set_xlabel("Easting (x)")
        graph.set_ylabel("Northing (y)")
        graph.set_zlabel("Altitude (z)")

        x, y = numpy.meshgrid(x, y)
        print(x, y)
        print(x.shape, x[0].shape, y.shape, y[0].shape)

        if plot_surface:
            graph.plot_surface(x, y, z, linewidth=0, cmap=plt.cm.terrain)

        graph.view_init(25, 0, 0)
        plt.savefig("4.png")
        plt.show()


if __name__ == "__main__":
    # a = WaypointGenerator(FILE)
    a = WaypointPlotter(FILE, True)
    # a.export()
    # print(CAMERA_H)
    # print(CAMERA_V)
    # print(CLEARANCE)
    # print(Z_FILTER)
