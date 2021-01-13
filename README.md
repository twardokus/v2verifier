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
Running V2Verifier requires a minimum of two USRP software-defined radios (B210 or N210 with 5.9 GHz daughterboards) and at least one PC capable of running Ubuntu 18.04. A virtual machine may be used, but is not recommended. We further recommend using two PCs with one USRP connected to each PC for best results.


## Installing V2Verifier
On each Ubuntu PC, you must install the following dependencies:

	sudo apt install -y git cmake libuhd-dev uhd-host swig libgmp3-dev python-pip python3-pip python3-tk python3-pil python3-pil.imagetk gnuradio

Since V2Verifier incorporates open-source code from the [WiME project](https://www.wime-project.net/), 
you need to install two components from that project.  
    
    cd ~
    git clone https://github.com/bastibl/gr-foo.git
    cd gr-foo
    git checkout maint-3.7
    mkdir build
    cd build
    cmake ..
    make
    sudo make install
    sudo ldconfig

	cd ~
	git clone git://github.com/bastibl/gr-ieee802-11.git
	cd gr-ieee802-11
	git checkout maint-3.7
	mkdir build
	cd build
	cmake ..
	make
	sudo make install
	sudo ldconfig
		
Next, install some Python 3 libraries.

	pip3 install fastecdsa scapy
	pip3 install -U pyyaml

## Running V2Verifier
Connect one USRP to each PC. On both PCs, launch GNURadio with the command `gnuradio-companion` from a terminal. On one PC, open the `wifi_tx.grc` file from the `v2verifier/grc` project subdirectory. On the other PC, open the `wifi_rx.grc` file from the same subdirectory. Click the green play button at the top of GNURadio to launch the flowgraphs on both PCs.

On the PC running the `wifi_rx.grc` flowgraph, open a new terminal. Navigate to the V2Verifier directory and run the command `sudo python3 main.py local` to launch the receiver program with GUI support. On the othe PC, open a new terminal, vaigate to the project directory and run the command `sudo python3 main.py remote` to begin sending BSMs from that PC to the other. You should see red vehicles begin to appear on the GUI, indicating that messages are being received and processed by the receiver program.

## Running a reactive jamming attack on V2Verifier
To run a ractive jamming attack, you will need a third USRP capable of dual-antenna operation (i.e., with independent antenna chains). We used a USRP N210 + UBX40 daughterboard with dual 5.9 GHz antennas in our experimentation. Note in particular the USRP B210 will *not* work as the attacker due to a lack of dual antenna chains. You should also have a third PC with Ubuntu 18.04; alternatively, you can run the two devices set up in the steps above off of one PC and have the attacker run on the second. It is not recommended to connect the attacker USRP to a PC that is also running another USRP as this may cause too much latency with the attacker's USRP for the attack to be effective.

To run a reactive jamming attack, begin by following the instructions under "Running V2Verifier" to launch the environment with no attacker. On the PC connected to the attacker USRP, open the `reactive_jammer.grc` flowgraph in GNURadio. Run the flowgraph. 

Looking at the V2Verifier GUI (particularly at the packet statistics in the upper-right corner) you should see a dramatic decrease in all metrics when the jammer is activated. This is because the jammer is causing signature verification failures and/or unrecoverable packet errors in received BSMs, effecting a denial-of-service attack against the emulated V2V environment.


