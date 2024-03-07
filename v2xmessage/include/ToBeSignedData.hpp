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

        std::vector<std::byte> headerInfoBytes;
        headerInfoBytes.reserve(HeaderInfo::HEADERINFO_SIZE_BYTES);
        headerInfoBytes.assign(HeaderInfo::HEADERINFO_SIZE_BYTES, std::byte{0});

        std::vector<std::byte> signedDataPayloadBytes;
        signedDataPayloadBytes.reserve(coerBytes.size() - HeaderInfo::HEADERINFO_SIZE_BYTES);
        signedDataPayloadBytes.assign(coerBytes.size() - HeaderInfo::HEADERINFO_SIZE_BYTES, std::byte{0});

        std::memcpy(headerInfoBytes.data(),
                    coerBytes.data() + (coerBytes.size() - HeaderInfo::HEADERINFO_SIZE_BYTES),
                    HeaderInfo::HEADERINFO_SIZE_BYTES);

        std::memcpy(signedDataPayloadBytes.data(),
                    coerBytes.data(),
                    coerBytes.size() - HeaderInfo::HEADERINFO_SIZE_BYTES);

        this->headerInfo = HeaderInfo(headerInfoBytes);
        this->payload = SignedDataPayload(signedDataPayloadBytes);

    }
    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;

        auto tempPayloadBytes = this->payload.getCOER();
        auto tempHeaderInfoBytes = this->headerInfo.getCOER();

        coerBytes.insert(coerBytes.end(), tempPayloadBytes.begin(), tempPayloadBytes.end());
        coerBytes.insert(coerBytes.end(), tempHeaderInfoBytes.begin(), tempHeaderInfoBytes.end());

        return coerBytes;
    }

    SignedDataPayload getPayload() const {
        return this->payload;
    }

    HeaderInfo getHeaderInfo() const {
        return this->headerInfo;
    }

private:
    SignedDataPayload payload;
    HeaderInfo headerInfo;

};

#endif //V2VERIFIER_TOBESIGNEDDATA_HPP
