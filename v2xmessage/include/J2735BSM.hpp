//
// Created by Geoff Twardokus on 4/22/24.
//

#ifndef V2VERIFIER_J2735BSM_HPP
#define V2VERIFIER_J2735BSM_HPP

#include "V2XMessage.hpp"
#include <vector>

class J2735BSM : V2XMessage {

public:

    J2735BSM() = default;


    std::vector<std::byte> getCOER();

};


#endif //V2VERIFIER_J2735BSM_HPP
