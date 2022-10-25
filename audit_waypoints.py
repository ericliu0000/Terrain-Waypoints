import os

import matplotlib.pyplot as plt
import numpy

import constants
from calculate_gradient import WaypointGradient
from waypoint import WaypointGenerator


class Grid:
    def __init__(self) -> None:
        obj = WaypointGenerator(constants.FILE)
        lines = obj.waypoints

        for i in range(1, len(lines)):
            v_average = 0
            h_average = 0

            last, cur = lines[i - 1], lines[i]

            # Split up longer and shorter line
            if len(last) < len(cur):
                short, long = last, cur
            else:
                short, long = cur, last

            # Find the closest point in long to each point in short and get distance between two points
            for j in range(len(short)):
                closest = min(long, key=lambda x: abs(x[1] - short[j][1]))
                v_average += ((short[j][0] - closest[0]) ** 2 + (short[j][1] - closest[1]) ** 2) ** 0.5
                plt.plot([short[j][0], closest[0]], [short[j][1], closest[1]], "r")

            # Go through all points and find horizontal deviation
            for j in range(1, len(cur)):
                h_average += ((cur[j][0] - cur[j - 1][0]) ** 2 + (cur[j][1] - cur[j - 1][1]) ** 2) ** 0.5
                plt.plot(cur[j][0], cur[j][1], "b.")

            print(h_average / len(cur))
            print(v_average / len(short))
            print()

        plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])
        plt.show()


class Grid3:
    length = 500

    def __init__(self) -> None:
        # Read and rasterize the site data
        points = WaypointGenerator(constants.FILE)
        obj = WaypointGradient(constants.FILE)
        x, y = obj.x_grid, obj.y_grid
        z = obj.height
        x, y = numpy.meshgrid(x, y)

        x_min = constants.LEFT_BOUND
        y_min = 798900
        z_min = constants.Z_FILTER

        graph = plt.axes(projection="3d")
        graph.plot_surface(x, y, z, linewidth=0, cmap=plt.cm.terrain)

        # Label and scale axes to cube
        graph.set_xlabel("Easting (x)")
        graph.set_ylabel("Northing (y)")
        graph.set_zlabel("Altitude (z)")

        graph.set_xlim(x_min, x_min + self.length)
        graph.set_ylim(y_min, y_min + self.length)
        graph.set_zlim(z_min, z_min + self.length)

        # Plot line between original point and waypoint
        for r1, r2 in zip(points.values, points.waypoints):
            for p1, p2 in zip(r1, r2):
                plt.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], "r")

        plt.show()


class Reader:
    def __init__(self) -> None:
        main = plt.figure(figsize=(10, 5))
        graph = main.add_subplot(111, projection="3d")

        # Open most recent file from output/ and remove header
        list_of_files = {"output/" + file for file in os.listdir("output/")}
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file) as f:
            lines = f.readlines()

        header = lines.pop(0)

        if "Latitude" in header:
            graph.set_xlabel("Latitude")
            graph.set_ylabel("Longitude")
        elif "Easting" in header:
            graph.set_xlabel("Easting (ft)")
            graph.set_ylabel("Northing (ft)")

        graph.set_zlabel("Altitude (ft)")

        # Pull out first point
        first_line = lines[0].split(",")
        last = [float(first_line[1]), float(first_line[2]), float(first_line[3])]
        graph.plot(*last, "gH", ms=10)

        # Plot the points
        for line in lines[1:int(len(lines) / 2)]:
            _, x, y, z = [point[:9] for point in line.split(",")]
            graph.plot([last[0], float(x)], [last[1], float(y)], [last[2], float(z)], "r")
            last = [float(x), float(y), float(z)]
        for line in lines[int(len(lines) / 2):]:
            _, x, y, z = [point[:9] for point in line.split(",")]
            graph.plot([last[0], float(x)], [last[1], float(y)], [last[2], float(z)], "b")
            last = [float(x), float(y), float(z)]

        graph.plot(*last, "m^", ms=10)
        plt.show()


class Ruler:
    def __init__(self) -> None:
        list_of_files = {"output/" + file for file in os.listdir("output/")}
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file) as f:
            lines = f.readlines()

        if "Latitude" in lines.pop(0):
            print("Cannot measure distance on lat/long/feet data")
            return

        # Pull out first point
        total = 0
        last = [float(point) for point in lines[0][:-1].split(",")[1:]]
        slopes = []

        # Calculate distance between first and next point and slope
        for line in lines[1:]:
            _, x, y, z = [float(point) for point in line[:-1].split(",")]
            total += ((x - last[0]) ** 2 + (y - last[1]) ** 2 + (z - last[2]) ** 2) ** 0.5

            # Get slope between XY and Z
            slope = (z - last[2]) / (((x - last[0]) ** 2 + (y - last[1]) ** 2) ** 0.5)
            print(f"XY diff {(x - last[0]) ** 2 + (y - last[1]) ** 2} Z diff {z - last[2]} Slope {slope}")
            slopes.append(slope)    

            last = [x, y, z]

        print(f"Total length: {total}")
        counts, bins = numpy.histogram(slopes)
        plt.hist(bins[:-1], bins, weights=counts)
        plt.show()

        


if __name__ == "__main__":
    # Grid()
    # Grid3()
    # Reader()
    Ruler()
