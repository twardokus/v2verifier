/** @file   UnsecuredData.hpp
 *  @brief  Implementation of the UnsecuredData ASN.1 structure defined in IEEE1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#ifndef V2VERIFIER_UNSECUREDDATA_HPP
#define V2VERIFIER_UNSECUREDDATA_HPP

#include "V2XMessage.hpp"

class UnsecuredData : V2XMessage {

public:
    /** @brief Default constructor. */
    UnsecuredData() = default;

    /** @brief Create a new UnsecuredData from a COER encoding.
     *
     *  @param coerBytes The COER encoding of the object.
     */
    UnsecuredData(std::vector<std::byte> &coerBytes) {
        this->opaqueData = coerBytes;
    }

    /** @brief Get the COER encoding of the object.
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {
        std::vector<std::byte> coerBytes;
        auto opaqueBytes = this->opaqueData;
        coerBytes.insert(coerBytes.end(), opaqueBytes.begin(), opaqueBytes.end());
        return coerBytes;
    }

private:
    std::vector<std::byte> opaqueData;

};

#endif //V2VERIFIER_UNSECUREDDATA_HPP
