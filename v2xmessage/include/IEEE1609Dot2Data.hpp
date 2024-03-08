//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_IEEE1609DOT2DATA_HPP
#define V2VERIFIER_IEEE1609DOT2DATA_HPP

#include "V2XMessage.hpp"
#include "IEEE1609Dot2Content.hpp"

class IEEE1609Dot2Data : V2XMessage {

public:

    IEEE1609Dot2Data() = default;
    IEEE1609Dot2Data(const std::vector<std::byte> &coerBytes) {
        this->protocolVersion = (uint8_t) coerBytes.at(0);
        std::vector<std::byte> contentBytes;
        contentBytes.insert(contentBytes.end(), coerBytes.begin() + 1, coerBytes.end());
        this->content = IEEE1609Dot2Content(contentBytes);
    }

    std::vector<std::byte> getCOER() {

        std::vector<std::byte> coerBytes;

        auto contentBytes = this->content.getCOER();

        coerBytes.push_back(std::byte{0x3});
        coerBytes.insert(coerBytes.end(), contentBytes.begin(), contentBytes.end());

        return coerBytes;
    };

    [[nodiscard]] uint8_t getProtocolVersion() const {
        return this->protocolVersion;
    }

    [[nodiscard]] IEEE1609Dot2Content getContent() const {
        return this->content;
    }

private:
    uint8_t protocolVersion;
    IEEE1609Dot2Content content;
};

#endif //V2VERIFIER_IEEE1609DOT2DATA_HPP
