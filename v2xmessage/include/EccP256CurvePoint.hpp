/** @file   EccP256CurvePoint.hpp
 *  @brief  Implementation of the EccP256CurvePoint ASN.1 defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs
*/

//EccP256CurvePoint::= CHOICE {
//    x-only           OCTET STRING (SIZE (32)),
//    fill             NULL,
//    compressed-y-0   OCTET STRING (SIZE (32)),
//    compressed-y-1   OCTET STRING (SIZE (32)),
//    uncompressedP256 SEQUENCE {
//        x OCTET STRING (SIZE (32)),
//        y OCTET STRING (SIZE (32))
//    }
//}

#ifndef V2VERIFIER_ECCP256CURVEPOINT_HPP
#define V2VERIFIER_ECCP256CURVEPOINT_HPP

#include "V2XMessage.hpp"

/** @brief Options for how a curve point can be encoded under IEEE 1609.2 */
enum CurvePointChoice {
    xOnly,              ///< x-coordinate of the point as a 32-byte unsigned integer
    fillNull,           ///< no value (NULL) is provided
    compressedY0,       ///< y-coordinate of the point as a 32-byte unsigned integer when LSB is 0
    compressedY1,       ///< y-coordinate of the point as a 32-byte unsigned integer when LSB is 1
    uncompressedP256    ///< x- and y- coordinate provided in sequence as 32-byte unsigned integers
};

class EccP256CurvePoint {

public:

    /// Size of the COER representation for instantiations of this object (in bytes)
    static const uint16_t ECC_P256_CURVE_POINT_SIZE_BYTES = 33;

    /** @brief Default constructor */
    EccP256CurvePoint() = default;

    /** @brief Create a new ECCP256CurvePoint for a COER-encoded byte string
     *
     *  @param coerBytes COER encoding of an ECCP256CurvePoint object
     */
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

    /** @brief Get the object's COER representation as a byte string
     *
     *  @return COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;

        auto encodedCurvePointChoice = std::byte{0b10000000} | std::byte{(uint8_t) this->curvePointChoice};
        coerBytes.insert(coerBytes.end(), encodedCurvePointChoice);

        coerBytes.insert(coerBytes.end(), compressedValue.begin(), compressedValue.end());

        return coerBytes;
    }

    /** @brief Get the chosen curve point choice for this object
     *
     *  @return The CurvePointChoice for the object.
     */
    CurvePointChoice getCurvePointChoice() const {
        return this->curvePointChoice;
    }

    /** @brief  Get the compressed coordinate value for this curve point.
     *
     *  This could be x- or y-coordinate, depending on the selection for this->curvePointChoice. Queries should first
     *  call EccP256CurvePoint::getCurvePointChoice() to anticipate the correct coordinate encoding.
     *
     *  @return The compressed x- or y-coordinate value for this curve point.
     */
    std::vector<std::byte> getCompressedValue() const {
        return this->compressedValue;
    }

private:
    CurvePointChoice curvePointChoice;
    std::vector<std::byte> compressedValue;
};

#endif //V2VERIFIER_ECCP256CURVEPOINT_HPP
