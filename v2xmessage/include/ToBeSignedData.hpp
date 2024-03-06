//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_TOBESIGNEDDATA_HPP
#define V2VERIFIER_TOBESIGNEDDATA_HPP

/*
ToBeSignedData ::= SEQUENCE {
  payload    SignedDataPayload,
  headerInfo HeaderInfo
}
*/

#include "SignedDataPayload.hpp"
#include "V2XMessage.hpp"
#include "HeaderInfo.hpp"

class ToBeSignedData : V2XMessage {

public:

    ToBeSignedData() = default;
    ToBeSignedData(std::vector<std::byte> &coerBytes) {

    }
    std::vector<std::byte> getCOER() {}

private:
    SignedDataPayload payload;
    HeaderInfo headerInfo;

};

#endif //V2VERIFIER_TOBESIGNEDDATA_HPP
