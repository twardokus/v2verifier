# v2v-capstone
Repo to hold capstone project dev work

## Overview
__TO BE ADDED__
We do not include specific python library dependencies as this list is likely to change. Simply install the standard Ubuntu packaged version of any Python libraries that are errored as missing, and you should be good to go. We assume if you are at this level of software design, you should understand how to use Pip to quickly install python libraries.

## Requirements
Hardware:
- Two USRP N210 software-defined radios with a 40 MHz daughterboard installed on each
- Two PCs running some version of Linux (note: project has been tested only on Ubuntu 18.04 and Ubuntu 19.10. Use other distros at your own risk)

Software:
- GNURadio v3.7
- UHD drivers installed on each PC
- python 2.7 AND python 3.x installed on both PCs

## How to run this project
We assume you have set up the USRPs with the appropriate drivers and are able to communicate with them from the PCs they are respectively connected to.

On each PC:
1. Clone the repository.
2. Create a directory with the cloned repo to hold your crypto keys.
3. Edit `generate-p256-keypair.py` and update the public/private key paths
4. Run `python generate-p256-keypair.py`
5. On the PC attached to the "receiver" USRP, copy the public key from the other PC (the "transmitter") and place somewhere memorable on the local disk.
6. Edit `receiver.py` and update the path to the other PC's public key

At this point you are ready to run the codes. You may update the `traces.csv` file with your own vehicle traces if desired, or use the provided data. 

On the receiver:
_You will need to have two terminal windows open for this machine._
1. In the first terminal window, `cd GUI` within the cloned repo and execute `python3 App.py`
2. In the second terminal window, execute `sudo python rxMain.py`

On the transmitter:
1. Execute `python txMain.py`

This project was part of an undergraduate capstone and so, while fully functional, it is not polished. Good luck, and enjoy.
