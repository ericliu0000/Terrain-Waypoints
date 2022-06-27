import pyproj
from filter import SiteFilter
import matplotlib.pyplot as plt
import numpy
import datetime

from rectangular_gradient import InterpolatedGridGradient


class WaypointGenerator:
    """Generate points fitted to a polynomial curve defined by points at a certain elevation, and offset it."""
    length: int = 150
    overlap: int = 80
    waypoints: list = []
    altitudes: list = []
    new_points: list
    midpoints: list
    unit_normals: list
    inverse: bool = False

    # this is just a random point in the highway
    highway: int = 950700

    def __init__(self, doc: str, height: list, plot: bool = False) -> None:
        site = SiteFilter(doc, height)
        values = list(site.coords.values())

        # stash altitudes
        self.altitudes = height

        for point in values:
            self.new_points = []
            self.midpoints = []
            self.unit_normals = []

            point = numpy.array(sorted(point, key=lambda pt: pt[1]))

            # polynomial fit
            eq = numpy.polyfit(point[:, 1], point[:, 0], 3)
            x = numpy.linspace(point[:, 1].min() - self.overlap, point[:, 1].max() + self.overlap, int((point[:, 1].max() - point[:, 1].min() + self.overlap * 2) / 10))

            y = 0
            for degree, coefficient in enumerate(eq[::-1]):
                y += coefficient * x ** degree
                print(coefficient)

            # Slope perpendicular to the fit
            for i in range(1, len(x) - 1):
                back = (x[i - 1], y[i - 1])
                front = (x[i], y[i])

                # get direction of normal vector
                self.midpoints.append(((back[1] + front[1]) / 2, (back[0] + front[0]) / 2))
                normal = -(front[1] - back[1]) / (front[0] - back[0])
                self.unit_normals.append(((1, normal) / numpy.linalg.norm((1, normal))).tolist())

            # find the index of the unit normal with the minimum Y value, and stretch it to highway points
            min_index = self.unit_normals.index(min(self.unit_normals, key=lambda pt: abs(pt[1])))
            self.length = self.highway - self.midpoints[min_index][0]

            # get new points
            for (midpoint, unit) in zip(self.midpoints, self.unit_normals):
                new_point = (midpoint[0] + unit[0] * self.length, midpoint[1] + unit[1] * self.length)
                self.new_points.append(new_point)

            # reverse trajectory so altitude can increase on same side
            if self.inverse:
                self.waypoints.append(self.new_points[::-1])
            else:
                self.waypoints.append(self.new_points)

            self.inverse = not self.inverse

            if plot:
                # plot original points and fit
                plt.plot(point[:, 0], point[:, 1], "go")
                plt.plot(y, x, "b")

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

        graph.contour3D(x, y, z, 80, cmap=plt.cm.terrain)

        # Plot waypoints
        last = (self.waypoints[0][0][0], self.waypoints[0][0][1], height[0])
        for (altitude, waypoints) in zip(self.altitudes, self.waypoints):
            for point in waypoints:
                plt.plot([point[0], last[0]], [point[1], last[1]], [altitude, last[2]], "r")
                last = (point[0], point[1], altitude)


if __name__ == "__main__":
    # a = WaypointGenerator("data/cloud_lasground.h5", [3400, 3450, 3500, 3550])
    # a.export_latlong()

    WaypointGenerator("data/cloud_lasground.h5", [3400, 3450, 3500, 3550], plot=True)

    # a = WaypointPlotter("data/cloud_lasground.h5", list(range(3400, 3600, 20)))
    plt.show()
