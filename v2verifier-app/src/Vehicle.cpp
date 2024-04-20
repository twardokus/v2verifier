//
// Created by Geoff Twardokus on 3/12/24.
//

#include <iostream>

#include "../include/Vehicle.hpp"
#include "../../v2xmessage/include/IEEE1609Dot2Data.hpp"

std::vector<std::byte> Vehicle::getUnsecurePduCOERForPayload(const std::vector<std::byte> &payload) {

    try {
        IEEE1609Dot2Data t(payload);
        if(t.getContent().getContentChoice() != IEEE1609Dot2ContentChoice::unsecuredData) {
            throw std::runtime_error("Invalid call requests content type other than UnsecuredData");
        }
        return t.getCOER();
    }
    catch(std::runtime_error &e) {
        std::cout << e.what() << std::endl;
    }
}

int Vehicle::updateLatitude(const double latitude) {
    if(-90 <= latitude && latitude <= 90) {
        this->locationData.latitude = latitude;
        return 0;
    }
    else {
        return -1;
    }
}

int Vehicle::updateLongitude(const double longitude) {
    if(-180 <= longitude && longitude <= 180) {
        this->locationData.longitude = longitude;
        return 0;
    }
    else {
        return -1;
    }
}

int Vehicle::updateElevation(const double elevation) {
    // The lowest elevation for a road is roughly -500m (near the Dead Sea)
    // The highest elevation for a road is roughly 5800m (near Ladakh, India)
    if(-600 <= elevation && elevation <= 6000) {
        this->locationData.elevation = elevation;
        return 0;
    }
    else {
        return -1;
    }
}

int Vehicle::updateSpeed(const double speed) {
    // speed should never be less than zero
    // we do not expect a vehicle to exceed 110 m/s (250 mph)
    if(0 <= speed && speed <= 110) {
        this->motionData.speed = speed;
        return 0;
    }
    else {
        return -1;
    }
}

int Vehicle::updateHeading(const double heading) {
    if(0 <= heading && heading < 360) {
        this->motionData.heading = heading;
        return 0;
    }
    else {
        return -1;
    }
}

int Vehicle::updateGPSPosition(const double latitude, const double longitude, const double elevation) {
    if(updateLatitude(latitude) != 0)
        return -1;
    if(updateLongitude(longitude) != 0)
        return -1;
    if(updateElevation(elevation) != 0)
        return -1;

    return 0;
}
