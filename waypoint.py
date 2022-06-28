import pyproj
from filter import SiteFilter
import matplotlib.pyplot as plt
import numpy
import datetime

from rectangular_gradient import InterpolatedGridGradient


class WaypointGenerator:
    """Generate points fitted to a polynomial curve defined by points at a certain elevation, and offset it."""
    length: int = 150
    buf: int = 30.48 * 2
    clearance: int = 100
    waypoints: list = []
    altitudes: list = []
    fits: list = []
    new_points: list
    points: list
    unit_normals: list
    inverse: bool = False

    def __init__(self, doc: str, height: list, plot: bool = False) -> None:
        site = SiteFilter(doc, height)
        values = list(site.coords.values())

        # stash altitudes
        self.altitudes = height

        for row in values:
            self.new_points = []
            self.points = []
            self.midpoints = []
            self.unit_normals = []

            row = numpy.array(sorted(row, key=lambda pt: pt[1]))

            # polynomial fit
            eq = numpy.polyfit(row[:, 1], row[:, 0], 3)

            # TODO: Be able to add additional lines above the site to get additional coverage -- perhaps reuse a
            #  certain line (3600ft?) with a transformation

            for i in range(1, row.shape[0] - 1):
                point = ((row[i - 1][0] + row[i][0]) / 2, (row[i - 1][1] + row[i][1]) / 2)
                self.midpoints.append(point)

                # find unit tangent at that point based on x value
                y = point[1]
                slope = 0
                for degree, coefficient in enumerate(eq[::-1]):
                    slope += degree * coefficient * y ** (degree - 1)

                self.unit_normals.append(((-slope, 1) / numpy.linalg.norm((-slope, 1))).tolist())

            # get new points, stretching them by clearance off terrain
            for (midpoint, normal) in zip(self.midpoints, self.unit_normals):
                new_point = (midpoint[0] + normal[1] * self.clearance, midpoint[1] + normal[0] * self.clearance)
                self.new_points.append(new_point)

            # reverse trajectory so altitude can increase on same side
            if self.inverse:
                self.waypoints.append(self.new_points[::-1])
            else:
                self.waypoints.append(self.new_points)
            self.inverse = not self.inverse

            if plot:
                # plot original points and fit
                plt.plot(row[:, 0], row[:, 1], "go")
                y = numpy.linspace(row[:, 1].min(), row[:, 1].max())
                x = 0
                for degree, coefficient in enumerate(eq[::-1]):
                    x += coefficient * y ** degree
                plt.plot(x, y, "r")

                # graph the transformation for each points
                for (midpoint, new) in zip(self.midpoints, self.new_points):
                    plt.plot((midpoint[0], new[0]), (midpoint[1], new[1]), "b")

        if plot:
            from show_gradient import site_slope_only
            site_slope_only()

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

    def __init__(self, doc: str, height: list) -> None:
        super().__init__(doc, height)
        # Plot terrain
        obj = InterpolatedGridGradient("data/cloud_lasground.h5")
        x, y = obj.x_grid, obj.y_grid
        z = obj.points

        graph = plt.axes(projection="3d")
        graph.set_xlabel("Easting")
        graph.set_ylabel("Northing")
        graph.set_zlabel("Altitude")

        x, y = numpy.meshgrid(x, y)

        graph.plot_surface(x, y, z, linewidth=0, cmap=plt.cm.terrain)

        # Plot waypoints
        last = (self.waypoints[0][0][0], self.waypoints[0][0][1], height[0])
        for (altitude, waypoints) in zip(self.altitudes, self.waypoints):
            for point in waypoints:
                plt.plot([point[0], last[0]], [point[1], last[1]], [altitude, last[2]], "r")
                last = (point[0], point[1], altitude)

        plt.show()


if __name__ == "__main__":
    # a = WaypointGenerator("data/cloud_lasground.h5", [3400, 3450, 3500, 3550])
    # a.export()

    WaypointGenerator("data/cloud_lasground.h5", [3400, 3450, 3500, 3550, 3600], plot=True)
    # WaypointGenerator("data/cloud_lasground.h5", [3500], plot=True)
    # WaypointPlotter("data/cloud_lasground.h5", list(range(3400, 3600, 6)))
