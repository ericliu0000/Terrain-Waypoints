from waypoint import WaypointGenerator
import matplotlib.pyplot as plt

obj = WaypointGenerator("data/cloud_lasground.h5", list(range(3400, 3600, 6)))
lines = obj.waypoints

for i in range(1, len(lines) - 1):
    average = 0
    last, cur = lines[i - 1], lines[i]

    # Make two vairables with the shorter and longer line
    if len(last) < len(cur):
        short, long = last, cur
    else:
        short, long = cur, last

    # Find the closest point in long to each point in short and get distance between two points
    for j in range(len(short)):
        closest = min(long, key=lambda x: abs(x[1] - short[j][1]))
        plt.plot([short[j][0], closest[0]], [short[j][1], closest[1]], "r")
        average += ((short[j][0] - closest[0]) ** 2 + (short[j][1] - closest[1]) ** 2) ** 0.5

    print(average / len(short))

plt.show()
