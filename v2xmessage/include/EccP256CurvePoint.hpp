//
// Created by Geoff Twardokus on 3/7/24.
//
/*
EccP256CurvePoint::= CHOICE {
    x-only           OCTET STRING (SIZE (32)),
    fill             NULL,
    compressed-y-0   OCTET STRING (SIZE (32)),
    compressed-y-1   OCTET STRING (SIZE (32)),
    uncompressedP256 SEQUENCE {
      x OCTET STRING (SIZE (32)),
      y OCTET STRING (SIZE (32))
    }
}
*/

#ifndef V2VERIFIER_ECCP256CURVEPOINT_HPP
#define V2VERIFIER_ECCP256CURVEPOINT_HPP

#include "V2XMessage.hpp"

enum CurvePointChoice {
    xOnly,
    fillNull,
    compressedY0,
    compressedY1,
    uncompressedP256
};

class EccP256CurvePoint {

public:

    static const uint16_t ECC_P256_CURVE_POINT_SIZE_BYTES = 33;

    EccP256CurvePoint() = default;
    EccP256CurvePoint(std::vector<std::byte> &coerBytes) {
        if(coerBytes.size() != ECC_P256_CURVE_POINT_SIZE_BYTES) {
            throw std::runtime_error("Invalid COER (wrong length) provided for EccP256CurvePoint");
        }

        auto choiceTag = (uint8_t) (coerBytes.at(0) & std::byte{0b00111111});
        auto choiceByte = coerBytes.at(0);

        if(
            (choiceByte & std::byte{0b11000000}) == std::byte{0b10000000}   // Make sure bit 8 is set and bit 7 is not
        ) {
            if(0 <= choiceTag && choiceTag <= 4) {
                if (choiceTag == 0) {
                    this->curvePointChoice = (CurvePointChoice) choiceTag;
                    auto start = coerBytes.begin() + 1;
                    auto end = coerBytes.end();
                    this->compressedValue = std::vector<std::byte>(start, end);
                }
            }
            else {
                throw std::runtime_error("Only xOnly is supported as a CurvePointChoice at this time.");
            }
        }
        else {
            throw std::runtime_error("Invalid CurvePointChoice tag number.");
        }
    }

    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;

        auto encodedCurvePointChoice = std::byte{0b10000000} | std::byte{(uint8_t) this->curvePointChoice};
        coerBytes.insert(coerBytes.end(), encodedCurvePointChoice);

        coerBytes.insert(coerBytes.end(), compressedValue.begin(), compressedValue.end());

        return coerBytes;
    }

    CurvePointChoice getCurvePointChoice() const {
        return this->curvePointChoice;
    }

    std::vector<std::byte> getCompressedValue() const {
        return this->compressedValue;
    }

private:
    CurvePointChoice curvePointChoice;

    std::vector<std::byte> compressedValue;
};

#endif //V2VERIFIER_ECCP256CURVEPOINT_HPP
