/** @file   IEEE1609Dot2Content.hpp
 *  @brief  Implementation of the Ieee1609Dot2Content ASN.1 structure defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs
 */

#ifndef V2VERIFIER_IEEE1609DOT2CONTENT_HPP
#define V2VERIFIER_IEEE1609DOT2CONTENT_HPP

#include "SignedData.hpp"
#include "V2XMessage.hpp"
#include "UnsecuredData.hpp"

/** @brief The type of content contained in this SPDU */
enum IEEE1609Dot2ContentChoice {
    unsecuredData,             ///< an arbitrary byte string of variable length
    signedData,                ///< a SignedData
    encryptedData,             ///< a EncryptedData
    signedCertificateRequest   ///< a SignedCertificateRequest
};

class IEEE1609Dot2Content : V2XMessage {

public:
    /** @brief Default constructor. */
    IEEE1609Dot2Content() = default;

    /** @brief  Create a new IEEE1609Dot2Content from a COER-encoded byte string.
     *
     *  @param coerBytes The COER encoding use to create the object.
     */
    IEEE1609Dot2Content(std::vector<std::byte> &coerBytes) {
        std::byte choiceTag = coerBytes.at(0);

        // Get the content type choice from the first octet

        if((choiceTag & std::byte{0b10000000}) == std::byte{0b10000000}) {
            //  Make sure the MSB of the first octet is set to indicate a context-specific tag number, then get the
            //  specific tag number from bits 1-6 (see ITU-T Rec. X.696 Clause 8.7.2.1).
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
