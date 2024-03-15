/** @file   V2XMessage.hpp
 *  @brief  Abstract parent class for V2X message classes
 *
 *  All classes for SPDU elements defined in IEEE 1609.2, as well as specific message types, inherit from this abstract
 *  class.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    no known bugs
 */

#ifndef V2VERIFIER_V2XMESSAGE_HPP
#define V2VERIFIER_V2XMESSAGE_HPP

#include <chrono>
#include <cstddef>
#include <stdexcept>
#include <vector>

#include "IEEE1609Dot2DataTypes.hpp"
#include "Utility.hpp"

class V2XMessage {

public:
    /** @brief  Default constructor for V2XMessage.
     *
     *  @param  None.
     */
    V2XMessage() = default;

private:

    /** @brief  Get the COER bytestring for the object.
     *
     *  @return The COER encoding of the object as a byte string.
     */
    virtual std::vector<std::byte> getCOER() = 0;

};

#endif //V2VERIFIER_V2XMESSAGE_HPP
