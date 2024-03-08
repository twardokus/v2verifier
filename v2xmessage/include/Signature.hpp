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

    static const uint16_t SIGNATURE_SIZE_BYTES = EcdsaP256Signature::ECDSAP256_SIGNATURE_SIZE_BYTES + 1;

    Signature() = default;

    Signature(std::vector<std::byte> &coerBytes) {

        if(coerBytes.size() == SIGNATURE_SIZE_BYTES) {
            auto signatureChoiceByte = coerBytes.at(0);
            if((uint8_t) (std::byte{0x0F} & signatureChoiceByte) != (uint8_t) SignatureChoice::ecdsaNistP256Signature) {
                throw std::runtime_error("Only ECDSANistP256 is currently supported");
            }
            else {
                this->signatureChoice = SignatureChoice::ecdsaNistP256Signature;
            }

            std::vector<std::byte> signatureBytes;
            signatureBytes.insert(signatureBytes.end(), coerBytes.begin() + 1, coerBytes.end());
            this->ecdsaP256Signature = EcdsaP256Signature(signatureBytes);
        }
        else {
            throw std::runtime_error("Invalid COER (wrong length) for a Signature.");
        }
    }

    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;

        std::vector<std::byte> signatureChoiceBytes = {std::byte{0x80} | std::byte{(uint8_t) this->signatureChoice}};
        auto signatureBytes = this->ecdsaP256Signature.getCOER();

        coerBytes.insert(coerBytes.end(), signatureChoiceBytes.begin(), signatureChoiceBytes.end());
        coerBytes.insert(coerBytes.end(), signatureBytes.begin(), signatureBytes.end());

        return coerBytes;
    }

    [[nodiscard]] SignatureChoice getSignatureChoice() const {
        return this->signatureChoice;
    }

    [[nodiscard]] EcdsaP256Signature getEcdsaP256Signature() const {
        return this->ecdsaP256Signature;
    }

private:
    SignatureChoice signatureChoice;
    EcdsaP256Signature ecdsaP256Signature;
};

#endif //V2VERIFIER_SIGNATURE_HPP
