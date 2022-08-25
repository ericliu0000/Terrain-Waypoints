PROJECTION: str = "+proj=lcc +lat_0=33.75 +lon_0=-79 +lat_1=36.1666666666667 +lat_2=34.3333333333333 +x_0=609601.22 " \
                  "+y_0=0 +datum=NAD83 +units=m no_defs +ellps=GRS80 +towgs84=0,0,0 "
OUTPUT_HEADER: str = "Index,Latitude,Longitude,Altitude\n"

CLEARANCE: float = 100.0
LEFT_BOUND: float = 950310.0
RIGHT_BOUND: float = 950600.0
Z_FILTER: float = 3420.0

GLOBAL_SCALE: float = 1.0
METERS_TO_FEET: float = 3.048
CAMERA_H: float = 3.0 * METERS_TO_FEET * GLOBAL_SCALE
CAMERA_V: float = 2.3 * METERS_TO_FEET * GLOBAL_SCALE

FILE = "data/cloud_lasground.h5"


def upper(coord):
    return min((6.0268 * (coord - 950288) + 799669), 800344)


def lower(coord):
    return max((-16.8125 * (coord - 950304) + 799400), (-3.6393 * (coord - 950304) + 799400), 798956)
