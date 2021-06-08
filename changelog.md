# Changelog
Notable changes to this project will be tracked here. Additions, deprecations, etc. are described per version release.

## Unreleased changes
### Added
- major re-structuring of the project to reflect a typical Python project. V2Verifier can now be imported as a module for maximum portability and integration with other open-source projects.
- a new GUI, based on Electron, features a Google Maps integration and support for GNSS-based vehicle locations, facilitaing more realistic experimentation and an interface better suited to research activities than the old Tk-based GUI
- real-time message generation and transmission replaces pre-generated message queues in versions <= 1.1
- initial support for receiving ([not] transmitting) C-V2X messages from commercial devices ([commit #b35898d](https://github.com/twardokus/v2verifier/commits/master?before=8655d3f1db9c398f9496732a3307af6d7617fb92+70&branch=master))
- fully functional C-V2X receiver (note that SDR-to-SDR C-V2X support is still under development)
- a basic reputation tracking functionality which degrades vehicle reputation based on signature verification failures and receipt of expired messages
- Tk-based GUI now features a "threat tracking" interface to allow at-a-glance reporting on vehicle location/motion information within a scenario
- files to execute a simple message replay attack in DSRC are now included with the testbed code
### Changed
- V2Verifier no longer requires root permissions (i.e., `sudo`-ing commands is no longer required)
- Several instances of object-oriented design converted to straightforward functions, reducing system resource consumption and improving performance
- socket communication between testbed components now uses TCP instead of UDP for more reliable (and faster) communication
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
