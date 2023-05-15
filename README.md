# V2Verifier

****Important** - this version of V2Verifier (v3.0.0) is a _preliminary_ release of V2Verifier 3.0. 
As we await bug fixes in third-party open-source projects that V2Verifier relies on
for C-V2X sidelink communication, **this version of V2Verifier temporarily does 
not support C-V2X**. We thank you for your patience as we work towards resolving this
issue.**

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
- ~~Cellular Vehicle-to-Everything (C-V2X) - based on the 
[srsRAN](https://github.com/srsRAN/srsRAN) project (formerly
srsLTE)~~ (temporarily not supported)

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

## Equipment Requirements
V2Verifier is designed for over-the-air experiments with software-defined radios 
(SDRs).
For C-V2X, you _**must**_ use SDRs with GPSDO modules installed. We recommend
the USRP B210 and TCXO GPSDO module from Ettus Research (we have not tested and 
do not officially support the use of other SDRs for C-V2X).
For DSRC, you may use USRP B210s (GPSDO not required for DSRC) or, preferably, 
USRP N210s (also available from Ettus Research). If you are using N210s, a 6 GHz 
daughterboard (e.g., UBX 40) is required for each N210 device.

If you do not have access to SDRs, V2Verifier can also be run as a pure 
simulation environment that only requires a modern PC to run. With or without
SDRs, we strongly discourage the use of virtual machines as this may incur 
testbed-breaking latency. Ubuntu 20.04 is currently the only supported
operating system. **Windows operating systems are not supported.**

## Installing V2Verifier

Installation consists of two parts.

### Part 1 - V2V Protocols
Follow the instructions for DSRC, C-V2X, or both to install the software needed
for your PC to communicate with your software-defined radios and send V2V
messages over the air.

#### C-V2X

V2Verifier's implementation of C-V2X sidelink communication is based on the
open-source srsRAN project.

_C-V2X support has been temporarily removed as we await bug fixes in third-party code
that V2Verifier relies on. Thank you for your patience as we work to restore this
functionality as soon as possible._

#### DSRC

V2Verifier's implementation of DSRC is based on the open-source GNURadio 
and WiME Project implementation of IEEE 802.11p.

[GNURadio](https://github.com/gnuradio/gnuradio) version 3.10 is required to run
DSRC experiments in V2Verifier. Additionally, GNURadio modules from the 
[WiME project](https://www.wime-project.net/) are required. Install GNURadio
as well as the required WiME modules with the following commands. If you
encounter any errors, please visit the GNURadio project on GitHub for their most recent
installation instructions and troubleshooting guide.

    pip install pybombs
    pybombs auto-config
    pybombs recipes add-defaults
    pybombs prefix init ~/gr-3.10 -R gnuradio-default

To finish configuring the environment and ensure installation was successful, execute the following commands to 
run GNURadio Companion.

    source ~/gr-3.10/setup_env.sh
    gnuradio-companion

Now, install the WiME project code. You will need to install from source, as the `pybombs` installation method (e.g., `pybombs install gr-foo`) will likely fail due to Swig issues in GNURadio 3.10.

    cd ~
    git clone https://github.com/bastibl/gr-foo.git
    cd gr-foo
    git checkout maint-3.10
    mkdir build && cd build
    cmake ../
    make
    sudo make install
    sudo ldconfig
    
    cd ~
    git clone https://github.com/bastibl/gr=ieee802-11.git
    cd gr-ieee802-11
    git checkout maint-3.10
    mkdir build && cd build
    cmake ../
    make
    sudo make install 
    sudo ldconfig

You can confirm everything installed correctly by launching GNURadio Companion and opening the flowgraph file at `~/gr-ieee802-11/examples/wifi-loopback.grc`. If 
you encounter any errors, some of the above commands did not work correctly. Do not proceed until you have fixed any issues running the example flowgraph.

### Part 2 - V2Verifier

Now that you have installed the communication software, you can install V2Verifier. 
Begin by installing several dependencies:

	sudo apt install -y git cmake libuhd-dev uhd-host swig libgmp3-dev python3-pip python3-tk python3-pil 
	python3-pil.imagetk 

If you have not already cloned the V2Verifier repository, do so with the commands

    cd ~
    git clone https://github.com/twardokus/v2verifier.git

Move into the V2Verifier directory and build the project using the standard CMake
build process:

    cd v2verifier
    mkdir build
    cd build
    cmake ../
    make

If you have missed any dependencies, CMake will warn you at this point.
Once V2Verifier is built, proceed to the next section for instructions on how to
run experiments in V2Verifier.

Finally, download the ZIP file for the latest stable release of V2Verifier, extract the project, and you are ready 
to start using V2Verifier!

## Running V2Verifier

Before running V2Verifier, connect one USRP (with appropriate antennas) to each Ubuntu PC.
Assuming you have two PCs with one USRP each, designate one USRP as the "receiver" and the other
as the "transmitter." In this configuration, the receiver will show you how a single vehicle 
responds to V2V transmissions (e.g., using a GUI) while the transmitter can generate V2V
traffic for up to ten vehicles. You can specify the number of vehicles by changing the relevant
parameter in `config.json`.

On each PC, begin by launching the C-V2X or DSRC code (follow 
the respective instructions below) to run in the background and manage your SDR transmitting
or receiving. Then, on each PC, `cd` into the `build` directory. For the receiver, run the command

    ./src/v2verifier dsrc receiver [--test] [--gui]

For the transmitter, run the command

    ./src/v2verifier dsrc transmitter [--test]

See the command-line help (`./v2verifier -h`) for optional arguments. You should not use the `--test`
option unless you are not using SDRs (this option allows you to run transmitter and receiver on a 
single PC with communication via network socket). Use `--gui` on the receiver if you want to use 
a graphical interface on the receiver (see additional instructions for GUIs below).

### Radio layer: C-V2X
*Note C-V2X communication requires equipment capable of both cellular
communication and GPS clock synchronization (e.g., USRP B210 w/ GPSDO or
[Cohda Wireless MK6c](https://cohdawireless.com/solutions/hardware/mk6c-evk/)) as well as access to either an outdoor
testing environment or synthesized GPS source.*

**C-V2X support has been temporarily removed as we await bug fixes in third-party code
that V2Verifier relies on. Thank you for your patience as we work to restore this
functionality as soon as possible.**


### Radio layer: DSRC

On both PCs, launch GNURadio with `pybombs run gnuradio-companion`. 
On one PC, open the `wifi_tx.grc` file from the `v2verifier/grc` project subdirectory. On the other PC, open 
the `wifi_rx.grc` file from the same subdirectory. Click the green play button at the top of GNURadio to launch the 
flowgraphs on both PCs. You will need to configure the communication options (e.g., bandwith, frequency) to suit your 
needs. The default is a 10 MHz channel on 5.89 GHz.

### Using GUIs
V2Verifier currently offers two graphical 
interfaces. The first is a web-based interface that interacts with Google Maps. 
To use this GUI, you will need to purchase a Google Maps API key through Google 
Cloud services and create `config.js` file in the `web` directory of V2Verifier
(some familiarity with JavaScript is helpful). Please contact us for assistance 
if you want to use this GUI.

Our second interface is based on
TkGUI. To use this option, open a separate terminal window before running any 
`v2verifier` commands above and run `python3 tkgui_execute.py` to launch the 
TkGUI interface as a separate process. 

We encourage you to open a GitHub issue
with any questions or problems using either graphical interface.
