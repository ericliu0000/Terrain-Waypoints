from waypoint import WaypointGenerator
import matplotlib.pyplot as plt
import glob
import os


class Grid:
    def __init__(self) -> None:
        obj = WaypointGenerator("data/cloud_lasground.h5")
        lines = obj.waypoints

        for i in range(1, len(lines)):
            v_average = 0
            h_average = 0

            last, cur = lines[i - 1], lines[i]

            # Make two vairables with the shorter and longer line
            if len(last) < len(cur):
                short, long = last, cur
            else:
                short, long = cur, last

            # Find the closest point in long to each point in short and get distance between two points
            for j in range(len(short)):
                closest = min(long, key=lambda x: abs(x[1] - short[j][1]))

                v_average += ((short[j][0] - closest[0]) ** 2 + (short[j][1] - closest[1]) ** 2) ** 0.5
                # v_average += ((short[j][0] - closest[0]) ** 2 + (short[j][1] - closest[1]) ** 2 + (short[j][2] - closest[2]) ** 2) ** 0.5

                plt.plot([short[j][0], closest[0]], [short[j][1], closest[1]], "r")

            # Go through all points and find horizontal deviation
            for j in range(1, len(cur)):
                h_average += ((cur[j][0] - cur[j - 1][0]) ** 2 + (cur[j][1] - cur[j - 1][1]) ** 2) ** 0.5
                # h_average += ((cur[j][0] - cur[j - 1][0]) ** 2 + (cur[j][1] - cur[j - 1][1]) ** 2 + (cur[j][2] - cur[j - 1][2]) ** 2) ** 0.5

                plt.plot(cur[j][0], cur[j][1], "b.")

            print(h_average / len(cur))
            print(v_average / len(short))
            print()

        plt.imshow(plt.imread("data/site.png"), extent=[950132.25, 950764.18, 798442.81, 800597.99])
        plt.show()


class Reader:
    def __init__(self) -> None:
        graph = plt.axes(projection="3d")

        # open most recent file from output/
        list_of_files = {"output/" + file for file in os.listdir("output/")}
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file) as f:
            lines = f.readlines()[1:]

        # get first line
        first_line = lines[0].split(",")
        last = [float(first_line[0]), float(first_line[1]), float(first_line[2])]
        graph.plot(*last, "gH")
        
        # plot points
        for line in lines[1:]:
            x, y, z = [point[:9] for point in line.split(",")]
            graph.plot([last[0], float(x)], [last[1], float(y)], [last[2], float(z)], "r")
            last = [float(x), float(y), float(z)]

        graph.plot(*last, "m^")

        plt.show()


if __name__ == "__main__":
    Grid()
    # Reader()
