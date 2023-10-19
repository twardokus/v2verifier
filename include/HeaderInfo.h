//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_HEADERINFO_H
#define V2VERIFIER_HEADERINFO_H


#include <cstdint>

class HeaderInfo {

public:

    HeaderInfo() = default;
    HeaderInfo(HeaderInfo& headerInfo) {
        this->psid = headerInfo.getPsid();
        this->generationTime = headerInfo.getGenerationTime();
        this->expiryTime = headerInfo.getExpiryTime();
    }
    HeaderInfo(uint8_t _psid, uint64_t _generationTime, uint64_t _expiryTime) {
        this->psid = _psid;
        this->generationTime = _generationTime;
        this->expiryTime = _expiryTime;
    }

    uint8_t getPsid();
    uint64_t getGenerationTime();
    uint64_t getExpiryTime();

    void setPsid(uint8_t _psid);
    void setGenerationTime(uint64_t _generationTime);
    void setExpiryTime(uint64_t _expiryTime);

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
