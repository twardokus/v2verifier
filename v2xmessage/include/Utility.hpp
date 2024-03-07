//
// Created by Geoff Twardokus on 3/7/24.
//

#ifndef V2VERIFIER_UTILITY_HPP
#define V2VERIFIER_UTILITY_HPP

#include <vector>

namespace Utility {

    static std::vector<std::byte> vectorFromUint64(const uint64_t &val) {

        auto returnVec = std::vector<std::byte>(sizeof(uint64_t));
        std::fill(returnVec.begin(), returnVec.end(), std::byte{0});

        std::memcpy(returnVec.data(), &val, sizeof(val));

        return returnVec;
    }

    static std::vector<std::byte> vectorFromUint32(const uint32_t &val) {

        auto returnVec = std::vector<std::byte>(sizeof(uint32_t));

        std::memcpy(returnVec.data(), &val, sizeof(val));

        return returnVec;
    }

}

#endif //V2VERIFIER_UTILITY_HPP
