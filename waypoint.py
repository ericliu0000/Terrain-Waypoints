import datetime

import matplotlib.pyplot as plt
import numpy
import pyproj

from filter import SiteFilter
from rectangular_gradient import WaypointGridGradient


class WaypointGenerator:
    clearance: int = 00
    waypoints: list = []

    def __init__(self, doc: str) -> None:
        site = SiteFilter(doc)
        values = site.filtered
        inverted = False

        for row in values:
            line = []
            for point in row:
                # move every point normal by buf
                line.append([point[0] + point[3] * self.clearance, point[1] + point[4] * self.clearance, point[2] + point[5] * self.clearance])
            if inverted: self.waypoints.append(line[::-1])
            else: self.waypoints.append(line)
            inverted = not inverted

        # Perhaps do a similar thing with filtering and gather waypoints in batches and go around the mountain

    # TODO: fix these two methods because the coordinates might be in the wrong order
    def export(self) -> None:
        """Export the waypoints to a file (EPSG 32119)."""
        with open(f"output/{datetime.datetime.now()}.csv", "w") as file:
            file.write("Easting,Northing,Altitude\n")
            for (altitude, waypoints) in zip(self.altitudes, self.waypoints):
                for waypoint in waypoints:
                    file.write(f"{waypoint[0]},{waypoint[1]},{altitude}\n")

    def export_latlong(self) -> None:
        """Export the waypoints to a file (EPSG 4326)."""

        with open(f"output/{datetime.datetime.now()}_latlong.csv", "w") as file:
            file.write("Latitude,Longitude,Altitude\n")
            for (altitude, waypoints) in zip(self.altitudes, self.waypoints):
                for waypoint in waypoints:
                    transformer = pyproj.Transformer.from_proj('epsg:32119', 'epsg:4326')
                    x, y = transformer.transform(waypoint[0], waypoint[1])
                    file.write(f"{y},{x},{altitude}\n")


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

        # x, y = numpy.meshgrid(x, y)
        # graph.plot_surface(x, y, z, linewidth=0, cmap=plt.cm.terrain)

        # Plot waypoints
        last = (self.waypoints[0][0][0], self.waypoints[0][0][1], self.waypoints[0][0][2])
        for row in self.waypoints:
            for point in row:
                plt.plot([point[0], last[0]], [point[1], last[1]], [point[2], last[2]], "r")
                last = (point[0], point[1], point[2])
                plt.plot(point[0], point[1], point[2], "bo")

        plt.show()


if __name__ == "__main__":
    # a = WaypointGenerator("data/cloud_lasground.h5", [3400, 3450, 3500, 3550])
    # a.export()

    WaypointPlotter("data/cloud_lasground.h5")
