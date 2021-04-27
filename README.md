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

	sudo apt install -y git cmake libuhd-dev uhd-host swig libgmp3-dev python3-pip python3-tk python3-pil python3-pil.imagetk gnuradio

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

	pip3 install fastecdsa
	pip3 install -U pyyaml

## Running V2Verifier
Connect one USRP to each PC. On both PCs, launch GNURadio with the command `gnuradio-companion` from a terminal. On one PC, open the `wifi_tx.grc` file from the `v2verifier/grc` project subdirectory. On the other PC, open the `wifi_rx.grc` file from the same subdirectory. Click the green play button at the top of GNURadio to launch the flowgraphs on both PCs. You will need to configure the communication options (e.g., bandwith, frequency) to suit your needs. The default is a 10 MHz channel on 5.89 GHz.

On each PC, navigate to the v2verifier directory and run `python3 main.py [local | remote] [dsrc | cv2x ]` (leave off the options for usage help) to execute the transmit and receiver V2V programs.

