# a file for utility functions
import math
import WavePacketBuilder
from datetime import datetime


def calculate_heading(current_coords, next_coords):
    x_now, y_now = current_coords.split(",")
    x_now = float(x_now)
    y_now = float(y_now)

    x_next, y_next = next_coords.split(",")
    x_next = float(x_next)
    y_next = float(y_next)

    if x_next == x_now and y_next == y_now:
        return "-"
    else:
        if x_next > x_now:
            if y_next > y_now:
                return "SE"
            elif y_next == y_now:
                return "E"
            else:
                return "NE"
        elif x_next == x_now:
            return "S" if y_next > y_now else "N"
        elif x_next < x_now:
            if y_next > y_now:
                return "SW"
            elif y_next == y_now:
                return "W"
            else:
                return "NW"


def calc_speed(current_coords, next_coords):
    x_now, y_now = current_coords.split(",")
    x_now = float(x_now)
    y_now = float(y_now)

    x_next, y_next = next_coords.split(",")
    x_next = float(x_next)
    y_next = float(y_next)

    return math.sqrt(math.pow(x_next-x_now, 2)+math.pow(y_next-y_now, 2)) * 36


def inject_time(bsm):

    # IEEE 1609.2 defines timestamps as an estimate of the microseconds elapsed since
    # 12:00 AM on January 1, 2004
    origin = datetime(2004, 1, 1, 0, 0, 0, 0)

    # get the offset since the origin time in microseconds
    offset = (datetime.now() - origin).total_seconds() * 1000
    time_string = hex(int(math.floor(offset)))
    time_string  = time_string[2:]
    if len(time_string) < 16:
        for i in range(0, 16 - len(time_string)):
            time_string = "0" + time_string
    time_string = "\\x" + "\\x".join(time_string[i:i + 2] for i in range(0, len(time_string), 2))
    bsm = bsm.replace("\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0", time_string)

    return bsm.replace("\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0\\xF0\\xE0", time_string)


class Utility:
    
    # For the local vehicle, full WSMs are unnecessary as there is no communication over the SDR
    def build_local_queue(self, trace_file_path):
        with open(trace_file_path) as infile:
            coordinates = infile.readlines()
        messages = []
        for i in range(0, len(coordinates)-2):
            messages.append("99," + coordinates[i].replace("\n", "") +
                            "," +
                            calculate_heading(coordinates[i], coordinates[i + 1]) +
                            "," +
                            str(calc_speed(coordinates[i], coordinates[i + 1])))
        return messages
        
    # takes in two strings "x,y" from a trace file
    # returns one- or two-character string indicating heading

    # takes in two strings "x,y" from a trace file
    # returns speed in km/hr

