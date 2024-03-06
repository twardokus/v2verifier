//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/IEEE1609Dot2Data.hpp"
#include <vector>

#include <iostream>

int main() {

    std::vector<std::byte> testBytes;
    testBytes.push_back(std::byte{3});
    testBytes.push_back(std::byte{15});

    IEEE1609Dot2Data t(testBytes);

    return t.getProtocolVersion() == 3 ? 0 : 1;
}