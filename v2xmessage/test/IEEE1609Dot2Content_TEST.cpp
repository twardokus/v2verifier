//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/IEEE1609Dot2Content.hpp"
#include <vector>

#include <iostream>

int main() {

    std::vector<std::byte> testBytes;
    testBytes.push_back(std::byte{0x81});
    testBytes.push_back(std::byte{0x11});

    IEEE1609Dot2Content t(testBytes);

    return t.getContentChoice() != IEEE1609Dot2ContentChoice::signedData;
}