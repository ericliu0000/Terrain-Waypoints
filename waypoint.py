import matplotlib.pyplot as plt
import numpy

import constants
from filter import SiteFilter


class WaypointGenerator:
    waypoints: list = []

    def __init__(self, doc: str, aclearance=constants.CLEARANCE) -> None:
        self.site = SiteFilter(doc)
        self.values = self.site.filtered
        inverted = False

        for row in self.values:
            line = []

            # Translate each point normal to the surface by clearance distance
            for point in row:
                line.append([point[0] + point[3] * aclearance, point[1] + point[4] * aclearance,
                             point[2] + point[5] * constants.CLEARANCE])

            # Reverse the order of every other line
            if inverted:
                self.waypoints.append(line[::-1])
            else:
                self.waypoints.append(line)
            inverted = not inverted

    def export(self) -> None:
        print(constants.export(self.waypoints))

    def export_latlong(self) -> None:
        print(constants.export_latlong(self.waypoints))


class WaypointPlotter(WaypointGenerator):
    """Generate and plot waypoints"""

    def __init__(self, doc: str, plot_surface=True) -> None:
        super().__init__(doc)
        # Plot terrain
        x, y = self.site.obj.x_grid, self.site.obj.y_grid
        z = self.site.obj.height

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
    # a = WaypointGenerator(constants.FILE)
    # a.export()
    # a.export_latlong()

    WaypointPlotter(constants.FILE, True)
