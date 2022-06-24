from filter import SiteFilter
import matplotlib.pyplot as plt
import numpy


class WaypointGenerator:
    """Generate points fitted to a polynomial curve defined by points at a certain elevation, and offset it."""
    # TODO: make the length work
    length = 150

    # this is just a random point in the highway
    highway = 950700

    def __init__(self, doc, height):
        site = SiteFilter(doc, height)
        values = list(site.coords.values())

        for point in values:
            self.new_points = []
            self.midpoints = []
            self.unit_normals = []

            point = numpy.array(sorted(point, key=lambda x: x[1]))
            # plot points
            plt.plot(point[:, 0], point[:, 1], "go")

            # polynomial fit
            eq = numpy.polyfit(point[:, 1], point[:, 0], 3)
            x = numpy.linspace(point[:, 1].min(), point[:, 1].max(), int((point[:, 1].max() - point[:, 1].min()) / 10))

            # plot fit
            y = 0
            for degree, coefficient in enumerate(eq[::-1]):
                y += coefficient * x ** degree

            plt.plot(y, x, "b")

            # Slope perpendicular to the fit
            for i in range(1, len(x) - 1):
                last = (x[i - 1], y[i - 1])
                next = (x[i], y[i])

                self.midpoints.append(((last[1] + next[1]) / 2, (last[0] + next[0]) / 2))
                normal = -(next[1] - last[1]) / (next[0] - last[0])
                self.unit_normals.append(((1, normal) / numpy.linalg.norm((1, normal))).tolist())

            # testing for now: modular length offset
            self.normalize_middle()

            # graph the transformation for each points
            for (midpoint, new) in zip(self.midpoints, self.new_points):
                plt.plot((midpoint[0], new[0]), (midpoint[1], new[1]), "b")

    def constant_offset(self):
        for (midpoint, unit) in zip(self.midpoints, self.unit_normals):
            new_point = (midpoint[0] + unit[0] * self.length, midpoint[1] + unit[1] * self.length)
            self.new_points.append(new_point)

    def normalize_middle(self):
        # find the index of the unit normal with the minimum Y value
        min_index = self.unit_normals.index(min(self.unit_normals, key=lambda x: abs(x[1])))

        # make the middle point stretch to highway point
        self.length = self.highway - self.midpoints[min_index][0]
        self.constant_offset()


if __name__ == "__main__":
    WaypointGenerator("data/cloud_lasground.h5", [3400, 3450, 3500, 3550])
    from show_gradient import site_slope_only

    site_slope_only()
