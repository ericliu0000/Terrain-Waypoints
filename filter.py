import numpy
import scipy.interpolate

import constants
from calculate_gradient import WaypointGradient


def normal(x, y):
    # Return upward unit normal vector from dx, dy
    return [-x, -y, 1] / numpy.linalg.norm([-x, -y, 1])


class SiteFilter:
    """Extracts the coordinates of the site from a las file and constrains it to the site"""
    filtered: list = []

    def __init__(self, doc: str) -> None:
        self.obj = WaypointGradient(doc)
        a, b = numpy.meshgrid(self.obj.x_grid, self.obj.y_grid)

        # Create a grid of coordinates with corresponding gradient values
        coordinates = numpy.dstack((a, b, self.obj.height))
        gradient = numpy.nan_to_num(self.obj.gradient)

        # Smooth values
        dx = scipy.interpolate.RectBivariateSpline(self.obj.x_grid, self.obj.y_grid, gradient[0].T, s=100)
        dy = scipy.interpolate.RectBivariateSpline(self.obj.x_grid, self.obj.y_grid, gradient[1].T, s=100)

        # For each point, place in filtered (x, y, z, [unit normal -- dy, dx, dz])
        for i in range(len(coordinates[0]) - 1, -1, -1):
            row = []
            for j in range(len(coordinates)):
                # Filter bounds and remove points below 3420 feet
                point = coordinates[j][i]
                if constants.left < point[0] < constants.right and constants.lower(point[0]) < point[
                    1] < constants.upper(point[0]) and point[2] > constants.Z_FILTER:
                    row.append([*point, *normal(dy.ev(point[0], point[1]), dx.ev(point[0], point[1]))])
            if row:
                self.filtered.append(row)


if __name__ == "__main__":
    test = SiteFilter(constants.FILE)
