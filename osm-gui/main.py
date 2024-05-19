import json
import pandas as pd

from pprint import pprint

from Vehicle import BSM, Vehicle
from Vehicle import *
from Utility import *


def main():

    Vehicle.test_mode = True

    v = Vehicle(8000, 9999, 'coordinate_trace.csv')
    time.sleep(5)
    v2 = Vehicle(8001, 9999, 'coordinate_trace.csv')



if __name__ == '__main__':
    main()
