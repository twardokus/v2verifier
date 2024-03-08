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
    std::vector<std::byte> getCOER() {

        std::vector<std::byte> coerBytes;


        if(this->contentChoice == IEEE1609Dot2ContentChoice::unsecuredData) {
            coerBytes.push_back(std::byte{0x80} | std::byte{(uint8_t) IEEE1609Dot2ContentChoice::unsecuredData});
            auto contentBytes = this->unsecuredData.getCOER();
            coerBytes.insert(coerBytes.end(), contentBytes.begin(), contentBytes.end());

            return coerBytes;
        }
        else if(this->contentChoice == IEEE1609Dot2ContentChoice::signedData) {
            coerBytes.push_back(std::byte{0x80} | std::byte{(uint8_t) IEEE1609Dot2ContentChoice::signedData});
            auto contentBytes = this->signedData.getCOER();
            coerBytes.insert(coerBytes.end(), contentBytes.begin(), contentBytes.end());

            return coerBytes;
        }
        else {
            throw std::runtime_error("Somehow this got an invalid content type. Aborting.");
        }
    }

    [[nodiscard]] IEEE1609Dot2ContentChoice getContentChoice() const {
        return this->contentChoice;
    }

private:
    IEEE1609Dot2ContentChoice contentChoice;
    SignedData signedData;
    UnsecuredData unsecuredData;
};

#endif //V2VERIFIER_IEEE1609DOT2CONTENT_HPP
