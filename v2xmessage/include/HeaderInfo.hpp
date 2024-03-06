//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_HEADERINFO_HPP
#define V2VERIFIER_HEADERINFO_HPP

/*
HeaderInfo ::= SEQUENCE {
  psid                  Psid,
  generationTime        Time64 OPTIONAL,
  expiryTime            Time64 OPTIONAL,
  generationLocation    ThreeDLocation OPTIONAL,
  p2pcdLearningRequest  HashedId3 OPTIONAL,
  missingCrlIdentifier  MissingCrlIdentifier OPTIONAL,
  encryptionKey         EncryptionKey OPTIONAL,
  ...,
  inlineP2pcdRequest    SequenceOfHashedId3 OPTIONAL,
  requestedCertificate  Certificate OPTIONAL,
  pduFunctionalType     PduFunctionalType OPTIONAL,
  contributedExtensions ContributedExtensionBlocks OPTIONAL
}
*/

#include "V2XMessage.hpp"

class HeaderInfo : V2XMessage {

public:

    HeaderInfo() = default;
    HeaderInfo(std::vector<std::byte> &coerBytes) {

        if(coerBytes.size() == 20) {
            std::memcpy(&psid, coerBytes.data(), sizeof(std::uint32_t));
            std::memcpy(&generationTime, coerBytes.data() + 4, sizeof(std::uint64_t));
            std::memcpy(&expiryTime, coerBytes.data() + 12, sizeof(std::uint64_t));
        }
        else {
            throw std::runtime_error("Invalid data for HeaderInfo");
        }

    }

    std::vector<std::byte> getCOER() {}

private:

    uint32_t psid;              // This is a 4-octet word under ASN.1 encoding rules
    uint64_t generationTime;    // This is an 8-octet word under ASN.1 encoding rules
    uint64_t expiryTime;        // This is an 8-octet word under ASN.1 encoding rules

};

#endif //V2VERIFIER_HEADERINFO_HPP
