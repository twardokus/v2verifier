//
// Created by Geoff Twardokus on 3/7/24.
//

#include "../include/ToBeSignedData.hpp"

#include <random>

int main() {

    std::vector<std::byte> testCOER;

    // Create 50 bytes of random data to be the SignedDataPayload->data elements
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(0, 255);

    testCOER.reserve(50);
    testCOER.assign(50,std::byte{0});

    for(auto & i : testCOER) {
        i = std::byte{(uint8_t) distr(gen)};
    }

    auto randomBytes = testCOER;

    // Append COER for a valid headerInfo structure
    uint32_t psid = 0x32;
    auto psidBytes = Utility::vectorFromUint32(psid);

    auto now = std::chrono::time_point_cast<std::chrono::milliseconds>(std::chrono::system_clock::now());
    uint64_t generationTime = now.time_since_epoch().count();
    auto generationBytes = Utility::vectorFromUint64(generationTime);
    uint64_t expiryTime = now.time_since_epoch().count() + 100000;
    auto expiryBytes = Utility::vectorFromUint64(expiryTime);

    std::vector<std::byte> coerBytes;
    coerBytes.insert(coerBytes.begin(), psidBytes.begin(), psidBytes.end());
    coerBytes.insert(coerBytes.end(), generationBytes.begin(), generationBytes.end());
    coerBytes.insert(coerBytes.end(), expiryBytes.begin(), expiryBytes.end());

    testCOER.insert(testCOER.end(), coerBytes.begin(), coerBytes.end());

    ToBeSignedData t(testCOER);

    if(t.getPayload().getData() != randomBytes)
        return 1;

    if(t.getHeaderInfo().getPsid() != psid)
        return 2;
    if(t.getHeaderInfo().getGenerationTime() != generationTime)
        return 3;
    if(t.getHeaderInfo().getExpiryTime() != expiryTime)
        return 4;

    if(t.getCOER() != testCOER)
        return 5;

    return 0;
}
