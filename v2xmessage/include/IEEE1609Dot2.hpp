/** @file   IEEE1609Dot2.cpp
 *  @brief  Implementation of IEEE 1609.2 security structures and functions.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#ifndef V2VERIFIER_IEEE1609DOT2_HPP
#define V2VERIFIER_IEEE1609DOT2_HPP

#include <cstdint>
#include <vector>

#include "Utility.hpp"

namespace IEEE1609Dot2 {

    /** @brief The type of content contained in an SPDU */
    enum IEEE1609Dot2ContentChoice {
        unsecuredData,             ///< an arbitrary byte string of variable length
        signedData,                ///< a SignedData
        encryptedData,             ///< a EncryptedData
        signedCertificateRequest   ///< a SignedCertificateRequest
    };

    /** @brief HashAlgorithm ASN.1 structure defined in IEEE 1609.2-2022. */
    enum HashAlgorithm {
        sha256, ///< SHA-256
        sha384, ///< SHA-384
        sm3     ///< SM3 (Chinese variant of SHA)
    };

    /** @brief SignatureChoice ASN.1 structure defined in IEEE 1609.2-2022. */
    enum SignatureChoice {
        ecdsaNistP256Signature,         ///< ECDSA with the NIST P.256 curve
        ecdsaBrainpoolP256r1Signature,  ///< ECDSA with the Brainpool P256r1 curve
        ecdsaBrainpoolP384r1Signature,  ///< ECDSA with the Brainpool P384r1 curve
        ecdsaNistP384Signature,         ///< ECDSA with the NIST P.384 curve
        sm2Signature                    ///< SM2 (Chinese variant of ECDSA 256)
    };

    /** @brief SignerIdentifierChoice ASN.1 structured defined in IEEE 1609.2-2022. */
    enum SignerIdentifierChoice {
        digest,         ///< A truncated SHA-256 hash digest (HashedID3) of the signer's certificate.
        certificate,    ///< The full signer certificate (as a Certificate).
        self            ///< Self-signed (no credential provided).
    };

    /** @brief Certificate ASN.1 structured defined in IEEE 1609.2-2022. */
    typedef struct Certificate {

    } Certificate;

    /** @brief EccP256CurvePoint ASN.1 structured defined in IEEE 1609.2-2022. */
    typedef struct EccP256CurvePoint {

    } EccP256CurvePoint;

    /** @brief EcdsaP256Signature ASN.1 structured defined in IEEE 1609.2-2022. */
    typedef struct EcdsaP256Signature {
        EccP256CurvePoint rSig;         ///< rSig encoded in EccP256CurvePoint
        std::vector<std::byte> sSig;    ///< sSig value as bytes
    } EcdsaP256Signature;

    /** @brief Signature ASN.1 structured defined in IEEE 1609.2-2022. */
    typedef struct Signature {
        SignatureChoice signatureChoice;        ///< selection of \ref IEEE1609Dot2::signatureChoice
        EcdsaP256Signature ecdsaP256Signature;  ///< signature stored as \ref IEEE1609Dot2::EcdsaP256Signature
    } Signature;

    /** @brief SignerIdentifier ASN.1 structured defined in IEEE 1609.2-2022. */
    typedef struct SignerIdentifier {
        SignerIdentifierChoice signerIdentifierChoice;  ///< selection of signerIdentifier
        std::vector<std::byte> digest;                  ///< hash digest of issuer certificate
        Certificate certificate;                        ///< certificate \ref IEEE1609Dot2::Certificate
    } SignerIdentifier;

    /** @brief HeaderInfo ASN.1 structured defined in IEEE 1609.2-2022. */
    typedef struct HeaderInfo {
        uint8_t psid;               ///< service identifier (0x20 for BSM safety service)
        uint64_t generationTime;    ///< generation time in milliseconds
        uint64_t expiryTime;        ///< expiration time in milliseconds
    } HeaderInfo;

    typedef struct SignedDataPayload {
        std::vector<std::byte> data;
    } SignedDataPayload;

    typedef struct ToBeSignedData {
        SignedDataPayload payload;
        HeaderInfo headerInfo;
    } ToBeSignedData;

    typedef struct SignedData {
        HashAlgorithm hashID;
        ToBeSignedData tbsData;
        SignerIdentifier signer;
        Signature signature;
    } SignedData;

    typedef struct UnsecuredData {
        std::vector<std::byte> payload;
    } UnsecuredData;

    typedef struct IEEE1609Dot2Content {
        IEEE1609Dot2ContentChoice contentChoice;
        SignedData signedData;
        UnsecuredData unsecuredData;
    } IEEE1609Dot2Content;

    typedef struct IEEE1609Dot2Data {

        uint8_t protocol_version;
        IEEE1609Dot2Content content;

    } IEEE1609Dot2Data;
}

namespace IEEE1609Dot2Generation {

    IEEE1609Dot2::IEEE1609Dot2Data generateSPDU(IEEE1609Dot2::IEEE1609Dot2ContentChoice contentChoice,
                                                const std::vector<std::byte> &payload,
                                                const uint32_t psid,
                                                const uint64_t generationTime,
                                                const uint64_t expiryTime,
                                                IEEE1609Dot2::HashAlgorithm hashID,
                                                IEEE1609Dot2::SignerIdentifierChoice signType,
                                                std::vector<std::byte> &certificateDigest,
                                                IEEE1609Dot2::Certificate certificate
                                                ) {
        // Create SPDU object
        IEEE1609Dot2::IEEE1609Dot2Data spdu;
        spdu.protocol_version = 0x03;


        // Create contents structure for the SPDU
        IEEE1609Dot2::IEEE1609Dot2Content spduContent;
        spduContent.contentChoice = contentChoice;

        if(spduContent.contentChoice == IEEE1609Dot2::IEEE1609Dot2ContentChoice::unsecuredData) {
            spduContent.unsecuredData.payload = std::vector<std::byte>(payload);
        }
        else if(spduContent.contentChoice == IEEE1609Dot2::IEEE1609Dot2ContentChoice::signedData) {
            spduContent.signedData.tbsData.headerInfo.psid = psid;
            spduContent.signedData.tbsData.headerInfo.generationTime = generationTime;
            spduContent.signedData.tbsData.headerInfo.expiryTime = expiryTime;
            spduContent.signedData.tbsData.payload.data = payload;

            spduContent.signedData.hashID = hashID;
            spduContent.signedData.signer.signerIdentifierChoice = signType;

            if(signType == IEEE1609Dot2::SignerIdentifierChoice::self) {

            }
            else if(signType == IEEE1609Dot2::SignerIdentifierChoice::digest) {
                spduContent.signedData.signer.digest = certificateDigest;
            }
            else if(signType == IEEE1609Dot2::SignerIdentifierChoice::certificate) {
                spduContent.signedData.signer.certificate = certificate;
            }
            else {
                throw std::runtime_error("Invalid signer type");
            }
        }
        else {
            throw std::runtime_error("Invalid content choice specified");
        }

        spdu.content = spduContent;

        return spdu;
    }

    std::vector<std::byte> encodeSPDU(IEEE1609Dot2::IEEE1609Dot2Data &spdu) {

        std::vector<std::byte> coerBytes;

        // IEEE1609Dot2Data

        coerBytes.push_back(std::byte{spdu.protocol_version}); // protocol version is always 0x03

        // IEEE1609Dot2Content

        uint8_t encodedSPDUType = 0x80 | spdu.content.contentChoice; // Choice for content type
        coerBytes.push_back(std::byte{(encodedSPDUType)});

        if(spdu.content.contentChoice == IEEE1609Dot2::IEEE1609Dot2ContentChoice::unsecuredData) {
            uint8_t encodedLength = spdu.content.unsecuredData.payload.size();
            coerBytes.push_back(std::byte{encodedLength});
            coerBytes.insert(coerBytes.end(),
                             spdu.content.unsecuredData.payload.begin(),
                             spdu.content.unsecuredData.payload.end());
        }
        else if(spdu.content.contentChoice == IEEE1609Dot2::IEEE1609Dot2ContentChoice::signedData) {

            // HashAlgorithm
            uint8_t encodedHashID = spdu.content.signedData.hashID;
            coerBytes.push_back(std::byte{encodedHashID});

            // ToBeSignedData
            coerBytes.push_back(std::byte{(0x40)}); // sequence item separator

            coerBytes.push_back(std::byte{0x03}); // IEEE1609Dot2Data -> protocol version
            coerBytes.push_back(std::byte{0x80}); // IEEE1609Dot2Data -> unsecuredData

            uint8_t encodedLength = spdu.content.signedData.tbsData.payload.data.size();
            coerBytes.push_back(std::byte{encodedLength}); // unsecuredData length

            coerBytes.insert(coerBytes.end(), // unsecuredData payload
                             spdu.content.signedData.tbsData.payload.data.begin(),
                             spdu.content.signedData.tbsData.payload.data.end());


            coerBytes.push_back(std::byte{0x40}); // sequence item separator

            coerBytes.push_back(std::byte{0x02}); // headerInfo -> we use first two optional fields (for times), set flags

            uint8_t encodedPSID = spdu.content.signedData.tbsData.headerInfo.psid;
            coerBytes.push_back(std::byte{encodedPSID}); // headerInfo -> psid

            auto encodedGenerationTime = Utility::vectorFromUint64(spdu.content.signedData.tbsData.headerInfo.generationTime);
            coerBytes.insert(coerBytes.end(), encodedGenerationTime.begin(), encodedGenerationTime.end()); // headerInfo -> generationTime

            auto encodedExpiryTime = Utility::vectorFromUint64(spdu.content.signedData.tbsData.headerInfo.expiryTime);
            coerBytes.insert(coerBytes.end(), encodedExpiryTime.begin(), encodedExpiryTime.end()); // headerInfo -> expiryTime

            // SignerIdentifier
            coerBytes.push_back(std::byte{0x80}); // 0x80 -> self-signed, which we'll treat as null for now (TODO: finish + implement 0x81, certificate, and 0x82, digest)

            // Signature



        }
        else {
            throw std::runtime_error("Invalid content choice for encoding");
        }

        return coerBytes;
    }


}

namespace IEEE1609Dot2Parsing {

}

#endif //V2VERIFIER_IEEE1609DOT2_HPP
