# v2verifier
V2Verifer is an open-source project dedicated to wireless experimentation
focused on the security of vehicle-to-vehicle (V2V) communications.
Included are implementations of:
- security features from the IEEE 1609.2 standard for V2V security
- WAVE Short Message Protocol (IEEE 1609.3)
-  Dedicated Short Range Communication (DSRC) - adapted from 
the [WiME Project's](http://dx.doi.org/10.1109/TMC.2017.2751474)
IEEE 802.11p transceiver 

## Requirements
This code base is intended to be used with two or more software-defined
radios (SDRs). Our development and testing is done with USRP N210 and B210
SDRs from Ettus Research.

Python version 3.6+ is required to run this project. The following
libraries are specifically required and can be installed using Pip:

- fastecdsa
- scapy
- tkinter

Note that this list may not be comprehensive as the project is under
continuous expansion.

The files for transmitting and receiving are set up for GNURadio version
3.7. 

To run the project as-is, clone the repository on two PCs (each connected
to one USRP). In GNURadio, open `wifi_tx.grc` on one PC and `wifi_rx.grc`
on the other. Run both flowgraphs. Then, in a terminal on each PC,
navigate to the cloned repository. On one PC, run 
`sudo python3 local_main.py`. This will start the receiver with the 
graphical user interface. On the other PC, run 
`sudo python3 remote_main.py`. This will run the initial configuration
with pre-configured parameters.

Additional documentation and tutorials coming soon!

Copyright (c) 2020 Geoff Twardokus et al. (see LICENSE for all authors)