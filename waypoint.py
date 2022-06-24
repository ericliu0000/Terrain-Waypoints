from filter import SiteFilter
import matplotlib.pyplot as plt
import numpy

site = SiteFilter("data/cloud_lasground.h5", [3500])
values = list(site.coords.values())

for point in values:
    point = numpy.array(sorted(point, key=lambda x: x[1]))

    # polynomial fit -- testing
    eq = numpy.polyfit(point[:, 1], point[:, 0], 3)
    x = numpy.linspace(point[:, 1].min(), point[:, 1].max(), 100)

    y = 0
    for degree, coefficient in enumerate(eq[::-1]):
        y += coefficient * x ** degree

    plt.plot(y, x, "b")

    print(x, y)
    length = 150

    # Slope perpendicular to the fit
    for i in range(1, len(x) - 1):
        last = (x[i - 1], y[i - 1])
        next = (x[i], y[i])

        midpoint = ((last[1] + next[1]) / 2, (last[0] + next[0]) / 2)
        normal = -(next[1] - last[1]) / (next[0] - last[0])
        unit = (1, normal) / numpy.linalg.norm((1, normal))
        
        # print(midpoint, normal)
        new_point = (midpoint[0] + unit[0] * length, midpoint[1] + unit[1] * length)
        print(midpoint, new_point)

        plt.plot([midpoint[0], new_point[0]], [midpoint[1], new_point[1]], "b")

    # Find the slope perpendicular to all the points
    # slopes = []

    # for i in range(1, len(point) - 1):
    #     slopes.append(-(point[i][0] - point[i - 1][0]) / (point[i][1] - point[i - 1][1]))
    #     plt.plot([point[i - 1][0], point[i][0]], [point[i - 1][1], point[i][1]], "go")



from show_gradient import site_slope_only
site_slope_only()

plt.show()
