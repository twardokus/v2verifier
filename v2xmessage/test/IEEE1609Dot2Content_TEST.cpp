//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/IEEE1609Dot2Content.hpp"
#include <vector>

#include <iostream>

int main() {


    std::vector<std::byte> testCOER;

    testCOER.push_back(std::byte{0x81});

    // HashAlgorithm

    testCOER.push_back(std::byte{(uint8_t) IEEE1609Dot2DataTypes::HashAlgorithm::sha256});

    // ToBeSignedData

    std::vector<std::byte> toBeSignedDataBytes;

    // Create 50 bytes of random data to be the SignedDataPayload->data elements
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(0, 255);

    toBeSignedDataBytes.reserve(50);
    toBeSignedDataBytes.assign(50,std::byte{0});

    for(auto & i : toBeSignedDataBytes) {
        i = std::byte{(uint8_t) distr(gen)};
    }

    // Append COER for a valid headerInfo structure
    uint32_t psid = 0x32;
    auto psidBytes = Utility::vectorFromUint32(psid);

    auto now = std::chrono::time_point_cast<std::chrono::milliseconds>(std::chrono::system_clock::now());
    uint64_t generationTime = now.time_since_epoch().count();
    auto generationBytes = Utility::vectorFromUint64(generationTime);
    uint64_t expiryTime = now.time_since_epoch().count() + 100000;
    auto expiryBytes = Utility::vectorFromUint64(expiryTime);

    std::vector<std::byte> headerInfoBytes;
    headerInfoBytes.insert(headerInfoBytes.begin(), psidBytes.begin(), psidBytes.end());
    headerInfoBytes.insert(headerInfoBytes.end(), generationBytes.begin(), generationBytes.end());
    headerInfoBytes.insert(headerInfoBytes.end(), expiryBytes.begin(), expiryBytes.end());

    toBeSignedDataBytes.insert(toBeSignedDataBytes.end(), headerInfoBytes.begin(), headerInfoBytes.end());

    testCOER.insert(testCOER.end(), toBeSignedDataBytes.begin(), toBeSignedDataBytes.end());

    // SignerIdentifier

    testCOER.push_back(std::byte{0x80} | std::byte{(uint8_t) SignerIdentifierChoice::self});

    // Signature
    auto ecdsaP256Bytes = Utility::randomBytesOfLength(Signature::SIGNATURE_SIZE_BYTES);
    ecdsaP256Bytes[0] = std::byte{0x80};
    ecdsaP256Bytes[1] = std::byte{0x80};

    testCOER.insert(testCOER.end(), ecdsaP256Bytes.begin(), ecdsaP256Bytes.end());

    IEEE1609Dot2Content t(testCOER);

    return t.getContentChoice() != IEEE1609Dot2ContentChoice::signedData;
}