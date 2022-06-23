from filter import SiteFilter
import matplotlib.pyplot as plt
import numpy

site = SiteFilter("data/cloud_lasground.h5", [3560, 3500, 3440, 3380])
values = list(site.coords.values())

for point in values:
    point = numpy.array(sorted(point, key=lambda x: x[1]))

    # Find the slope perpendicular to all the points
    slopes = []

    for i in range(1, len(point) - 1):
        slopes.append(-(point[i][0] - point[i - 1][0]) / (point[i][1] - point[i - 1][1]))
        plt.plot([point[i - 1][0], point[i][0]], [point[i - 1][1], point[i][1]], "go")

    eq = numpy.polyfit(point[:, 1], point[:, 0], 2)
    x = numpy.linspace(point[:, 1].min(), point[:, 1].max(), 100)
    y = eq[0] * x ** 2 + eq[1] * x + eq[2] 

    plt.plot(y, x, "b")

from show_gradient import site_slope_only
site_slope_only()

plt.show()
