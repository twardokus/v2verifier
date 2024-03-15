/** @file   SignedDataPayload.hpp
 *  @brief  Implementation of the SignedDataPayload ASN.1 structure defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#ifndef V2VERIFIER_SIGNEDDATAPAYLOAD_HPP
#define V2VERIFIER_SIGNEDDATAPAYLOAD_HPP


//SignedDataPayload ::= SEQUENCE {
//  data        Ieee1609Dot2Data OPTIONAL,
//  extDataHash HashedData OPTIONAL,
//  ...,
//  omitted     NULL OPTIONAL
//} (WITH COMPONENTS {..., data PRESENT} |
//   WITH COMPONENTS {..., extDataHash PRESENT} |
//   WITH COMPONENTS {..., omitted PRESENT})


#include "V2XMessage.hpp"


class SignedDataPayload : V2XMessage {

public:
    /** @brief Default constructor. */
    SignedDataPayload() = default;

    /** @brief Create a new SignedDataPayload from a COER encoding.
     *
     *  @param coerBytes The COER encoding from which to create the object.
     */
    SignedDataPayload(std::vector<std::byte> &coerBytes) {
        this->data = coerBytes;
    }

    /** @brief Get the COER encoding of the object.
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {
        return this->data;
    }

    /** @brief Get the data contained in this object.
     *
     *  This is supposed to be IEEE1609Dot2Data under IEEE 1609.2; however, that creates a circular inheritance problem
     *  in C++. Since in practice this substructure would just contain an UnsecuredData object, which itself is just
     *  an OPAQUE octet string of indefinite length, we skip the substructure here and directly encapsulate a byte
     *  string of indefinitely length in this object.
     *
     * @return The data (as bytes) contained in this object.
     */
    std::vector<std::byte> getData() const {
        return this->data;
    }

private:
    std::vector<std::byte> data;    // This is technically supposed to be IEEE1609Dot2Data, but that causes no end of
                                    // circular inheritance issues, so just put the data here. Only omits a byte of
                                    // "real" COER because the skipped substructure has a single byte indicating
                                    // protocol version (which is fixed at 3 anyway) and then the octet string here.
};

#endif //V2VERIFIER_SIGNEDDATAPAYLOAD_HPP
