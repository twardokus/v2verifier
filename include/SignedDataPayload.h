//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_SIGNEDDATAPAYLOAD_H
#define V2VERIFIER_SIGNEDDATAPAYLOAD_H


#include "Ieee1609Dot2Data.h"

class SignedDataPayload {

public:
    SignedDataPayload(Ieee1609Dot2Data& _data);

private:
    Ieee1609Dot2Data data;
};


#endif //V2VERIFIER_SIGNEDDATAPAYLOAD_H
