from waypoint import WaypointGenerator
import matplotlib.pyplot as plt

obj = WaypointGenerator("data/cloud_lasground.h5")
lines = obj.waypoints

for i in range(1, len(lines) - 1):
    v_average = 0
    h_average = 0

    last, cur = lines[i - 1], lines[i]

    for j in range(1, len(cur)):
        # Add 3d pythagorean distance to horizontal points
        h_average += ((cur[j][0] - cur[j - 1][0]) ** 2 + (cur[j][1] - cur[j - 1][1]) ** 2) ** 0.5
        # h_average += ((cur[j][0] - cur[j - 1][0]) ** 2 + (cur[j][1] - cur[j - 1][1]) ** 2 + (cur[j][2] - cur[j - 1][2]) ** 2) ** 0.5

    # Make two vairables with the shorter and longer line
    if len(last) < len(cur):
        short, long = last, cur
    else:
        short, long = cur, last

    # Find the closest point in long to each point in short and get distance between two points
    for j in range(len(short)):
        closest = min(long, key=lambda x: abs(x[1] - short[j][1]))

        # Add distance from short to closest by means of 3d pythagorean distance
        v_average += ((short[j][0] - closest[0]) ** 2 + (short[j][1] - closest[1]) ** 2) ** 0.5
        # v_average += ((short[j][0] - closest[0]) ** 2 + (short[j][1] - closest[1]) ** 2 + (short[j][2] - closest[2]) ** 2) ** 0.5


    print(h_average / len(cur))
    print(v_average / len(short))
    print()

# plt.show()
