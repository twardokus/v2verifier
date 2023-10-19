//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_HEADERINFO_H
#define V2VERIFIER_HEADERINFO_H


#include <cstdint>

class HeaderInfo {

private:
    uint8_t psid; /* Can be much larger than 1 octet per IEEE 1609.12, but sufficient for our purposes */
    uint64_t generationTime;
    uint64_t expiryTime;

    /* To be implemented at a later time TBD */
//    ThreeDLocation generationLocation;
//    HashedId3 p2pcdLearningRequest;
//    MissingCrlIdentifier missingCrlIdentifier;
//    EncryptionKey encryptionKey;
//    SequenceOfHashedId3 inlineP2pcdRequest;
//    Certificate requestedCertificate;
//    PduFunctionalType pduFunctionalType;
//    ContributedExtensionsBlock contributedExtensionsBlock;
};


#endif //V2VERIFIER_HEADERINFO_H
