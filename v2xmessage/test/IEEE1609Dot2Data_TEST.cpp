//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/IEEE1609Dot2Data.hpp"
#include <vector>

#include <iostream>

int main() {

    std::vector<std::byte> testBytes;
    testBytes.push_back(std::byte{0x03});
    testBytes.push_back(std::byte{0x80});
    testBytes.push_back(std::byte{0x11});

    IEEE1609Dot2Data t(testBytes);

    return t.getProtocolVersion() == 3 ? 0 : 1;
}