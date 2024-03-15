/** @file   SignerIdentifier.hpp
 *  @brief  Implementation of the SignerIdentifier ASN.1 structure defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */


//SignerIdentifier ::= CHOICE {
//  digest      HashedId8,
//  certificate SequenceOfCertificate,
//  self        NULL,
//  ...
//}


#ifndef V2VERIFIER_SIGNERIDENTIFIER_HPP
#define V2VERIFIER_SIGNERIDENTIFIER_HPP

#include "V2XMessage.hpp"

/** @brief Choice of how the signer identifies itself. */
enum SignerIdentifierChoice {
    digest,         ///< A truncated SHA-256 hash digest (HashedID3) of the signer's certificate.
    certificate,    ///< The full signer certificate (as a Certificate).
    self            ///< Self-signed (no credential provided).
};

class SignerIdentifier : V2XMessage {

public:

    static const uint16_t SIGNER_IDENTIFIER_SIZE_BYTES = 1;

    /** @brief Defaul constructor */
    SignerIdentifier() = default;

    /** @brief Create a new SignerIdentifier from a COER encoding.
     *
     *  @param coerBytes The COER encoding from which to create a new object.
     */
    SignerIdentifier(std::vector<std::byte> &coerBytes) {

        // For self-signed, this thing should just be one octet with value 0x82
        if(coerBytes.size() == 1 && coerBytes.at(0) == std::byte{0b10000010}) {
            this->signerIdentifierChoice = SignerIdentifierChoice::self;
        }
        else {
            throw std::runtime_error("Invalid SignerIdentifier, only self-signed supported at this time.");
        }
    }

    /** @brief Get the COER encoding of the object.
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;
        coerBytes.push_back(std::byte{0b10000000} | std::byte{(uint8_t) this->signerIdentifierChoice});
        return coerBytes;
    }

    /** @brief Get the choice of signer identifier (SignerIdentifier::SignerIdentifierChoice)
     *
     *  @return The type of signer identifier.
     */
    [[nodiscard]] SignerIdentifierChoice getSignerIdentifierChoice() const {
        return this->signerIdentifierChoice;
    }

private:
    SignerIdentifierChoice signerIdentifierChoice;
//    std::vector<std::byte> digest;
//    std::vector<Certificate> certificate;

};
#endif //V2VERIFIER_SIGNERIDENTIFIER_HPP
