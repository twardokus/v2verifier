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
    IEEE1609Dot2Content(std::vector<std::byte> &coerBytes) {
        std::byte choiceTag = coerBytes.at(0);

        // Get the content type choice from the first octet

        if((choiceTag & std::byte{0b10000000}) == std::byte{0b10000000}) {
            /** Make sure the MSB of the first octet is set to indicate a context-specific tag number, then get the
             *  specific tag number from bits 1-6 (see ITU-T Rec. X.696 Clause 8.7.2.1)
             */
            auto tag = (uint8_t) (choiceTag & std::byte{0b00111111});
            if(0 <= tag && tag <= 3) {

                this->contentChoice = IEEE1609Dot2ContentChoice(tag);
                auto newCOER = std::vector<std::byte>(coerBytes.begin() + 1, coerBytes.end());

                switch(this->contentChoice) {

                case IEEE1609Dot2ContentChoice::unsecuredData:
                    this->unsecuredData = UnsecuredData(newCOER);
                    break;
                case IEEE1609Dot2ContentChoice::signedData:
                    this->signedData = SignedData(newCOER);
                    break;

                // For now, we only support unsecuredData and signedData. TODO: eventually - implement other types.
                case IEEE1609Dot2ContentChoice::encryptedData:
                case IEEE1609Dot2ContentChoice::signedCertificateRequest:
                default:
                throw   std::runtime_error("Unsupported IEEE1609Dot2Content type requested.");
                }
            }
            else {
                throw std::out_of_range("Invalid choice tag number");
            }
        }
        else {
            throw std::runtime_error("Invalid tag value passed to decoder");
        }
    }

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
