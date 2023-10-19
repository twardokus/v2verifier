//
// Created by Geoff Twardokus on 10/19/23.
//

#include "UnsecuredData.h"

OctetString UnsecuredData::getUnsecuredData() {
    return {this->unsecuredData};
}

void UnsecuredData::setUnsecuredData(OctetString _unsecuredData) {
    this->unsecuredData = OctetString(_unsecuredData);
}
