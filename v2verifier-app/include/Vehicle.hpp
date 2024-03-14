//
// Created by Geoff Twardokus on 3/12/24.
//

#ifndef V2VERIFIER_VEHICLE_HPP
#define V2VERIFIER_VEHICLE_HPP

#include <cstddef>
#include <vector>

class Vehicle {

public:
    Vehicle() = default;
    Vehicle(Vehicle &v) = default;
    ~Vehicle() = default;

    [[nodiscard]] static std::vector<std::byte> getUnsecurePduCOERForPayload(const std::vector<std::byte> &payload);

private:

};


#endif //V2VERIFIER_VEHICLE_HPP
