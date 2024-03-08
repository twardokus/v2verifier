//
// Created by Geoff Twardokus on 3/6/24.
//

/*
Signature ::= CHOICE {
    ecdsaNistP256Signature        EcdsaP256Signature,
    ecdsaBrainpoolP256r1Signature EcdsaP256Signature,
    ...,
    ecdsaBrainpoolP384r1Signature EcdsaP384Signature,
    ecdsaNistP384Signature        EcdsaP384Signature,
    sm2Signature                  EcsigP256Signature
}
*/

#ifndef V2VERIFIER_SIGNATURE_HPP
#define V2VERIFIER_SIGNATURE_HPP

#include "V2XMessage.hpp"
#include "EcdsaP256Signature.hpp"

enum SignatureChoice {
    ecdsaNistP256Signature,
    ecdsaBrainpoolP256r1Signature,
    ecdsaBrainpoolP384r1Signature,
    ecdsaNistP384Signature,
    sm2Signature
};

class Signature : V2XMessage {

public:
    Signature() = default;

    Signature(std::vector<std::byte> &coerBytes) {

        auto signatureChoiceByte = coerBytes.at(0);



    }

    std::vector<std::byte> getCOER() {}

private:
    SignatureChoice signatureChoice;
    EcdsaP256Signature ecdsaP256Signature;
};

#endif //V2VERIFIER_SIGNATURE_HPP
