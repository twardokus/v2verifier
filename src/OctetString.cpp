//
// Created by Geoff Twardokus on 10/19/23.
//

#include "OctetString.h"

#include <utility>

OctetString::OctetString(OctetString& _octetString) {
    this->data = _octetString.getData();
}

OctetString::OctetString(const OctetString& octetString) {
    this->data = octetString.getData();
}

OctetString::OctetString(std::vector<uint8_t> _data) {
    this->data = std::move(_data);
}

void OctetString::setData(std::vector<uint8_t> _data) {
    this->data = std::move(_data);
}

std::vector<uint8_t> OctetString::getData() const {
    return this->data;
}
