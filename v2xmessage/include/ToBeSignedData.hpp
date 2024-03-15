/** @file   ToBeSignedData.hpp
 *  @brief  Implementation of the ToBeSignedData ASN.1 structure defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#ifndef V2VERIFIER_TOBESIGNEDDATA_HPP
#define V2VERIFIER_TOBESIGNEDDATA_HPP

//ToBeSignedData ::= SEQUENCE {
//  payload    SignedDataPayload,
//  headerInfo HeaderInfo
//}

#include "SignedDataPayload.hpp"
#include "V2XMessage.hpp"
#include "HeaderInfo.hpp"

class ToBeSignedData : V2XMessage {

public:

    /** @brief Default constructor. */
    ToBeSignedData() = default;

    /** @brief Create a new ToBeSignedData from a COER encoding.
     *
     *  @param coerBytes The COER encoding from which to create a new object.
     */
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

    /** @brief Get the COER encoding of the object.
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;

        auto tempPayloadBytes = this->payload.getCOER();
        auto tempHeaderInfoBytes = this->headerInfo.getCOER();

        coerBytes.insert(coerBytes.end(), tempPayloadBytes.begin(), tempPayloadBytes.end());
        coerBytes.insert(coerBytes.end(), tempHeaderInfoBytes.begin(), tempHeaderInfoBytes.end());

        return coerBytes;
    }

    /** @brief Get the payload (SignedDataPayload) contained in this object.
     *
     *  @return The payload of the object.
     */
    SignedDataPayload getPayload() const {
        return this->payload;
    }

    /** @brief Get the header info (HeaderInfo) for this object.
     *
     *  @return The header information for this object.
     */
    HeaderInfo getHeaderInfo() const {
        return this->headerInfo;
    }

private:
    SignedDataPayload payload;
    HeaderInfo headerInfo;

};

#endif //V2VERIFIER_TOBESIGNEDDATA_HPP
