//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_IEEE1609DOT2DATA_H
#define V2VERIFIER_IEEE1609DOT2DATA_H


#include <cstdint>

#include "Ieee1609Dot2Content.h"

class Ieee1609Dot2Data {

public:

private:
    uint8_t protocolVersion = 3; /** Always 3 in IEEE1609.2-2022 */
    Ieee1609Dot2Content content;
};


#endif //V2VERIFIER_IEEE1609DOT2DATA_H
