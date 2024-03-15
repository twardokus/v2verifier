/** @file   HeaderInfo.hpp
 *  @brief  Implementation of the HeaderInfo ASN.1 structure defined in IEEE 1609.2-2022
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs
 */
#ifndef V2VERIFIER_HEADERINFO_HPP
#define V2VERIFIER_HEADERINFO_HPP

//HeaderInfo ::= SEQUENCE {
//    psid                  Psid,
//    generationTime        Time64 OPTIONAL,
//    expiryTime            Time64 OPTIONAL,
//    generationLocation    ThreeDLocation OPTIONAL,
//    p2pcdLearningRequest  HashedId3 OPTIONAL,
//    missingCrlIdentifier  MissingCrlIdentifier OPTIONAL,
//    encryptionKey         EncryptionKey OPTIONAL,
//    ...,
//    inlineP2pcdRequest    SequenceOfHashedId3 OPTIONAL,
//    requestedCertificate  Certificate OPTIONAL,
//    pduFunctionalType     PduFunctionalType OPTIONAL,
//    contributedExtensions ContributedExtensionBlocks OPTIONAL
//}


#include "V2XMessage.hpp"

class HeaderInfo : V2XMessage {

public:

    /** @brief The size of the COER-encoded byte string for this object */
    static const uint16_t HEADERINFO_SIZE_BYTES = 20;

    /** @brief Default constructor. */
    HeaderInfo() = default;

    /** @brief Create a new HeaderInfo from a COER-encoded byte string */
    HeaderInfo(std::vector<std::byte> &coerBytes) {

        if(coerBytes.size() == HEADERINFO_SIZE_BYTES) {
            std::memcpy(&psid, coerBytes.data(), sizeof(std::uint32_t));
            std::memcpy(&generationTime, coerBytes.data() + 4, sizeof(std::uint64_t));
            std::memcpy(&expiryTime, coerBytes.data() + 12, sizeof(std::uint64_t));
        }
        else {
            throw std::runtime_error("Invalid data for HeaderInfo");
        }

    }

    /** @brief Get the COER encoding of this object as a byte string
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {

        std::vector<std::byte> coerBytes;

        auto psidBytes = Utility::vectorFromUint32(this->psid);
        auto generationTimeBytes = Utility::vectorFromUint64(this->generationTime);
        auto expiryTimeBytes = Utility::vectorFromUint64(this->expiryTime);

        coerBytes.insert(coerBytes.end(), psidBytes.begin(), psidBytes.end());
        coerBytes.insert(coerBytes.end(), generationTimeBytes.begin(), generationTimeBytes.end());
        coerBytes.insert(coerBytes.end(), expiryTimeBytes.begin(), expiryTimeBytes.end());

        return coerBytes;
    }

    /** @brief Get the PSID value
     *
     *  @return The PSID value.
     */
    [[nodiscard]] uint32_t getPsid() const {
        return this->psid;
    }

    /** @brief  Get the generation time
     *
     *  @return The generation time.
     */
    [[nodiscard]] uint64_t getGenerationTime() const {
        return this->generationTime;
    }

    /** @brief Get the expiration time
     *
     *  @return The expiration time.
     */
    [[nodiscard]] uint64_t getExpiryTime() const {
        return this->expiryTime;
    }

private:

    uint32_t psid;              // This is a 4-octet word under ASN.1 encoding rules
    uint64_t generationTime;    // This is an 8-octet word under ASN.1 encoding rules
    uint64_t expiryTime;        // This is an 8-octet word under ASN.1 encoding rules

};

#endif //V2VERIFIER_HEADERINFO_HPP
