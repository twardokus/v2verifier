# this is the main execution file for the "local vehicle"

import yaml
from v2verifier.LocalVehicle import LocalVehicle

with open("init.yml", "r") as confFile:
    config = yaml.load(confFile,Loader=yaml.FullLoader)
    
