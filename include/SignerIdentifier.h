//
// Created by Geoff Twardokus on 10/20/23.
//

#ifndef V2VERIFIER_SIGNERIDENTIFIER_H
#define V2VERIFIER_SIGNERIDENTIFIER_H

#include "OctetString.h"
#include "CertificateBase.h"

enum signerIdentifierChoice{
    digest,
    certificate,
    self
};

class SignerIdentifier {

public:
    SignerIdentifier() = default;
    SignerIdentifier(SignerIdentifier& _signerIdentifier);
    SignerIdentifier(signerIdentifierChoice _idType, OctetString& _digest);

    signerIdentifierChoice getIdentifierChoice() const;
    OctetString getDigest() const;

private:
    signerIdentifierChoice identifierChoice;
    OctetString digest;
    std::vector<CertificateBase> certificate;

};


#endif //V2VERIFIER_SIGNERIDENTIFIER_H
