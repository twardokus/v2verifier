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

    auto spdu = IEEE1609Dot2Generation::generateSPDU(IEEE1609Dot2::IEEE1609Dot2ContentChoice::signedData,
                                                     payload,
                                                     1,
                                                     1,
                                                     1,
                                                     IEEE1609Dot2::HashAlgorithm::sha256,
                                                     IEEE1609Dot2::SignerIdentifierChoice::self,
                                                     certDigest,
                                                     cert);



    return 0;
}