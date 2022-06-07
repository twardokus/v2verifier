# Changelog
Notable changes to this project will be tracked here. Additions, deprecations, etc. are described per version release.

## [3.0.0] - 2022-06
Version 3.0.0, a preliminary release, is a major overhaul of the testbed. Most prominently, V2Verifier is now a C++ project. Several factors 
informed the change from Python to C++; most significantly, V2Verifier code now runs at speeds much closer to real
V2V software and therefore more accurately reflects real-world performance (e.g., ECDSA verifications are performed)
at a more realistic pace. 

Version 3.0.1 will be released in the near future to supersede this version and restore C-V2X support to the project.

### Added
- C++ implementations of all V2Verifier files.
- Support for GNURadio version 3.8
### Changed
- V2Verifier is now a C++ project
- TkGUI is now a standalone utility included with the project that can be run alongside,
but not as a direct part of, the main C++ code.
- C-V2X is temporarily not supported pending bug fixes in third-party source code that this project relies on.
### Fixed
- Sidelink communication (C-V2X) in V2Verifier based on the srsRAN project ([issue #34](https://github.com/twardokus/v2verifier/issues/34)) was fixed by srsRAN developers (see that project's [issue #838](https://github.com/srsran/srsRAN/issues/838)).
### Deprecated
- All Python-based versions of V2Verifier (<3.0) are no longer supported.
- GNURadio 3.7 is no longer supported. 
### Removed
- All Python (.py,.pyc) files except some utilities and GUI source files.

## [2.0] - 2021-10-10
V2Verifier 2.0 introduced several major changes including support for C-V2X and additional IEEE 1609.2 features.
### Added
- Implicit certificate and certificate digest structures (see IEEE 1609.2 Section 6.4) are now included with V2Verifier messages. \*_Note that full cryptographic support for certificate generation and verification, including 1609.2 pseudonym generation and linkage, is not yet included but is currently under active development_.
- A new, browser-based GUI (built with JavaScript as an Electron app) features a Google Maps integration and support for GNSS-based vehicle locations.
    - This facilitates more realistic experiments
    - Better suited to research activities than the existing Tkinter GUI (which remains suitable for instructional use)
- Real-time message generation and transmission replace pre-generated message queues in versions <= 1.1
    - Compliant with IEEE 1609.2 Section 6.3.9 (regarding the `generationTime` field)
- Support for receiving C-V2X messages from commercial off-the-shelf C-V2X devices ([commit #b35898d](https://github.com/twardokus/v2verifier/commits/master?before=8655d3f1db9c398f9496732a3307af6d7617fb92+70&branch=master))
- A fully functional C-V2X _receiver_ (full SDR-to-SDR C-V2X support is in the final stages of development)
- Basic reputation tracking had been added. Vehicle reputation starts at a customizable value (default 1000) and degrades over time with security failures like signature verification failure or transmission of expired messages
    - This is a starting point for evaluating reputation-based misbehavior detection systems
- The existing Tk-based GUI now features a "threat tracking" interface to allow at-a-glance understanding of vehicle location/motion information within a scenario
- Files and documentation to execute a message replay attack in DSRC are now included with the testbed code
- The project has been significantly restructured. V2Verifier can now be imported as a module, facilitating maximum portability and integration with other open-source projects.
- V2Verifier can now be run as pure simulation if access to software-defined radios is not available
    - This is ideal for testing and development as well as in situations where equipment is limited
### Changed
- V2Verifier no longer requires root permissions (i.e., `sudo`-ing commands is no longer required)
- Several instances of object-oriented design converted to straightforward functions, reducing system resource consumption and improving performance
- Socket communication between testbed components now uses TCP instead of UDP for more reliable (and faster) communication
### Fixed
- Resolve issue with GUI not launching that originated with Python 3.6/3.9 differences in keyword argument handling
- Verification failures due to dropping the leading zero in some ECDSA signatures have been resolved ([commit #648b118](https://github.com/twardokus/v2verifier/commit/648b11883d4f4b71055d84c9cfc6b1c548654160))
### Deprecated
- Scapy-based listeners are no longer supported and receivers based on this implementation may not work properly with the updated transmitter
### Removed
- long-defunct unified DSRC flowgraph file has been removed
- a large number of files dating back to version 0.9, and long-since unused, have been removed


## [1.1] - 2020-11-13
V2Verifier 1.1 was a minor update focused on cleaning up the code base and adding minimal support documentation, e.g., how to run the software.

### Added
- terminal interface and option to use console interaction instead of GUI during program execution
- loopback interface from GNURadio to facilitate experimentation and development without software-defined radios
- placeholders added for certificate structures to ensure realistic packet size
### Changed
- README updated to add instructions for reactive jamming attack and clarify usage of the software in general
- Pre-specifying the number of packets to be sent during simulation (in the configuration file) is no longer required for accurate statistical reporting in GUI
- Tx/Rx flowgraph defaults adjusted to reduce need for end-user tinkering with SDR parameters. This significantly reduces the packet error rate at frequencies approaching 6 GHz, especially on less capable SDRs (e.g., USRP B210)
### Fixed
Nothing to report.
### Deprecated
Nothing to report.
### Removed
Nothing to report.

## [1.0] - 2020-5-20
V2Verifier 1.0 was the first functional software release.

### Added
- Support for V2V communication between software-defined radios using IEEE 802.11p (DSRC) protocol
- Basic features of IEEE 1609.2 V2V security (for example, message signing and verification)
- A basic, Tk-based GUI
### Changed
Nothing to report.
### Fixed
Nothing to report.
### Deprecated
Nothing to report.
### Removed
Nothing to report.
