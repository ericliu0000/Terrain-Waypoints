from filter import SiteFilter
import matplotlib.pyplot as plt

site = SiteFilter("data/cloud_lasground.h5", [3500])
points = list(site.coords.values())[0]
points = sorted(points, key=lambda x: x[1])

# Find the slope perpendicular to all the points
slopes = []

for i in range(1, len(points) - 1):
    slopes.append(-(points[i][0] - points[i - 1][0]) / (points[i][1] - points[i - 1][1]))
    plt.plot([points[i - 1][0], points[i][0]], [points[i - 1][1], points[i][1]], "r")

# print(slopes)
plt.show()