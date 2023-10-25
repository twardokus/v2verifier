//
// Created by Geoff Twardokus on 10/25/23.
//

#include "CertificateBase.h"

CertificateBase::CertificateBase(CertificateBase &_certBase) {
    this->type = _certBase.getCertificateType();
}

CertificateBase::CertificateBase(certificateType _type) {
    this->type = _type;
}

certificateType CertificateBase::getCertificateType() const {
    return this->type;
}

ToBeSignedCertificate CertificateBase::getCertificate() const {
    return this->toBeSigned;
}
