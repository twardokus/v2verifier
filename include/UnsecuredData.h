//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_UNSECUREDDATA_H
#define V2VERIFIER_UNSECUREDDATA_H


#include "OctetString.h"
#include "Ieee1609Dot2Content.h"

class UnsecuredData : Ieee1609Dot2Content {

public:

    UnsecuredData() = default;
    UnsecuredData(UnsecuredData& _data);

    UnsecuredData(OctetString _unsecuredData) {
        this->unsecuredData = OctetString(_unsecuredData);
    }
    OctetString getUnsecuredData();
    void setUnsecuredData(OctetString _unsecuredData);

private:
    OctetString unsecuredData;

};


#endif //V2VERIFIER_UNSECUREDDATA_H
