//
// Created by Geoff Twardokus on 3/6/24.
//

#include "../include/HeaderInfo.hpp"
#include "../include/Utility.hpp"

#include <chrono>
#include <iostream>


int main() {

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

    HeaderInfo headerInfo(coerBytes);

    if(headerInfo.getPsid() != psid)
        return 1;
    if(headerInfo.getGenerationTime() != generationTime)
        return 2;
    if(headerInfo.getExpiryTime() != expiryTime)
        return 3;

    auto headerInfoBytes = headerInfo.getCOER();

    if(headerInfoBytes != coerBytes)
        return 4;

    return 0;
}