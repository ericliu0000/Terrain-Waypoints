import numpy

from rectangular_gradient import WaypointGridGradient


# Only take restrictive set (rock face points only) for regression limits
def upper(coord):
    return min((6.0268 * (coord - 950288) + 799669), 800344)


def lower(coord):
    return max((-16.8125 * (coord - 950304) + 799400), (-3.6393 * (coord - 950304) + 799400), 798956)


def normal(x, y):
    # Return upward unit normal vector from dx, dy
    return [-x, -y, 1] / numpy.linalg.norm([-x, -y, 1])


class SiteFilter:
    """Extracts the coordinates of the site from a las file and constrains it to the site"""
    left: float = 950310
    right: float = 950600
    filtered: list = []
    

    def __init__(self, doc: str) -> None:
        self.obj = WaypointGridGradient(doc)
        a, b = numpy.meshgrid(self.obj.x_grid, self.obj.y_grid)

        # make a grid of filled xy values based on axis labels xgrid and ygrid
        coordinates = numpy.dstack((a, b, self.obj.height))
        gradient = self.obj.gradient

        # For each point, place in filtered (x, y, z, [unit normal])
        for i in range(len(coordinates)):
            for j in range(len(coordinates[i])):
                point = coordinates[i][j]
                if self.left < point[0] < self.right and lower(point[0]) < point[1] < upper(point[0]) and point[2] > 3420:
                    self.filtered.append([*point, *normal(gradient[0][i][j], gradient[1][i][j])])


if __name__ == "__main__":
    test = SiteFilter("data/cloud_lasground.h5")
