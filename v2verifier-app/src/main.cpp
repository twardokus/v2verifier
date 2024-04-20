//
// Created by Geoff Twardokus on 3/6/24.
//

#include <cstddef>
#include <iostream>
#include <vector>

#include "../include/Vehicle.hpp"

int main() {
    std::vector<std::byte> testBytes;
    testBytes.push_back(std::byte{0x03});
    testBytes.push_back(std::byte{0x80});
    testBytes.push_back(std::byte{0xF3});
    testBytes.push_back(std::byte{0xA5});

    auto test = Vehicle::getUnsecurePduCOERForPayload(testBytes);

    return 0;
}