import matplotlib.pyplot as plt
import numpy

from filter import ElevationFilter
from rectangular_gradient import InterpolatedGridGradient

obj = InterpolatedGridGradient("data/cloud_lasground.h5")
# gradient
x_val, y_val = obj.x_grid, obj.y_grid
gradient = obj.magnitude

z_min = 0
z_max = 2

z = numpy.clip(gradient, z_min, z_max)

plt.contourf(x_val, y_val, z, 20, cmap=plt.cm.Blues, vmin=z_min, vmax=z_max)
# plt.colorbar()

plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])
# Upper segment
plt.plot([950310, 950410], [799640, 800310], "r")
# Upper limitation
plt.plot([950410, 950550], [800310, 800310], "r")
# Left segment
plt.plot([950310, 950310], [799400, 799640], "r")
# Lower segment
plt.plot([950440, 950310], [798970, 799400], "r")
# Lower limitation
plt.plot([950440, 950550], [798970, 798970], "r")


def upper(x):
    return min((6.7 * (x - 950310) + 799640), 800310)


def lower(x):
    return max((-3.3077 * (x - 950310) + 799400), 798970)


left = 950310

obj = ElevationFilter("data/cloud_lasground.h5", [3360, 3400, 3440, 3480])

for value in obj.coords.values():
    for row in value:
        x = row[0]
        if (x >= left) and (lower(x) <= row[1] <= upper(x)):
            plt.plot(x, row[1], "ro")
            print(f"Plotted {x} {row[1]}")

    # plt.plot(value[:, 0], value[:, 1], "ro")

plt.show()
