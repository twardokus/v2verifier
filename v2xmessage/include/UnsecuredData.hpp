//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_UNSECUREDDATA_HPP
#define V2VERIFIER_UNSECUREDDATA_HPP

#include "V2XMessage.hpp"

class UnsecuredData : V2XMessage {

public:
    UnsecuredData() = default;
    UnsecuredData(std::vector<std::byte> &coerBytes) {
        this->opaqueData = coerBytes;
    }

    std::vector<std::byte> getCOER() {}

private:
    std::vector<std::byte> opaqueData;

};

#endif //V2VERIFIER_UNSECUREDDATA_HPP