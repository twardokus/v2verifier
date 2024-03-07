//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_SIGNEDDATAPAYLOAD_HPP
#define V2VERIFIER_SIGNEDDATAPAYLOAD_HPP

/*
SignedDataPayload ::= SEQUENCE {
  data        Ieee1609Dot2Data OPTIONAL,
  extDataHash HashedData OPTIONAL,
  ...,
  omitted     NULL OPTIONAL
} (WITH COMPONENTS {..., data PRESENT} |
   WITH COMPONENTS {..., extDataHash PRESENT} |
   WITH COMPONENTS {..., omitted PRESENT})
*/

#include "V2XMessage.hpp"
//#include "IEEE1609Dot2Data.hpp"


class SignedDataPayload : V2XMessage {

public:
    SignedDataPayload() = default;
    SignedDataPayload(std::vector<std::byte> &coerBytes) {

    }
    std::vector<std::byte> getCOER() {}

private:
    std::vector<std::byte> data;    // This is technically supposed to be IEEE1609Dot2Data, but that causes no end of
                                    // circular inheritance issues, so just put the data here. Only omits a byte of
                                    // "real" COER because the skipped substructure has a single byte indicating
                                    // protocol version (which is fixed at 3 anyway) and then the octet string here.
};

#endif //V2VERIFIER_SIGNEDDATAPAYLOAD_HPP
