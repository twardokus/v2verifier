//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_V2XMESSAGE_HPP
#define V2VERIFIER_V2XMESSAGE_HPP

#include <vector>

#include "IEEE1609Dot2DataTypes.hpp"

class V2XMessage {

public:
    V2XMessage() = default;

private:
    virtual std::vector<std::byte> getCOER() = 0;

};

#endif //V2VERIFIER_V2XMESSAGE_HPP
