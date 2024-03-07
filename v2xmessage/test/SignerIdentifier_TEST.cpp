//
// Created by Geoff Twardokus on 3/7/24.
//

#include "../include/SignerIdentifier.hpp"

int main() {

    std::vector<std::byte> testIdentifier;
    testIdentifier.push_back(std::byte{0x82});

    SignerIdentifier s(testIdentifier);

    if(s.getSignerIdentifierChoice() != SignerIdentifierChoice::self)
        return 1;

    if(s.getCOER() != testIdentifier)
        return 2;

    return 0;
}