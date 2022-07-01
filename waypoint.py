import datetime

import matplotlib.pyplot as plt
import numpy
import pyproj

from filter import SiteFilter
from rectangular_gradient import WaypointGridGradient


class WaypointGenerator:
    clearance: int = 100
    waypoints: list = []

    def __init__(self, doc: str) -> None:
        site = SiteFilter(doc)
        values = site.filtered
        inverted = False

        for row in values:
            line = []

            # move every point normal by buf
            for point in row:
                line.append([point[0] + point[3] * self.clearance, point[1] + point[4] * self.clearance, point[2] + point[5] * self.clearance])

            # reverse every other line
            if inverted:
                self.waypoints.append(line[::-1])
            else:
                self.waypoints.append(line)
            inverted = not inverted

    def export(self) -> None:
        """Export the waypoints to a file (EPSG 32119)."""

        with open(f"output/{datetime.datetime.now()}.csv", "w") as file:
            file.write("Easting,Northing,Altitude\n")
            for row in self.waypoints:
                for point in row:
                    file.write(f"{point[0]},{point[1]},{point[2]}\n")

    def export_latlong(self) -> None:
        """Export the waypoints to a file (EPSG 4326)."""

        p = pyproj.Proj("+proj=lcc +lat_0=33.75 +lon_0=-79 +lat_1=36.1666666666667 +lat_2=34.3333333333333 +x_0=609601.22 +y_0=0 +datum=NAD83 +units=m no_defs +ellps=GRS80 +towgs84=0,0,0")
        with open(f"output/{datetime.datetime.now()}_latlong.csv", "w") as file:
            file.write("Latitude,Longitude,Altitude\n")
            for row in self.waypoints:
                for point in row:
                    x, y = p(point[0], point[1], inverse=True)    
                    file.write(f"{x},{y},{point[2]}\n")


class WaypointPlotter(WaypointGenerator):
    """Generate and plot waypoints"""

    def __init__(self, doc: str) -> None:
        super().__init__(doc)
        # Plot terrain
        obj = WaypointGridGradient("data/cloud_lasground.h5")
        x, y = obj.x_grid, obj.y_grid
        z = obj.height

        graph = plt.axes(projection="3d")
        graph.set_xlabel("Easting")
        graph.set_ylabel("Northing")
        graph.set_zlabel("Altitude")

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
    a = WaypointGenerator("data/cloud_lasground.h5")
    a.export_latlong()

    # WaypointPlotter("data/cloud_lasground.h5")
