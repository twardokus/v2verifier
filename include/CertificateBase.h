//
// Created by Geoff Twardokus on 10/25/23.
//

#ifndef V2VERIFIER_CERTIFICATEBASE_H
#define V2VERIFIER_CERTIFICATEBASE_H


#include <cstdint>
#include "ToBeSignedCertificate.h"

enum certificateType {
    expl,
    impl
};

class CertificateBase {
public:
    CertificateBase() = default;
    CertificateBase(CertificateBase &_certBase);
    CertificateBase(certificateType _type);

    certificateType getCertificateType() const;
    ToBeSignedCertificate getCertificate() const;

private:
    uint8_t version = 3;
    certificateType type;
    // TODO: IssuerIdentifier
    ToBeSignedCertificate toBeSigned;
    // TODO: Signature signature;
};


#endif //V2VERIFIER_CERTIFICATEBASE_H
