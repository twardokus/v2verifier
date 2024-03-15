/** @file   IEEE1609Dot2Data.hpp
 *  @brief  Implementation of the Ieee1609Dot2Data ASN.1 structure defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#ifndef V2VERIFIER_IEEE1609DOT2DATA_HPP
#define V2VERIFIER_IEEE1609DOT2DATA_HPP

#include "V2XMessage.hpp"
#include "IEEE1609Dot2Content.hpp"

class IEEE1609Dot2Data : V2XMessage {

public:

    /** @brief Default constructor. */
    IEEE1609Dot2Data() = default;

    /** @brief Create a new IEEE1609Dot2Data from a COER-encoded byte string
     *
     *  @param coerBytes The COER-encoded byte string used to create the object.
     */
    IEEE1609Dot2Data(const std::vector<std::byte> &coerBytes) {
        this->protocolVersion = (uint8_t) coerBytes.at(0);
        std::vector<std::byte> contentBytes;
        contentBytes.insert(contentBytes.end(), coerBytes.begin() + 1, coerBytes.end());
        this->content = IEEE1609Dot2Content(contentBytes);
    }

    /** @brief Get the COER encoding of this object.
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {

        std::vector<std::byte> coerBytes;

        auto contentBytes = this->content.getCOER();

        coerBytes.push_back(std::byte{0x3});
        coerBytes.insert(coerBytes.end(), contentBytes.begin(), contentBytes.end());

        return coerBytes;
    };

    /** @brief Get the protocol version.
     *
     *  @return The protocol version.
     */
    [[nodiscard]] uint8_t getProtocolVersion() const {
        return this->protocolVersion;
    }

    /** @brief Get the encapsulated IEEE1609Dot2Content object.
     *
     *  @return The IEEE1609Dot2Content object contained within this object.
     */
    [[nodiscard]] IEEE1609Dot2Content getContent() const {
        return this->content;
    }

private:
    uint8_t protocolVersion;
    IEEE1609Dot2Content content;
};

#endif //V2VERIFIER_IEEE1609DOT2DATA_HPP
