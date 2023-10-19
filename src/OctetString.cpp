//
// Created by Geoff Twardokus on 10/19/23.
//

#include "OctetString.h"

const std::vector<uint8_t> &OctetString::getData() {
    return this->data;
}

void OctetString::setData(std::vector<uint8_t> _data) {
    this->data = _data;
}
