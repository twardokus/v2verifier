//
// Created by Geoff Twardokus on 10/19/23.
//

#include "HeaderInfo.h"

uint8_t HeaderInfo::getPsid() const {
    return this->psid;
}

uint64_t HeaderInfo::getGenerationTime() const {
    return this->generationTime;
}

uint64_t HeaderInfo::getExpiryTime() const {
    return this->expiryTime;
}

void HeaderInfo::setPsid(uint8_t _psid) {
    this->psid = _psid;
}

void HeaderInfo::setGenerationTime(uint64_t _generationTime) {
    this->generationTime = _generationTime;
}

void HeaderInfo::setExpiryTime(uint64_t _expiryTime) {
    this->expiryTime = _expiryTime;
}
