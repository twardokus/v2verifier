// Copyright (c) 2022. Geoff Twardokus
// Reuse permitted under the MIT License as specified in the LICENSE file within this project.

//
// Created by geoff on 6/5/22.
//

#include <bsm.h>

float calculate_speed_kph(float x1, float x2, float y1, float y2, float time_msec) {
    double distance_km = sqrt(pow(x2-x1,2) + pow(y2-y1,2)) / 1000;
    double time_hours = time_msec / (60 * 60 * 1000);
    return distance_km/time_hours;
}

float calculate_heading(float x1, float x2, float y1, float y2) {
    return atan2(y2-y1, x2-x1) * 180 / M_PI;
}