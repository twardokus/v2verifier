//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/IEEE1609Dot2Data.hpp"
#include <vector>

#include <iostream>

int main() {

    // UnsecuredData version

    std::vector<std::byte> testBytes;
    testBytes.push_back(std::byte{0x03});
    testBytes.push_back(std::byte{0x80});

    auto randomBytes = Utility::randomBytesOfLength(100);

    testBytes.insert(testBytes.end(), randomBytes.begin(), randomBytes.end());

    IEEE1609Dot2Data t(testBytes);

    if(t.getProtocolVersion() != 3)
        return 1;

    auto test = t.getContent().getCOER();
    if(t.getCOER() != testBytes)
        return 2;

    // SignedData test

    // TODO implement this

    return 0;
}