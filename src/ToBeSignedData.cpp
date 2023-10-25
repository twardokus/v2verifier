//
// Created by Geoff Twardokus on 10/19/23.
//

#include "ToBeSignedData.h"

ToBeSignedData::ToBeSignedData(Ieee1609Dot2Data& _payload) {
    this->payload = Ieee1609Dot2Data(_payload);
}