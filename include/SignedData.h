//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_SIGNEDDATA_H
#define V2VERIFIER_SIGNEDDATA_H

#include "HashAlgorithm.h"
#include "Ieee1609Dot2Content.h"
#include "ToBeSignedData.h"

class SignedData : Ieee1609Dot2Content{

private:
    HashAlgorithm hashId;
    ToBeSignedData tbsData;
//    SignerIdentifier signer;
//    Signature signature;

};


#endif //V2VERIFIER_SIGNEDDATA_H
