import numpy as np
import shapely

from dataclasses import dataclass
from shapely.geometry import Point, LineString


@dataclass
class Coordinate:
    latitude: float
    longitude: float


def generate_coordinate_trace(coordinates: list[Coordinate]) -> list[Coordinate]:

    trace = []

    for i in range(1, len(coordinates)):
        interpolation = interpolate(coordinates[i-1], coordinates[i])
        trace += interpolation

    return trace


def interpolate(coord1: Coordinate, coord2: Coordinate) -> list[Coordinate]:

    point1 = Point(coord1.latitude, coord1.longitude)
    point2 = Point(coord2.latitude, coord2.longitude)

    line = LineString([point1, point2])

    pts = []
    # the fifth decimal place of a coordinate is roughly representing 1.1m of precision
    precision_level = 0.00001

    # Cartesian distance - since this is GPS, it's in (decimal) degrees
    point_distance = shapely.distance(point1, point2)

    # This will give us as many points as are needed to be in 1.1m increments between the two points
    for div in np.arange(0, point_distance/precision_level, 1):
        pts.extend(line.interpolate(div*0.00001).coords[:])

    coord_list = []
    for point in pts:
        coord_list.append(Coordinate(latitude=point[0], longitude=point[1]))

    return coord_list
