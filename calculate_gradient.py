import numpy
import pandas
import scipy.interpolate


class WaypointGradient:
    """Extracts las data, interpolates to grid, and returns gradient. Specifically intended for waypoint generation"""
    scale: float = 1
    hdev: float = 3.0 * 3.048 * scale
    vdev: float = 2.3 * 3.048 * scale

    def __init__(self, doc: str) -> None:
        # Read data from h5 file
        self.data = pandas.read_hdf(doc, "a").to_numpy()
        self.spacing, self.values = self.data[..., :2], self.data[..., 2]

        # Create grid 
        self.x_grid = numpy.arange(self.spacing[:, 0].min(), self.spacing[:, 0].max(), self.vdev, dtype=numpy.float64)
        self.y_grid = numpy.arange(self.spacing[:, 1].min(), self.spacing[:, 1].max(), self.hdev, dtype=numpy.float64)

        # Interpolate values and calculate gradient
        self.height = scipy.interpolate.griddata(self.spacing, self.values,
                                                 (self.x_grid[None, :], self.y_grid[:, None]), method="linear")
        self.gradient = numpy.gradient(self.height, self.x_grid[1] - self.x_grid[0], self.y_grid[1] - self.y_grid[0])


if __name__ == "__main__":
    gradient = WaypointGradient("data/cloud_simplified_2.h5")
