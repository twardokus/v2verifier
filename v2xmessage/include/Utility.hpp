/** @file   Utility.hpp
 *  @brief  Defines the Utility namespace to collect these functions in one spot.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs.
 */

#ifndef V2VERIFIER_UTILITY_HPP
#define V2VERIFIER_UTILITY_HPP

#include <cstring>
#include <random>
#include <vector>

//! Utility functions to be reused throughout the project.
namespace Utility {

    /** @brief Get the COER encoding for a given uint64_t.
     *
     *  @param val The integer for which a COER encoding is requested.
     *  @return The COER encoding (8 octets) of \p val
     */
    static std::vector<std::byte> vectorFromUint64(const uint64_t &val) {

        auto returnVec = std::vector<std::byte>(sizeof(uint64_t));
        std::fill(returnVec.begin(), returnVec.end(), std::byte{0});

        std::memcpy(returnVec.data(), &val, sizeof(val));

        return returnVec;
    }

    /** @brief Get the COER encoding for a given uint32_t.
     *
     *  @param val The integer for which a COER encoding is requested.
     *  @return The COER encoding (4 octets) of \p val.
     */
    static std::vector<std::byte> vectorFromUint32(const uint32_t &val) {

        auto returnVec = std::vector<std::byte>(sizeof(uint32_t));

        std::memcpy(returnVec.data(), &val, sizeof(val));

        return returnVec;
    }

    /** @brief Get \p n random bytes.
     *
     *  @param n The length of the random byte string to return.
     * @return A random byte string of length \p n.
     */
    static std::vector<std::byte> randomBytesOfLength(const uint32_t &n) {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distr(0, 255);

        std::vector<std::byte> randomBytes;
        randomBytes.reserve(n);
        randomBytes.assign(n,std::byte{0});


        for(auto & i : randomBytes) {
            i = std::byte{(uint8_t) distr(gen)};
        }

        return randomBytes;
    }

}

#endif //V2VERIFIER_UTILITY_HPP
