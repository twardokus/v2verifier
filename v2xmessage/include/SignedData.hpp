//
// Created by Geoff Twardokus on 3/6/24.
//


/*
SignedData ::= SEQUENCE {
  hashId    HashAlgorithm,
  tbsData   ToBeSignedData,
  signer    SignerIdentifier,
  signature Signature
}
*/

#ifndef V2VERIFIER_SIGNEDDATA_HPP
#define V2VERIFIER_SIGNEDDATA_HPP

#include "Signature.hpp"
#include "SignerIdentifier.hpp"
#include "ToBeSignedData.hpp"
#include "V2XMessage.hpp"

class SignedData : V2XMessage {

public:
    SignedData() = default;
    SignedData(const std::vector<std::byte> &coerBytes) {

        this->hashID = (IEEE1609Dot2DataTypes::HashAlgorithm) ((uint8_t) coerBytes.at(0));

        std::vector<std::byte> tbsDataBytes;
        std::vector<std::byte> signerBytes;
        std::vector<std::byte> signatureBytes;

        tbsDataBytes.insert(tbsDataBytes.end(),
                            coerBytes.begin() + 1,
                            coerBytes.end() - SignerIdentifier::SIGNER_IDENTIFIER_SIZE_BYTES - Signature::SIGNATURE_SIZE_BYTES);
        signerBytes.insert(signerBytes.end(),
                           coerBytes.end() - SignerIdentifier::SIGNER_IDENTIFIER_SIZE_BYTES - Signature::SIGNATURE_SIZE_BYTES,
                           coerBytes.end() - Signature::SIGNATURE_SIZE_BYTES);
        signatureBytes.insert(signatureBytes.end(),
                              coerBytes.end() - Signature::SIGNATURE_SIZE_BYTES,
                              coerBytes.end());

        this->tbsData = ToBeSignedData(tbsDataBytes);
        this->signer = SignerIdentifier(signerBytes);
        this->signature = Signature(signatureBytes);
    }

    std::vector<std::byte> getCOER() {

        std::vector<std::byte> coerBytes;

        std::vector<std::byte> hashIDBytes = {std::byte{(uint8_t) this->hashID}};
        std::vector<std::byte> toBeSignedDataBytes = this->tbsData.getCOER();
        std::vector<std::byte> signerIdentifierBytes = this->signer.getCOER();
        std::vector<std::byte> signatureBytes = this->signature.getCOER();

        coerBytes.insert(coerBytes.end(), hashIDBytes.begin(), hashIDBytes.end());
        coerBytes.insert(coerBytes.end(), toBeSignedDataBytes.begin(), toBeSignedDataBytes.end());
        coerBytes.insert(coerBytes.end(), signerIdentifierBytes.begin(), signerIdentifierBytes.end());
        coerBytes.insert(coerBytes.end(), signatureBytes.begin(), signatureBytes.end());

        return coerBytes;
    }

    [[nodiscard]] IEEE1609Dot2DataTypes::HashAlgorithm getHashID() const {
        return this->hashID;
    }

    [[nodiscard]] ToBeSignedData getTbsData() const {
        return this->tbsData;
    }

    [[nodiscard]] SignerIdentifier getSigner() const {
        return this->signer;
    }

    [[nodiscard]] Signature getSignature() const {
        return this->signature;
    }

private:
    IEEE1609Dot2DataTypes::HashAlgorithm hashID;
    ToBeSignedData tbsData;
    SignerIdentifier signer;
    Signature signature;

};

#endif //V2VERIFIER_SIGNEDDATA_HPP
