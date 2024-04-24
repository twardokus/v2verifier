/** @file   main.cpp
 *  @brief  Main execution file for the testbed.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#include <cstddef>
#include <iostream>
#include <vector>

#include "../../logger/Log.h"
#include "../include/Vehicle.hpp"
#include "../../v2xmessage/include/IEEE1609Dot2.hpp"
#include "../include/V2VSecurity.hpp"

int main() {

    Logger::startLog("vehicleLog.txt");

//    std::vector<std::byte> testBytes;
//    testBytes.push_back(std::byte{0x03});
//    testBytes.push_back(std::byte{0x80});
//    testBytes.push_back(std::byte{0xF3});
//    testBytes.push_back(std::byte{0xA5});
//
//    auto test = Vehicle::getUnsecurePduCOERForPayload(testBytes);

    Vehicle v(43, 75, 100, 100, 40);

    std::vector<std::byte> payload = {std::byte{0x00}, std::byte{0x01}};
    std::vector<std::byte> certDigest = {std::byte{0x00}};
    IEEE1609Dot2::Certificate cert;

    uint64_t currentTime = Utility::getCurrentTimeAsUint64();

    auto spdu = IEEE1609Dot2Generation::generateSPDU(IEEE1609Dot2::IEEE1609Dot2ContentChoice::signedData,
                                                     payload,
                                                     0x20,
                                                     currentTime,
                                                     currentTime + (1000*60*60) /*one hour in milliseconds */,
                                                     IEEE1609Dot2::HashAlgorithm::sha256,
                                                     IEEE1609Dot2::SignerIdentifierChoice::self,
                                                     certDigest,
                                                     cert);

    auto spduBytes = IEEE1609Dot2Generation::encodeSPDU(spdu);

    std::string pemFilename = "../../test_key.pem";
    V2VSecurity secmgr(pemFilename);

    std::string message = "Test";
    bool result;
    unsigned char* signature = nullptr;
    size_t signature_length;

    secmgr.signMessage(message.data(), signature, signature_length);

    return 0;
}