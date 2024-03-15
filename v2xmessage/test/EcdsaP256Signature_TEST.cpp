//
// Created by Geoff Twardokus on 3/7/24.
//

#include "../include/EcdsaP256Signature.hpp"

int main() {

    auto sigBytes = Utility::randomBytesOfLength(EcdsaP256Signature::ECDSAP256_SIGNATURE_SIZE_BYTES);
    sigBytes[0] = std::byte{0x80};
    sigBytes[1] = std::byte{0x80};

    EcdsaP256Signature e(sigBytes);

    if(e.getRSig().getCurvePointChoice() != CurvePointChoice::xOnly)
        return 1;

    auto tempSBytes = std::vector<std::byte>(sigBytes.end() - 32, sigBytes.end());
    if(tempSBytes != e.getSSig())
        return 2;

    return 0;
}