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

    }

    std::vector<std::byte> getCOER() {}

private:

    IEEE1609Dot2DataTypes::HashAlgorithm hashID;
    ToBeSignedData tbsData;
    SignerIdentifier signer;
    Signature signature;
};

#endif //V2VERIFIER_SIGNEDDATA_HPP
