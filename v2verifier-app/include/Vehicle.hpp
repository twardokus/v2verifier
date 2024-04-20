/** @file   Vehicle.hpp
 *  @brief  Implementation of a class to represent a vehicle in the testbed environment.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs
*/

#ifndef V2VERIFIER_VEHICLE_HPP
#define V2VERIFIER_VEHICLE_HPP

#include <cstddef>

#include <vector>

/** @brief Representation of vehicle position/location data to be kept updated and retrieved as needed.*/
typedef struct VehicleLocationData {
    double latitude;
    double longitude;
    double elevation;
} VehicleLocationData;

/** @brief Representation of vehicle motion data to be kept updated and retrieved as needed. */
typedef struct VehicleMotionData {
    double speed;
    double heading;
} VehicleMotionData;


class Vehicle {

public:
    Vehicle() = default;
    Vehicle(Vehicle &v) = default;
    ~Vehicle() = default;

    [[nodiscard]] static std::vector<std::byte> getUnsecurePduCOERForPayload(const std::vector<std::byte> &payload);

private:

    VehicleLocationData locationData;
    VehicleMotionData motionData;

    /** @brief Update vehicle position from GPS data
     *
     *  @param latitude     the current GPS latitude
     *  @param longitude    the current GPS longitude
     *  @param elevation    the current GPS elevation
     *  @return 0 if successfully updated, -1 if not.
     */
    int updateGPSPosition(const double latitude, const double longitude, const double elevation);

    /** @brief Update the latitude for the vehicle's current location.
     *
     *  @param latitude the latitude of the vehicle, in meters
     *  @return 0 if successfully updated, -1 if not.
     */
    int updateLatitude(const double latitude);

    /** @brief Update the longitude for the vehicle's current location.
     *
     *  @param longitude the longitude of the vehicle, in meters
     *  @return 0 if updated successfully, -1 if not.
     */
    int updateLongitude(const double longitude);

    /** @brief Update the elevation for the vehicle's current location.
     *
     *  @param elevation the elevation of the vehicle, in meters
     *  @return 0 if updated successfully, -1 if not.
     */
    int updateElevation(const double elevation);

    /** @brief Update the speed for the vehicle's current motion data.
     *
     *  @param speed the vehicle's current speed, in meters per second
     *  @return 0 if updated succesfully, -1 if not.
     */
    int updateSpeed(const double speed);

    /** @brief Update the heading for the vehicle's current motion data.
     *
     *  @param heading the vehicle's current direction of travel, in degrees
     *  @return 0 if updated successfully, -1 if not.
     */
    int updateHeading(const double heading);

};


#endif //V2VERIFIER_VEHICLE_HPP
