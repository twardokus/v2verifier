//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_IEEE1609DOT2DATA_HPP
#define V2VERIFIER_IEEE1609DOT2DATA_HPP

#include "V2XMessage.hpp"

class IEEE1609Dot2Data : V2XMessage {

public:

    IEEE1609Dot2Data() = default;
    IEEE1609Dot2Data(const std::vector<std::byte> &coerBytes) {
        this->protocolVersion = (uint8_t) coerBytes.at(0);
    }

    std::vector<std::byte> getCOER() {};

    [[nodiscard]] uint8_t getProtocolVersion() const {
        return this->protocolVersion;
    }

private:
    uint8_t protocolVersion;



};

#endif //V2VERIFIER_IEEE1609DOT2DATA_HPP
