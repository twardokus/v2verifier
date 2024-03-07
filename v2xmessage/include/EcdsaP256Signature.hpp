//
// Created by Geoff Twardokus on 3/7/24.
//

#ifndef V2VERIFIER_ECDSAP256SIGNATURE_HPP
#define V2VERIFIER_ECDSAP256SIGNATURE_HPP

#include "V2XMessage.hpp"
#include "EccP256CurvePoint.hpp"

class EcdsaP256Signature {

public:
    EcdsaP256Signature() = default;
    EcdsaP256Signature(std::vector<std::byte> &coerBytes) {

    }

    std::vector<std::byte> getCOER() {}

private:
    EccP256CurvePoint rSig;
    std::vector<std::byte> sSig;

};
#endif //V2VERIFIER_ECDSAP256SIGNATURE_HPP
