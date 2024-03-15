/** @file   IEEE1609Dot2DataTypes.hpp
 *  @brief  Namespace definitions for ASN.1 types defined in IEEE 1609.2-2022 and reused throughout other data
 *          structures.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#ifndef V2VERIFIER_IEEE1609DOT2DATATYPES_HPP
#define V2VERIFIER_IEEE1609DOT2DATATYPES_HPP

//! Data types defined by IEEE 1609.2-2022 that are reused throughout the project.
namespace IEEE1609Dot2DataTypes {

    /** @brief HashAlgorithm ASN.1 structure defined in IEEE 1609.2-2022. */
    enum HashAlgorithm {
        sha256, ///< SHA-256
        sha384, ///< SHA-384
        sm3     ///< SM3 (Chinese variant of SHA)
    };

}

#endif //V2VERIFIER_IEEE1609DOT2DATATYPES_HPP
