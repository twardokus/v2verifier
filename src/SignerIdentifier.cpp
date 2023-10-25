//
// Created by Geoff Twardokus on 10/20/23.
//

#include "SignerIdentifier.h"

SignerIdentifier::SignerIdentifier(SignerIdentifier& _signerIdentifier) {
    this->identifierChoice = _signerIdentifier.getIdentifierChoice();
    this->digest = OctetString(_signerIdentifier.getDigest());
}

SignerIdentifier::SignerIdentifier(signerIdentifierChoice _idType, OctetString &_digest) {
    this->identifierChoice = _idType;
    this->digest = OctetString(_digest);
}

signerIdentifierChoice SignerIdentifier::getIdentifierChoice() const {
    return this->identifierChoice;
}

OctetString SignerIdentifier::getDigest() const {
    return this->digest;
}
