# Changelog
Notable changes to this project will be tracked here. Additions, deprecations, etc. are described per version release.

## Unreleased changes
### Added
- Message certificates are now added to the 1609.2 message structure, moving V2Verifier more closely to full support for the IEEE 1609.2 and 1609.2.1 standards. \*Note that full cryptographic support for certificate generation and verification, including 1609.2 pseudonym generation and linkage, is not yet included but is currently under active development.
- A new, browser-based GUI (built with Electron) features Google Maps integration and support for GNSS-based vehicle locations, facilitaing more realistic experimentation and providing an interface that is better suited to research activities than the existing Tkinter GUI.
- Real-time message generation and transmission replace pre-generated message queues in versions <= 1.1
- Support for receiving C-V2X messages from commercial off-the-shelf C-V2X devices ([commit #b35898d](https://github.com/twardokus/v2verifier/commits/master?before=8655d3f1db9c398f9496732a3307af6d7617fb92+70&branch=master))
- A fully functional C-V2X _receiver_ (full SDR-to-SDR C-V2X support is in the final stages of development)
- To support misbehavior detection system evaluation, a basic reputation tracking functionality had been added which degrades vehicle reputation based on security issues like signature verification failures or receipt of expired messages
- The Tk-based GUI now features a "threat tracking" interface to allow at-a-glance reporting on vehicle location/motion information within a scenario
- Files and documentation to execute a message replay attack in DSRC are now included with the testbed code.
- The project has been significantly restructured to reflect a typical Python module. V2Verifier can now be imported as a module, facilitating maximum portability and potential integration with other open-source projects.
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
