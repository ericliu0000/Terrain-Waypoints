from filter import SiteFilter
import matplotlib.pyplot as plt
import numpy

class WaypointGenerator:
    # TODO: make the length work
    length = 150
    new_points = []

    def __init__(self, doc, height):
        site = SiteFilter(doc, height)
        values = list(site.coords.values())

        for point in values:
            point = numpy.array(sorted(point, key=lambda x: x[1]))
            # plot points
            plt.plot(point[:, 0], point[:, 1], "go")

            # polynomial fit
            eq = numpy.polyfit(point[:, 1], point[:, 0], 3)
            x = numpy.linspace(point[:, 1].min(), point[:, 1].max(), 100)

            # plot fit
            y = 0
            for degree, coefficient in enumerate(eq[::-1]):
                y += coefficient * x ** degree

            plt.plot(y, x, "b")

            # Slope perpendicular to the fit
            for i in range(1, len(x) - 1):
                last = (x[i - 1], y[i - 1])
                next = (x[i], y[i])

                midpoint = ((last[1] + next[1]) / 2, (last[0] + next[0]) / 2)
                normal = -(next[1] - last[1]) / (next[0] - last[0])
                unit = (1, normal) / numpy.linalg.norm((1, normal))
                
                new_point = (midpoint[0] + unit[0] * self.length, midpoint[1] + unit[1] * self.length)
                self.new_points.append(new_point)

                plt.plot([midpoint[0], new_point[0]], [midpoint[1], new_point[1]], "b")


if __name__ == "__main__":
    WaypointGenerator("data/cloud_lasground.h5", [3400])
    from show_gradient import site_slope_only
    site_slope_only()

