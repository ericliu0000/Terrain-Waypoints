import datetime

import pyproj

PROJECTION: str = "+proj=lcc +lat_0=33.75 +lon_0=-79 +lat_1=36.1666666666667 +lat_2=34.3333333333333 +x_0=609601.22 " \
                  "+y_0=0 +datum=NAD83 +units=m no_defs +ellps=GRS80 +towgs84=0,0,0 "
OUTPUT_HEADER: str = "Index,X,Y,Altitude\n"
OUTPUT_HEADER_L: str = "Index,Latitude,Longitude,Altitude\n"

CLEARANCE: float = 100.0
LEFT_BOUND: float = 950310.0
RIGHT_BOUND: float = 950600.0
Z_FILTER: float = 3390.0

GLOBAL_SCALE: float = 3.0
METERS_TO_FEET: float = 3.048
CAMERA_H: float = 3.0 * METERS_TO_FEET * GLOBAL_SCALE
CAMERA_V: float = 2.3 * METERS_TO_FEET * GLOBAL_SCALE

FILE = "data/cloud_lasground.h5"


def upper(coord):
    return min((6.0268 * (coord - 950288) + 799669), 800344)


def lower(coord):
    return max((-16.8125 * (coord - 950304) + 799400), (-3.6393 * (coord - 950304) + 799400), 798956)


def export(waypoints) -> str:
    """Export the waypoints to a file (EPSG 32119)."""

    with open(f"output/{datetime.datetime.now()}.csv", "w") as file:
        file.write(OUTPUT_HEADER)
        count = 0

        for row in waypoints:
            for point in row:
                count += 1
                file.write(f"{count},{point[0]},{point[1]},{point[2]}\n")

        return f"Exported {count} waypoints to {file.name}"


def export_latlong(waypoints) -> str:
    """Export the waypoints to a file (EPSG 4326)."""

    p = pyproj.Proj(PROJECTION)
    with open(f"output/{datetime.datetime.now()}_latlong.csv", "w") as file:
        file.write(OUTPUT_HEADER_L)
        count = 0

        for row in waypoints:
            for point in row:
                count += 1
                x, y = p(point[0], point[1], inverse=True)
                file.write(f"{count},{x},{y},{point[2]}\n")

        return f"Exported {count} waypoints to {file.name}"
