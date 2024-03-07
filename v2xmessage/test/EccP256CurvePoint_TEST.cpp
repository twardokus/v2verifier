//
// Created by Geoff Twardokus on 3/7/24.
//

#include "../include/EccP256CurvePoint.hpp"

#include <random>


int main() {

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(0, 255);

    std::vector<std::byte> testPoint;
    testPoint.reserve(33);
    testPoint.assign(33,std::byte{0});


    for(auto & i : testPoint) {
        i = std::byte{(uint8_t) distr(gen)};
    }
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