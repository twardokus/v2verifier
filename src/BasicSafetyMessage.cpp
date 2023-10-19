//
// Created by Geoff Twardokus on 10/19/23.
//

#include "BasicSafetyMessage.h"

BasicSafetyMessage::BasicSafetyMessage(float _latitude,
                                       float _longitude,
                                       float _elevation,
                                       float _heading,
                                       float _speed) {

    this->latitude = _latitude;
    this->longitude = _longitude;
    this->elevation = _elevation;
    this->heading = _heading;
    this->speed = _speed;
}

void BasicSafetyMessage::setLatitude(float _latitude) {
    this->latitude = _latitude;
}

void BasicSafetyMessage::setLongitude(float _longitude) {
    this->longitude = _longitude;
}

void BasicSafetyMessage::setElevation(float _elevation) {
    this->elevation = _elevation;
}

void BasicSafetyMessage::setSpeed(float _speed) {
    this->speed = _speed;
}

void BasicSafetyMessage::setHeading(float _heading) {
    this->heading = _heading;
}
