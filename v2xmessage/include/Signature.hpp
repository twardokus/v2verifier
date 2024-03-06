//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_SIGNATURE_HPP
#define V2VERIFIER_SIGNATURE_HPP

#include "V2XMessage.hpp"

class Signature : V2XMessage {

public:
    Signature() = default;
    Signature(std::vector<std::byte> &coerBytes) {

    }

    std::vector<std::byte> getCOER() {}

};

#endif //V2VERIFIER_SIGNATURE_HPP
