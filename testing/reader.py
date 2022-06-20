"""
Read data to latitude, longitude, and elevation
"""
import numpy
import pandas
import pyproj


class XYZReader:
    points = []
    transformer = pyproj.Transformer.from_proj("epsg:32119", "epsg:4326")

    def __init__(self, file):
        with open(file) as f:
            # Read x, y, z points
            last = 0
            row = []

            for line in f.readlines():
                line = line.replace("\n", "")
                x, y, z = line.split()

                # If y value has advanced, add row to the list
                if y != last:
                    if len(row) != 0:
                        self.points.append(row)

                    row = []

                # Add values
                row.append((float(x), float(y), float(z)))
                last = y

            self.points.append(row)


class PandasReader:
    points = []
    array = []

    def __init__(self, file):
        self.points = pandas.read_hdf(file, "a").to_numpy()

        # only works if data is square
        self.points = numpy.reshape(self.points, (1600, 1600, 3))
        self.spacing = self.points[..., 0:2]
        self.values = self.points[..., 2]


class ConvertHDF:
    def __init__(self, file, out):
        # self.points = pandas.read_csv(file)
        self.points = pandas.read_csv(file, delimiter=" ", header=None)
        self.points.to_hdf(out, "a")


if __name__ == "__main__":
    # print("a")
    ConvertHDF("data/cloud_lasground.txt", "data/cloud_lasground.h5")
    # print(reader.spacing[0], "\n", reader.values[0])
