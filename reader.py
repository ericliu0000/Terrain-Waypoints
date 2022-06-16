"""
Read data to latitude, longitude, and elevation
"""
import pyproj
import pandas
import numpy


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


class PlaneReader:
    spacing = []
    values = []

    def __init__(self, file):
        with open(file) as f:
            # Read x, y, z points
            last = 0
            row = [[], []]

            for line in f.readlines():
                line = line.replace("\n", "")
                x, y, z = line.split()

                # If y value has advanced, add row to the list
                if y != last:
                    if len(row[0]) != 0:
                        self.spacing.append(row[0])
                        self.values.append(row[1])
                    row = [[], []]

                # Add values
                row[0].append([float(x), float(y)])
                row[1].append(float(z))
                last = y

            self.spacing.append(row[0])
            self.values.append(row[1])


class PandasReader:
    points = []
    array = []

    def __init__(self, file):
        self.points = pandas.read_hdf(file, "test").to_numpy()
        # self.points.to_hdf("data/ncsutest.h5", "test")

        # only works if data is square
        self.points = numpy.reshape(self.points, (1600, 1600, 3))
        print(self.points)
        """        
        last = 0
        row = []

        for point in self.points:
            # If y value has advanced, add row to the list
            # print(point)
            if point[1] != last:
                if len(row) != 0:
                    self.array.append(row)
                row = []

            # Add values
            row.append((point[0], point[1], point[2]))
            last = point[1]
        """


if __name__ == "__main__":
    reader = PandasReader("data/ncsutest.h5")
    # print(reader.spacing[0], "\n", reader.values[0])
