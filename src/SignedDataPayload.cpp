//
// Created by Geoff Twardokus on 10/19/23.
//

#include "SignedDataPayload.h"

SignedDataPayload::SignedDataPayload(Ieee1609Dot2Data &_data) {

}

Ieee1609Dot2Data SignedDataPayload::getData() const {
    return this->data;
}
