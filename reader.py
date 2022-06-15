"""
Read data to latitude, longitude, and elevation
"""
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

                # Add values (from survey feet to meters)
                row.append((float(x) * 1200 / 3937, float(y) * 1200 / 3937, float(z)))
                last = y

            self.points.append(row)


if __name__ == "__main__":
    reader = XYZReader("data/ncsutest.txt")
    print(reader.points[0])
