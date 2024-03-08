//
// Created by Geoff Twardokus on 3/8/24.
//

#include "../include/Signature.hpp"

int main() {

    std::vector<std::byte> testBytes;

    // Choice of signature in the Signature structure
    testBytes.push_back(std::byte{0x80});

    auto ecdsaP256Bytes = Utility::randomBytesOfLength(EcdsaP256Signature::ECDSAP256_SIGNATURE_SIZE_BYTES);
    ecdsaP256Bytes[0] = std::byte{0x80};
    ecdsaP256Bytes[1] = std::byte{0x80};
//    auto eccP256CurvePointBytes = Utility::randomBytesOfLength(EccP256CurvePoint::ECC_P256_CURVE_POINT_SIZE_BYTES);

    // Specify curve choice
//    eccP256CurvePointBytes[0] = std::byte{0x80};

    testBytes.insert(testBytes.end(), ecdsaP256Bytes.begin(), ecdsaP256Bytes.end());
//    testBytes.insert(testBytes.end(), eccP256CurvePointBytes.begin(), eccP256CurvePointBytes.end());

    Signature s(testBytes);

    if(s.getEcdsaP256Signature().getCOER() != ecdsaP256Bytes)
        return 1;
    if(s.getSignatureChoice() != SignatureChoice::ecdsaNistP256Signature)
        return 2;
    if(s.getCOER() != testBytes)
        return 3;

    return 0;
}