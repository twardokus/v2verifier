//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_SIGNEDDATA_H
#define V2VERIFIER_SIGNEDDATA_H

#include "HashAlgorithm.h"
#include "ToBeSignedData.h"
#include "SignerIdentifier.h"

class SignedData {

    SignedData() = default;


private:
    /** Always SHA-256 by default */
    HashAlgorithm hashId = sha256;
    ToBeSignedData tbsData;
    SignerIdentifier signer;
    // TODO: Signature signature;

};


#endif //V2VERIFIER_SIGNEDDATA_H
