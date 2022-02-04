# V2Verifier

V2Verifer is an open-source testbed for experimental evaluation of security in
vehicle-to-vehicle (V2V) communication. V2Verifier supports a broad range of 
experimentation with V2V technologies and security protocols using a 
combination of software-defined radios (e.g., USRPs) and commercial V2V
equipment. Among other features, V2Verifier includes implementations of:
- Security features from the IEEE 1609.2 standard for V2V security, including
message signing and verification and V2V certificates
- WAVE Short Message Protocol (IEEE 1609.3)
- Dedicated Short Range Communication (DSRC) - adapted from 
the [WiME Project's](http://dx.doi.org/10.1109/TMC.2017.2751474)
IEEE 802.11p transceiver
- Cellular Vehicle-to-Everything (C-V2X) - based on the 
[srsRAN](https://github.com/srsRAN/srsRAN) project (formerly
srsLTE)

Check out our 
[YouTube page](https://www.youtube.com/channel/UC5lY5D4KYgfKu3FXtfjHP7A)
for some of our past projects and publications that made use of V2Verifier!

V2Verifier is developed and maintained in the [Wireless and IoT Security 
and Privacy (WISP)](https://www.rit.edu/wisplab/) lab at Rochester Institute
of Technology's [Global Cybersecurity Institute](
https://rit.edu/cybersecurity).

### Citing V2Verifier
If you use V2Verifier or any of its components in your work, please cite 
[our paper](https://github.com/twardokus/v2verifier/wiki/Publications) from 
IEEE ICC 2021. Additional publications involving V2Verifier are listed on the 
same page.

## Requirements
V2Verifier is designed to be run with software-defined radios (SDRs); 
specifically, we recommend either the USRP B210 or, preferably, the USRP N210, 
both available from Ettus Research. When using N210s, 6 GHz daughterboards 
(e.g., UBX 40) are required for each N210 device.

If you do not have access to SDRs, V2Verifier can also be run as a pure 
simulation environment that only requires a modern PC to run. With or without
SDRs, we strongly discourage the use of virtual machines as this may incur 
testbed-breaking latency. Ubuntu 18.04 is the only officially supported 
operating system at this time.

## Installing V2Verifier
On each Ubuntu PC, you must install the following dependencies:

	sudo apt install -y git cmake libuhd-dev uhd-host swig libgmp3-dev python3-pip python3-tk python3-pil 
	python3-pil.imagetk gnuradio
	
You may alternately choose to use Pip to install all required packages from the included `requirements.txt` file.

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
		
Next, install and/or upgrade some Python 3 libraries.

	pip3 install -U fastecdsa pyyaml eel folium pynmea2

## Running V2Verifier
Connect one USRP to each PC. On both PCs, launch GNURadio with the command `gnuradio-companion` from a terminal. 
On one PC, open the `wifi_tx.grc` file from the `v2verifier/grc` project subdirectory. On the other PC, open 
the `wifi_rx.grc` file from the same subdirectory. Click the green play button at the top of GNURadio to launch the 
flowgraphs on both PCs. You will need to configure the communication options (e.g., bandwith, frequency) to suit your 
needs. The default is a 10 MHz channel on 5.89 GHz.

On each PC, navigate to the v2verifier directory. For the receiver, run the command

    python3 v2verifier.py receiver -t {dsrc cv2x} [-g {web tk}] [--test]

to launch the receiver (include the `-g` option for GUI support). For the transmitter, run the command

    python3 v2verifier.py transmitter [--test]
    
to begin transmitting messages. See the command-line help (`python3 v2verifier.py --help`) for information about the
optional arguments noted for each command.

*Note that V2Verifier also supports C-V2X communication, but this requires equipment capable of both cellular
communication and GPS clock synchronization (e.g., USRP B210 w/ GPSDO or 
[Cohda Wireless MK6c](https://cohdawireless.com/solutions/hardware/mk6c-evk/)) as well as access to either an outdoor
testing environment or synthesized GPS source.*

## Replay attack with V2Verifier
**Note - these instructions apply to versions of V2Verifier through the beta release of version 2.0. While updates are in progress, please ensure you use an appropriate release of V2Verifier as these instructions will not work with release 2.0**

Conducting a replay attack requires three USRPs and three PCs. Note that these instructions apply only to DSRC at present.
One USRP, which will be used to conduct the attack, will require two antennas.

Set up two PCs as above and run the normal transmitter and receiver programs. Make sure to use the `-g` option with 
the `local` program to launch the receiver GUI.

    python3 ./main.py [local | remote] dsrc [-g]
    
On the third PC, connected to the USRP with two antennas, open the `wifi_rx.grc` and `wifi_tx.grc` flowgraphs in 
GNURadio. Also, open a terminal and navigate to the `replay_attack` directory in the V2Verifier directory.
- Run the `wifi_rx.grc` flowgraph
- Switch to the terminal and run `python3 ./replay_attack.py <seconds_to_collect>`
- When the script prompts to press Enter, *wait!* Go back to GNURadio, stop the `wifi_rx.grc` flowgraph and run 
the `wifi_tx.grc` flowgraph
- Return to the terminal and press Enter. The attacker will begin replaying messages.
- Look at the receiver you started at the beginning. You should see the effects of the replay attack (e.g., warning 
messages in yellow text on the message feed) on the GUI.
