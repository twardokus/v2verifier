/** @file   EcdsaP256Signature.hpp
 *  @brief  Implementation of the EcdsaP256Signature ASN.1 structure defined in IEEE 1609.2-2022.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */


//EcdsaP256Signature ::= SEQUENCE {
//    rSig EccP256CurvePoint,
//    sSig OCTET STRING (SIZE (32))
//}


#ifndef V2VERIFIER_ECDSAP256SIGNATURE_HPP
#define V2VERIFIER_ECDSAP256SIGNATURE_HPP

#include "V2XMessage.hpp"
#include "EccP256CurvePoint.hpp"

class EcdsaP256Signature {

public:

    /** @brief Size of the COER-encoded byte string for this object */
    static const uint16_t ECDSAP256_SIGNATURE_SIZE_BYTES = EccP256CurvePoint::ECC_P256_CURVE_POINT_SIZE_BYTES + 32;

    /** @brief Default constructor */
    EcdsaP256Signature() = default;

    /** @brief Create a new EcdsaP256Signature from a COER-encoded byte string
     *
     *  @param coerBytes COER encoding of the structure as a byte string
     */
    EcdsaP256Signature(std::vector<std::byte> &coerBytes) {
        if(coerBytes.size() == ECDSAP256_SIGNATURE_SIZE_BYTES) {

            std::vector<std::byte> rSigBytes;
            rSigBytes.insert(rSigBytes.end(), coerBytes.begin(), coerBytes.begin() + EccP256CurvePoint::ECC_P256_CURVE_POINT_SIZE_BYTES);

            this->rSig = EccP256CurvePoint(rSigBytes);

            std::vector<std::byte> sSigBytes;
            sSigBytes.insert(sSigBytes.end(), coerBytes.begin() + EccP256CurvePoint::ECC_P256_CURVE_POINT_SIZE_BYTES, coerBytes.end());

            this->sSig = sSigBytes;

        }
        else {
            throw std::runtime_error("Invalid length COER passed for ECDSAP256Signature");
        }
    }

    /** @brief Get the COER encoding of the object as a byte string.
     *
     *  @return The COER encoding of the object.
     */
    std::vector<std::byte> getCOER() {

        std::vector<std::byte> coerBytes;

        auto rSigBytes = rSig.getCOER();

        coerBytes.insert(coerBytes.end(), rSigBytes.begin(), rSigBytes.end());
        coerBytes.insert(coerBytes.end(), this->sSig.begin(), this->sSig.end());

        return coerBytes;
    }

    /** @brief Get the rSig value for this signature.
     *
     *  @return The rSig value (an EccP256CurvePoint) for this signature.
     */
    EccP256CurvePoint getRSig() const {
        return this->rSig;
    }

    /** @brief Get the sSig value for this signature.
     *
     *  @return The sSig value (a 32-byte integer) for this signature.
     */
    std::vector<std::byte> getSSig() const {
        return this->sSig;
    }


private:
    EccP256CurvePoint rSig;
    std::vector<std::byte> sSig;

};
#endif //V2VERIFIER_ECDSAP256SIGNATURE_HPP
