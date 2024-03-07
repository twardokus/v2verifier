//
// Created by Geoff Twardokus on 3/6/24.
//

/*
SignerIdentifier ::= CHOICE {
  digest      HashedId8,
  certificate SequenceOfCertificate,
  self        NULL,
  ...
}
*/

#ifndef V2VERIFIER_SIGNERIDENTIFIER_HPP
#define V2VERIFIER_SIGNERIDENTIFIER_HPP

#include "V2XMessage.hpp"

enum SignerIdentifierChoice {
    digest,
    certificate,
    self
};

class SignerIdentifier : V2XMessage {

public:
    SignerIdentifier() = default;
    SignerIdentifier(std::vector<std::byte> &coerBytes) {

        // For self-signed, this thing should just be one octet with value 0x82
        if(coerBytes.size() == 1 && coerBytes.at(0) == std::byte{0b10000010}) {
            this->signerIdentifierChoice = SignerIdentifierChoice::self;
        }
        else {
            throw std::runtime_error("Invalid SignerIdentifier, only self-signed supported at this time.");
        }
    }

    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;
        coerBytes.push_back(std::byte{0b10000000} | std::byte{(uint8_t) this->signerIdentifierChoice});
        return coerBytes;
    }

    [[nodiscard]] SignerIdentifierChoice getSignerIdentifierChoice() const {
        return this->signerIdentifierChoice;
    }

private:
    SignerIdentifierChoice signerIdentifierChoice;
//    std::vector<std::byte> digest;
//    std::vector<Certificate> certificate;

};
#endif //V2VERIFIER_SIGNERIDENTIFIER_HPP
