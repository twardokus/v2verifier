# 43.0923826,-77.6704622
# 43.0929162,-77.6575104

import geopy.distance

from math import floor

def get_gps_trace(start_coord: tuple, end_coord: tuple, speed_kph: float) -> list:

    total_distance_km = geopy.distance.distance(start_coord, end_coord).km
    travel_time_ms = (total_distance_km / speed_kph) * 3600000

    num_bsm_intervals = floor(travel_time_ms / 100)

    lat_diff = end_coord[0] - start_coord[0]
    lon_diff = end_coord[1] - start_coord[1]

    lat_diff_step = lat_diff/num_bsm_intervals
    lon_diff_step = lon_diff/num_bsm_intervals

    trace = [start_coord]

    for i in range(1, num_bsm_intervals):
        trace.append((start_coord[0] + lat_diff_step * i, start_coord[1] + lon_diff_step * i))

    return trace
    

if __name__=="__main__":

    c1 = (43.0923826,-77.6704622)
    c2 = (43.0929162,-77.6575104)


    trace = get_gps_trace(c1, c2, 36)

    with open('test_trace.csv', 'w') as outfile:
        for i in range(len(trace)):
            outfile.write(str(trace[i][0]) + "," + str(trace[i][1]) + "," + "0,0,0\n")
