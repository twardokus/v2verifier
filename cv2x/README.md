# Cellular Vehicle-to-Everything Traffic Generator

An SDR-based C-V2X Traffic Generator based on [srsLTE](https://github.com/srsLTE/srsLTE).

![TU Dortmund University](img/tu-dortmund_small.png "TU Dortmund University")
![Communication Networks Institute](img/CNI_small.png "Communication Networks Institute")
![SFB 876](img/SFB876_small.png "Collaborative Research Center SFB 876")
![DFG](img/DFG_small.png "DFG")


The work on this paper has been partially funded by Deutsche Forschungsgemeinschaft (DFG) within the Collaborative Research Center SFB 876 project B4.

# Installation

The build dependencies are the same as for srsLTE and can be found [here](https://github.com/srsLTE/srsLTE#build-instructions).

### Download and build:
```
git clone https://github.com/FabianEckermann/cv2x-traffic-generator.git
cd cv2x-traffic-generator
mkdir build
cd build
cmake ../
make
```

### Install:
```
sudo make install
```


# Usage

The traffic generator can be used with static settings
```
   cv2x_traffic_generator -a clock=gpsdo -s 0 -l 5
```
or with a configuration file (an example config file is included in this repository)
```
   cv2x_traffic_generator -a clock=gpsdo -i sf_config.csv -o logfile.csv
```

# Cite as

If you use this traffic generator in your research, please cite the following paper:

<!-- F. Eckermann, C. Wietfeld, ["SDR-based open-source C-V2X traffic generator for stress testing vehicular communication"](https://www.kn.e-technik.tu-dortmund.de/.cni-bibliography/publications/cni-publications/Eckermann2021sdr-based.pdf), In 2021 IEEE 93rd Vehicular Technology Conference (VTC-Spring), Helsinki, Finland, April 2021. -->

F. Eckermann, C. Wietfeld, "SDR-based open-source C-V2X traffic generator for stress testing vehicular communication", In 2021 IEEE 93rd Vehicular Technology Conference (VTC-Spring), Helsinki, Finland, April 2021.

### Bibtex:

	@InProceedings{Eckermann2021sdr,
		Author = {Fabian Eckermann and Christian Wietfeld},
		Title = {{SDR}-based open-source {C-V2X} traffic generator for stress testing vehicular communication},
		Booktitle = {2021 IEEE 93rd Vehicular Technology Conference (VTC-Spring)},
		Year = {2021},
		Publishingstatus = {accepted for presentation},
		Address = {Helsinki, Finland},
		Month = {April}
	}