//
// Created by Geoff Twardokus on 10/25/23.
//

#include "ToBeSignedCertificate.h"

ToBeSignedCertificate::ToBeSignedCertificate(uint8_t _id) {
    this->id = _id;
}

uint8_t ToBeSignedCertificate::getId() const {
    return this->id;
}