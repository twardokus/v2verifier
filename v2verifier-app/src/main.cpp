//
// Created by Geoff Twardokus on 3/6/24.
//

#include <cstddef>
#include <iostream>
#include <vector>

#include "../../logger/Log.h"
#include "../include/Vehicle.hpp"

int main() {

    Logger::startLog("vehicleLog.txt");

//    std::vector<std::byte> testBytes;
//    testBytes.push_back(std::byte{0x03});
//    testBytes.push_back(std::byte{0x80});
//    testBytes.push_back(std::byte{0xF3});
//    testBytes.push_back(std::byte{0xA5});
//
//    auto test = Vehicle::getUnsecurePduCOERForPayload(testBytes);

    Vehicle v(43, 75, 100, 100, 40);

    return 0;
}