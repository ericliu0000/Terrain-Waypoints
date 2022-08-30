import datetime

import matplotlib.pyplot as plt
import numpy
import pyproj

import constants
from filter import SiteFilter


class WaypointGenerator:
    waypoints: list = []

    def __init__(self, doc: str, clearance=constants.CLEARANCE) -> None:
        self.site = SiteFilter(doc)
        self.values = self.site.filtered
        inverted = False
        self.clearance = clearance

        for row in self.values:
            line = []

            # Translate each point normal to the surface by clearance distance
            for point in row:
                line.append([point[0] + point[3] * self.clearance, point[1] + point[4] * self.clearance,
                             point[2] + point[5] * self.clearance])

            # Reverse the order of every other line
            if inverted:
                self.waypoints.append(line[::-1])
            else:
                self.waypoints.append(line)
            inverted = not inverted

    def export(self) -> None:
        """Export the waypoints to a file (EPSG 32119)."""

        with open(f"output/{datetime.datetime.now()}.csv", "w") as file:
            file.write(constants.OUTPUT_HEADER)
            count = 0

            for row in self.waypoints:
                for point in row:
                    count += 1
                    file.write(f"{count},{point[0]},{point[1]},{point[2]}\n")

            print(f"Exported {count} waypoints to {file.name}")

    def export_latlong(self) -> None:
        """Export the waypoints to a file (EPSG 4326)."""

        p = pyproj.Proj(constants.PROJECTION)
        with open(f"output/{datetime.datetime.now()}_latlong.csv", "w") as file:
            file.write(constants.OUTPUT_HEADER)
            count = 0

            for row in self.waypoints:
                for point in row:
                    count += 1
                    x, y = p(point[0], point[1], inverse=True)
                    file.write(f"{count},{x},{y},{point[2]}\n")

            print(f"Exported {count} waypoints to {file.name}")


class WaypointPlotter(WaypointGenerator):
    """Generate and plot waypoints"""

    def __init__(self, doc: str) -> None:
        super().__init__(doc)
        # Plot terrain
        x, y = self.site.obj.x_grid, self.site.obj.y_grid
        z = self.site.obj.height

        graph = plt.axes(projection="3d")
        graph.set_xlabel("Easting (x)")
        graph.set_ylabel("Northing (y)")
        graph.set_zlabel("Altitude (z)")

        x, y = numpy.meshgrid(x, y)
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
    # a = WaypointGenerator(constants.FILE)
    # a.export()
    # a.export_latlong()

    WaypointPlotter(constants.FILE)
