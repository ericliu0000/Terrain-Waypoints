from waypoint import WaypointGenerator
import matplotlib.pyplot as plt

obj = WaypointGenerator("data/cloud_lasground.h5")
lines = obj.waypoints

for i in range(1, len(lines) - 1):
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
