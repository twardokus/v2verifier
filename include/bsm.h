//
// Created by geoff on 10/19/21.
//

#ifndef CPP_BSM_H
#define CPP_BSM_H

#include <cmath>

struct bsm {
    float latitude;
    float longitude;
    float elevation;
    float speed;
    float heading;
};

// Assume all positions are in meters and time is in milliseconds
float calculate_speed_kph(float x1, float x2, float y1, float y2, float time_msec);
float calculate_heading(float x1, float x2, float y1, float y2);

#endif //CPP_BSM_H
