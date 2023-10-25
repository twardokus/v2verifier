//
// Created by Geoff Twardokus on 10/25/23.
//

#ifndef V2VERIFIER_TOBESIGNEDCERTIFICATE_H
#define V2VERIFIER_TOBESIGNEDCERTIFICATE_H

#include <cstdint>

#include "OctetString.h"

class ToBeSignedCertificate {

public:
    ToBeSignedCertificate() = default;
    ToBeSignedCertificate(uint8_t _id);

    uint8_t getId() const;

private:
    uint8_t id; // TODO: Implement actual certificate ID options. Simple integer for now.

    /* TODO: need to add all the certificate fields. They are not critical (yet)
     * and will be implemented at a date TBD. */
};


#endif //V2VERIFIER_TOBESIGNEDCERTIFICATE_H
