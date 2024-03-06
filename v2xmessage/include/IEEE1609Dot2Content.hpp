//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_IEEE1609DOT2CONTENT_HPP
#define V2VERIFIER_IEEE1609DOT2CONTENT_HPP

#include "V2XMessage.hpp"

enum IEEE1609Dot2ContentChoice {
    unsecuredData,
    signedData,
    encryptedData,
    signedCertificateRequest
};

class IEEE1609Dot2Content : V2XMessage {

public:
    IEEE1609Dot2Content(const std::vector<std::byte> &coerBytes) {
        std::byte choiceTag = coerBytes.at(0);

        // Get the content type choice from the first octet

        /** Make sure the MSB of the first octet is set to indicate a context-specific tag number (see ITU-T Rec. X.696
         *  Clause 8.7.2.1)
         */
        if((choiceTag & std::byte{0b1000000}) == std::byte{0b10000000}) {
            auto tag = (uint8_t) (choiceTag & std::byte{0b00111111});
            if(0 <= tag && tag <= 3) {
                /* TODO eventually - implement other types. */
                this->contentChoice = IEEE1609Dot2ContentChoice(tag);
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

private:
    IEEE1609Dot2ContentChoice contentChoice;

};

#endif //V2VERIFIER_IEEE1609DOT2CONTENT_HPP
