//
// Created by Geoff Twardokus on 3/12/24.
//

#include <iostream>

#include "../include/Vehicle.hpp"
#include "../../v2xmessage/include/IEEE1609Dot2Data.hpp"

std::vector<std::byte> Vehicle::getUnsecurePduCOERForPayload(const std::vector<std::byte> &payload) {

    try {
        IEEE1609Dot2Data t(payload);
        if(t.getContent().getContentChoice() != IEEE1609Dot2ContentChoice::unsecuredData) {
            throw std::runtime_error("Invalid call requests content type other than UnsecuredData");
        }
        return t.getCOER();
    }
    catch(std::runtime_error &e) {
        std::cout << e.what() << std::endl;
    }
}