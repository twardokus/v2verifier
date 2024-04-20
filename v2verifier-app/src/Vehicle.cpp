//
// Created by Geoff Twardokus on 3/12/24.
//

#include <iostream>

#include "../../logger/Log.h"
#include "../include/Vehicle.hpp"
#include "../../v2xmessage/include/IEEE1609Dot2Data.hpp"

Vehicle::Vehicle(double latitude, double longitude, double elevation, double speed, double heading) {
    if(initializePositionAndMotion(latitude,longitude,elevation,speed,heading) != 0) {
        Logger::logFatal(std::string("Failed to initialize vehicle: invalid parameters provided."));
        exit(-1);
    }
}

Vehicle::Vehicle(double latitude, double longitude, double elevation) {
    if(initializePositionAndMotion(latitude,longitude,elevation,0,0) != 0) {
        Logger::logFatal(std::string("Failed to initialize vehicle: invalid parameters provided."));
        exit(-1);
    }
}

int Vehicle::initializePositionAndMotion(double latitude,
                                         double longitude,
                                         double elevation,
                                         double speed,
                                         double heading) {

    if(updateLatitude(latitude) != 0)
        return -1;
    if(updateLongitude(longitude) != 0)
        return -1;
    if(updateElevation(elevation) != 0)
        return -1;
    if(updateSpeed(speed) != 0)
        return -1;
    if(updateHeading(heading) != 0)
        return -1;

    return 0;
}

int Vehicle::updateLatitude(const double latitude) {
    if(-90 <= latitude && latitude <= 90) {
        this->locationData.latitude = latitude;
        return 0;
    }
    else {
        auto field_name = std::string("latitude");
        Logger::logWarning(formatErrorForInvalidValue(field_name, latitude));
        return -1;
    }
}

int Vehicle::updateLongitude(const double longitude) {
    if(-180 <= longitude && longitude <= 180) {
        this->locationData.longitude = longitude;
        return 0;
    }
    else {
        auto field_name = std::string("longitude");
        Logger::logWarning(formatErrorForInvalidValue(field_name, longitude));
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
        auto field_name = std::string("elevation");
        Logger::logWarning(formatErrorForInvalidValue(field_name, elevation));
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
        auto field_name = std::string("speed");
        Logger::logWarning(formatErrorForInvalidValue(field_name, speed));
        return -1;
    }
}

int Vehicle::updateHeading(const double heading) {
    if(0 <= heading && heading < 360) {
        this->motionData.heading = heading;
        return 0;
    }
    else {
        auto field_name = std::string("heading");
        Logger::logWarning(formatErrorForInvalidValue(field_name, heading));
        return -1;
    }
}

int Vehicle::updateGPSPosition(const double latitude, const double longitude, const double elevation) {
    if(updateLatitude(latitude) != 0) {
        Logger::logWarning(std::string("Failed to set GPS position"));
        return -1;
    }
    if(updateLongitude(longitude) != 0) {
        Logger::logWarning(std::string("Failed to set GPS position"));
        return -1;
    }
    if(updateElevation(elevation) != 0) {
        Logger::logWarning(std::string("Failed to set GPS position"));
        return -1;
    }

    return 0;
}

std::string Vehicle::formatErrorForInvalidValue(std::string &field, const double invalidValue) {
    return  std::string("Failed to update " +
            field +
            std::string(" (invalid value: ") + std::to_string(invalidValue) + std::string(")"));
}

std::string Vehicle::formatErrorForInvalidValue(std::string &field, const int invalidValue) {
    return  std::string("Failed to update " +
                        field +
                        std::string(" (invalid value: ") + std::to_string(invalidValue) + std::string(")"));
}