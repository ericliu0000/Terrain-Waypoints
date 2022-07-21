import matplotlib.pyplot as plt
import numpy

from filter import SiteFilter
from rectangular_gradient import InterpolatedGridGradient

obj = InterpolatedGridGradient("data/cloud_lasground.h5")
x_val, y_val = obj.x_grid, obj.y_grid
gradient = obj.magnitude

z_min = 0
z_max = 2

z = numpy.clip(gradient, z_min, z_max)
plt.contourf(x_val, y_val, z, 20, cmap=plt.cm.Reds, vmin=z_min, vmax=z_max)

plt.colorbar()

# Reference lines and background image
plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])
# Upper limitation
plt.plot([950370, 950550], [800374, 800374], "b", linewidth=3)
# Upper segment
plt.plot([950258, 950370], [799699, 800374], "b", linewidth=3)
# Left segment
plt.plot([950274, 950258], [799400, 799699], "b", linewidth=3)
# Lower segment
plt.plot([950396, 950274], [798926, 799400], "b", linewidth=3)
# Lower limitation
plt.plot([950396, 950550], [798926, 798926], "b", linewidth=3)
# Right side limitation
plt.plot([950550, 950550], [798926, 800374], "b", linewidth=3)

obj = SiteFilter("data/cloud_lasground.h5")


# Derestrictive set of points (incl. 10 m buffer)
def upper(coord):
    return min((6.0268 * (coord - 950258) + 799699), 800374)


def lower(coord):
    return max((-18.6875 * (coord - 950274) + 799400), (-3.8852 * (coord - 950274) + 799400), 798926)


left = 950290

# Plot trajectory of lines
x = numpy.linspace(950250, 950600)
y = [upper(z) for z in x]
# plt.plot(x, y, "go")

y = [lower(z) for z in x]
# plt.plot(x, y, "go")

# Plot points
for value in obj.filtered:
    for row in value:
        x = row[0]
        # plt.plot(x, row[1], "ro")

plt.show()
