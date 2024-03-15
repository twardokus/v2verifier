//
// Created by Geoff Twardokus on 3/6/24.
//

#include <cstddef>
#include <iostream>
#include <vector>

#include "../../v2xmessage/include/IEEE1609Dot2Data.hpp"

int main() {

    std::vector<std::byte> testBytes;
    testBytes.push_back(std::byte{0x03});
    testBytes.push_back(std::byte{0x80});
    testBytes.push_back(std::byte{0xF3});
    testBytes.push_back(std::byte{0xA5});

    IEEE1609Dot2Data t(testBytes);

    return 0;
}