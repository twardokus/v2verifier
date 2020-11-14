import os
import yaml
from threading import Lock, Thread
from socket import socket
from Receiver import Receiver
from LocalVehicle import LocalVehicle
from GUI import GUI
import tkinter as tk

with open("init.yml", "r") as confFile:
    config = yaml.load(confFile,Loader=yaml.FullLoader)

if __name__ == "__main__":
    
    if os.geteuid() != 0:
        print("Error - you must be root! Try running with sudo")
        exit(1)

    root = tk.Tk()
    gui = GUI(root)
    gui.run_gui_receiver()
    print("GUI Initialized...")
    
    s2 = socket()
    s2.connect(('127.0.0.1',6666))
    
    lock = Lock()
    
    receiver = Receiver()
    
    listener = Thread(target=receiver.run_receiver, args=(s2, lock,))
    listener.start()
    print("Listener running...")
    
    lv = LocalVehicle(config["localConfig"]["tracefile"])
    
    local = Thread(target=lv.start, args=(s2,lock,))
    local.start()
    
    root.mainloop()