import os
import matplotlib.pyplot as plt
import numpy
import pandas
import scipy.interpolate

from constants import *


def normal(x: float, y: float) -> numpy.ndarray:
    # Return upward unit normal vector from dx, dy
    return [-x, -y, 1] / numpy.linalg.norm([-x, -y, 1])


def spin_around_point(x: numpy.ndarray, y: numpy.ndarray,
                      x_center: float, y_center: float, r: float) -> tuple[numpy.ndarray, numpy.ndarray]:
    r = numpy.radians(r)
    origin_graph = x - x_center, y - y_center
    rotation = numpy.array([[numpy.cos(r), -numpy.sin(r)],
                            [numpy.sin(r), numpy.cos(r)]])
    rotated_x, rotated_y = numpy.einsum("ji, mni -> jmn", rotation, numpy.dstack(origin_graph))

    output = rotated_x + x_center, rotated_y + y_center
    return output


class WaypointGenerator:
    spacing = []
    values = []

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

        # Rotate points
        a, b = numpy.meshgrid(self.x_grid, self.y_grid)
        # TODO make this a constant when done
        self.rotated = spin_around_point(a, b, 950500, 799500, 8)

        # Interpolate values and calculate gradient
        self.height = scipy.interpolate.griddata(self.spacing, self.values, self.rotated, method="linear")
        # Unsure whether this is right
        # self.gradient = numpy.gradient(self.height, self.rotated[1][:, 0], self.rotated[0][0])
        self.gradient = numpy.gradient(self.height, self.y_grid, self.x_grid)

        # Create a grid of coordinates with corresponding gradient values
        coordinates = numpy.dstack((self.rotated[0], self.rotated[1], self.height))
        self.gradient = numpy.nan_to_num(self.gradient)

        # Smooth values
        dx = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, self.gradient[0].T, s=100)
        dy = scipy.interpolate.RectBivariateSpline(self.x_grid, self.y_grid, self.gradient[1].T, s=100)

        # TODO Evaluate gradient --- make sure it's still perpendicular to ground
        # For each point, place in filtered (x, y, z, [unit normal -- dy, dx, dz])
        for i in range(len(coordinates[0]) - 1, -1, -1):
            row = []
            for j in range(len(coordinates)):
                # Filter bounds and remove points below 3420 feet
                point = coordinates[j][i]
                if LEFT_BOUND < point[0] < RIGHT_BOUND and lower(point[0]) < point[1] < upper(point[0]) and \
                        point[2] > Z_FILTER:
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

    # TODO maybe encode some data into each file about tiles, rotation
    def export(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")
        return export(self.waypoints)

    def export_latlong(self) -> str:
        if not os.path.exists("output"):
            os.makedirs("output")

        return export_latlong(self.waypoints)


class WaypointPlotter(WaypointGenerator):
    def __init__(self, doc: str, plot_surface=False, lim=None, name=None) -> None:
        super().__init__(doc)
        
        # Create new variables to make terrain appearance independent of waypoints
        x = numpy.arange(self.spacing[:, 0].min(), self.spacing[:, 0].max(), SURFACE_RES, dtype=numpy.float64)
        y = numpy.arange(self.spacing[:, 1].min(), self.spacing[:, 1].max(), SURFACE_RES, dtype=numpy.float64)
        x, y = numpy.meshgrid(x, y)
        z = scipy.interpolate.griddata(self.spacing, self.values, (x, y), method="linear")

        # Configure graph axes and labels

        graph = plt.axes(projection="3d", computed_zorder=False)
        graph.set_xlabel("Easting (x) (ft)", labelpad=25)
        graph.set_ylabel("Northing (y)", labelpad=25)
        graph.set_zlabel("Altitude (z)")
        graph.tick_params(axis="x", pad=0.2, labelsize=8)
        graph.tick_params(axis="y", pad=0.2, labelsize=8)

        # Plot terrain
        if plot_surface:
            graph.plot_surface(x, y, z, linewidth=0, cmap=plt.cm.terrain)

        # Set limits to fix bound
        if lim is not None:
            graph.set_xlim(lim[0])
            graph.set_ylim(lim[1])
            graph.set_zlim(lim[2])

        # Plot waypoints
        last = (self.waypoints[0][0][0], self.waypoints[0][0][1], self.waypoints[0][0][2])

        for row in self.waypoints:
            for point in row:
                plt.plot([point[0], last[0]], [point[1], last[1]], [point[2], last[2]], "r")
                last = (point[0], point[1], point[2])
                plt.plot(*last, "bo")

        # do a bunch of views
        for e in range(5, 31, 5):
            for a in range(-90, 91, 15):
                graph.view_init(elev=e, azim=a)
                xrot, yrot = max(-45, min((90 + a) % 180, 45)), a
                graph.tick_params(axis="x", pad=0.2, labelsize=8, labelrotation=xrot)
                graph.tick_params(axis="y", pad=0.2, labelsize=8, labelrotation=yrot)

                file = f"figures/e{e}a{a}-{'' if plot_surface else 'no'}surface.png"
                plt.savefig(file, dpi=100)
                print(f"saved {file}")

        # # If desired, save file
        # if name is not None:
        #     plt.savefig(f"{name}.png", dpi=600)
        # else:
        #     plt.show()


if __name__ == "__main__":
    bounds = [(950101, 950800), (798340, 800600), (3370, 3670)]

    a = WaypointPlotter(FILE, True, bounds, "a")
    b = WaypointPlotter(FILE, False, bounds, "b")
