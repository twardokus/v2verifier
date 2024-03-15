//
// Created by Geoff Twardokus on 3/7/24.
//

#include "../include/EccP256CurvePoint.hpp"

#include <random>


int main() {

    auto testPoint = Utility::randomBytesOfLength(33);
    testPoint[0] = std::byte{0x80};

    EccP256CurvePoint e(testPoint);

    if(e.getCurvePointChoice() != CurvePointChoice::xOnly)
        return 1;

    auto start = testPoint.begin() + 1;
    auto end = testPoint.end();
    auto cutDownTestPoint = std::vector<std::byte>(start, end);

    if(e.getCompressedValue() != cutDownTestPoint)
        return 2;

    if(e.getCOER() != testPoint)
        return 3;

    return 0;
}