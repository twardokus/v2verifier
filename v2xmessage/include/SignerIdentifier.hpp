//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_SIGNERIDENTIFIER_HPP
#define V2VERIFIER_SIGNERIDENTIFIER_HPP

#include "V2XMessage.hpp"

class SignerIdentifier : V2XMessage {

public:
    SignerIdentifier() = default;
    SignerIdentifier(std::vector<std::byte> &coerBytes) {

    }

    std::vector<std::byte> getCOER() {}


};
#endif //V2VERIFIER_SIGNERIDENTIFIER_HPP
