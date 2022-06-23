from filter import SiteFilter
import matplotlib.pyplot as plt
import numpy

site = SiteFilter("data/cloud_lasground.h5", [3500])
points = list(site.coords.values())[0]
points = numpy.array(sorted(points, key=lambda x: x[1]))

# Find the slope perpendicular to all the points
slopes = []

for i in range(1, len(points) - 1):
    slopes.append(-(points[i][0] - points[i - 1][0]) / (points[i][1] - points[i - 1][1]))
    plt.plot([points[i - 1][0], points[i][0]], [points[i - 1][1], points[i][1]], "go")

# print(slopes)
eq = numpy.polyfit(points[:, 1], points[:, 0], 2)
x = numpy.linspace(799100, 799900, 100)
y = eq[0] * x ** 2 + eq[1] * x + eq[2] 

plt.plot(y, x, "b")

from show_gradient import site_slope_only
site_slope_only()

plt.show()
