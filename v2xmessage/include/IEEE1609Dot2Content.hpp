//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_IEEE1609DOT2CONTENT_HPP
#define V2VERIFIER_IEEE1609DOT2CONTENT_HPP

#include "SignedData.hpp"
#include "V2XMessage.hpp"
#include "UnsecuredData.hpp"


enum IEEE1609Dot2ContentChoice {
    unsecuredData,
    signedData,
    encryptedData,
    signedCertificateRequest
};

class IEEE1609Dot2Content : V2XMessage {

public:
    IEEE1609Dot2Content() = default;
    IEEE1609Dot2Content(std::vector<std::byte> &coerBytes);
    std::vector<std::byte> getCOER() {};

    [[nodiscard]] IEEE1609Dot2ContentChoice getContentChoice() const {
        return this->contentChoice;
    }

private:
    IEEE1609Dot2ContentChoice contentChoice;
    SignedData signedData;
    UnsecuredData unsecuredData;
};

#endif //V2VERIFIER_IEEE1609DOT2CONTENT_HPP
