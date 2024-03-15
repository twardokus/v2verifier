/** @file   Signature.hpp
 *  @brief  Implementation of the Signature ASN.1 structure defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

//Signature ::= CHOICE {
//    ecdsaNistP256Signature        EcdsaP256Signature,
//    ecdsaBrainpoolP256r1Signature EcdsaP256Signature,
//    ...,
//    ecdsaBrainpoolP384r1Signature EcdsaP384Signature,
//    ecdsaNistP384Signature        EcdsaP384Signature,
//    sm2Signature                  EcsigP256Signature
//}


#ifndef V2VERIFIER_SIGNATURE_HPP
#define V2VERIFIER_SIGNATURE_HPP

#include "V2XMessage.hpp"
#include "EcdsaP256Signature.hpp"

/** @brief Choice of signature instantiated in this object */
enum SignatureChoice {
    ecdsaNistP256Signature,         ///< ECDSA with the NIST P.256 curve
    ecdsaBrainpoolP256r1Signature,  ///< ECDSA with the Brainpool P256r1 curve
    ecdsaBrainpoolP384r1Signature,  ///< ECDSA with the Brainpool P384r1 curve
    ecdsaNistP384Signature,         ///< ECDSA with the NIST P.384 curve
    sm2Signature                    ///< SM2 (Chinese variant of ECDSA 256)
};

class Signature : V2XMessage {

public:

    /** @brief Size of the COER encoding of this object (in bytes).
     *
     *  Defined as the size of an EcdsaP256Signature (EcdsaP256Signature::ECDSAP256_SIGNATURE_SIZE_BYTES) plus one byte
     *  for the COER-encoded SignatureChoice value.
     */
    static const uint16_t SIGNATURE_SIZE_BYTES = EcdsaP256Signature::ECDSAP256_SIGNATURE_SIZE_BYTES + 1;

    /** @brief Default constructor. */
    Signature() = default;

    /** @brief Create a new Signature using a COER-encoded byte string.
     *
     * @param coerBytes The COER encoding from which to create the object.
     */
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

    /** @brief Get the COER encoding of the object.
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;

        std::vector<std::byte> signatureChoiceBytes = {std::byte{0x80} | std::byte{(uint8_t) this->signatureChoice}};
        auto signatureBytes = this->ecdsaP256Signature.getCOER();

        coerBytes.insert(coerBytes.end(), signatureChoiceBytes.begin(), signatureChoiceBytes.end());
        coerBytes.insert(coerBytes.end(), signatureBytes.begin(), signatureBytes.end());

        return coerBytes;
    }

    /** @brief Get the signature choice (a SignatureChoice value) for the instantiated signature.
     *
     *  @return The SignatureChoice value for this signature.
     */
    [[nodiscard]] SignatureChoice getSignatureChoice() const {
        return this->signatureChoice;
    }

    /** @brief Get the EcdsaP256Signature encapsulated in this object.
     *
     *  @return The EcdsaP256Signature encapsulated in this object.
     */
    [[nodiscard]] EcdsaP256Signature getEcdsaP256Signature() const {
        return this->ecdsaP256Signature;
    }

private:
    SignatureChoice signatureChoice;
    EcdsaP256Signature ecdsaP256Signature;
};

#endif //V2VERIFIER_SIGNATURE_HPP
