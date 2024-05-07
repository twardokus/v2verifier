/** @file   Vehicle.hpp
 *  @brief  Class to represent a vehicle in the testbed environment.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs
*/

#ifndef V2VERIFIER_VEHICLE_HPP
#define V2VERIFIER_VEHICLE_HPP

#include <cstddef>
#include <vector>

#include "../include/V2VSecurity.hpp"

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
    /** @brief default constructor */
    Vehicle() = default;
    /** Copy constructor */
    Vehicle(Vehicle &v) = default;
    /** Destructor */
    ~Vehicle();

    /** @brief Create new vehicle with provided location and motion information
     *
     *  @param latitude the vehicle latitude
     *  @param longitude the vehicle longitude
     *  @param elevation the vehicle elevation
     *  @param speed the vehicle speed
     *  @param heading the vehicle heading
     */
    Vehicle(double latitude, double longitude, double elevation, double speed, double heading, std::string &keyFilename);

    /** @brief Create new vehicle with location data but no motion information (for stopped/parked vehicles)
     *
     *  @param latitude the vehicle latitude
     *  @param longitude the vehicle longitude
     *  @param elevation the vehicle elevation
     */
    Vehicle(double latitude, double longitude, double elevation, std::string &keyFilename);

private:

    VehicleLocationData locationData;
    VehicleMotionData motionData;

    V2VSecurity* securityManager = nullptr;

    std::string keyFilepath = "../../test.pem"; // TODO: should be passed or loaded from config file

    void initialize(std::string &keyFilename,
                               double latitude,
                               double longitude,
                               double elevation,
                               double speed = 0,
                               double heading = 0);

    /** @brief Initialized the position and motion data for the vehicle.
     *
     *  @param latitude the vehicle latitude
     *  @param longitude the vehicle longitude
     *  @param elevation the vehicle elevation
     *  @param speed the vehicle speed
     *  @param heading the vehicle heading
     *  @return 0 if all values initialized successfully, otherwise -1
     */
    int initializePositionAndMotion(double latitude,
                                    double longitude,
                                    double elevation,
                                    double speed,
                                    double heading);

    /** @brief Update vehicle position from GPS data
     *
     *  @param latitude     the current GPS latitude
     *  @param longitude    the current GPS longitude
     *  @param elevation    the current GPS elevation
     *  @return 0 if successfully updated, -1 if not.
     */
    int updateGPSPosition(double latitude, double longitude, double elevation);

    /** @brief Update the latitude for the vehicle's current location.
     *
     *  @param latitude the latitude of the vehicle, in meters
     *  @return 0 if successfully updated, -1 if not.
     */
    int updateLatitude(double latitude);

    /** @brief Update the longitude for the vehicle's current location.
     *
     *  @param longitude the longitude of the vehicle, in meters
     *  @return 0 if updated successfully, -1 if not.
     */
    int updateLongitude(double longitude);

    /** @brief Update the elevation for the vehicle's current location.
     *
     *  @param elevation the elevation of the vehicle, in meters
     *  @return 0 if updated successfully, -1 if not.
     */
    int updateElevation(double elevation);

    /** @brief Update the speed for the vehicle's current motion data.
     *
     *  @param speed the vehicle's current speed, in meters per second
     *  @return 0 if updated succesfully, -1 if not.
     */
    int updateSpeed(double speed);

    /** @brief Update the heading for the vehicle's current motion data.
     *
     *  @param heading the vehicle's current direction of travel, in degrees
     *  @return 0 if updated successfully, -1 if not.
     */
    int updateHeading(double heading);

    /** @brief Format an error string for an invalid double value provided as a location or motion field.
     *
     *  @param field name of the field that was to be set
     *  @param invalidValue the invalid value
     *  @return formatted string error message
     */
    static std::string formatErrorForInvalidValue(std::string &field, double invalidValue);

    /** @brief Format an error string for an invalid integer value provided as a location or motion field.
     *
     *  @param field name of the field that was to be set
     *  @param invalidValue the invalid value
     *  @return formatted string error message
     */
    static std::string formatErrorForInvalidValue(std::string &field, int invalidValue);



};

#endif //V2VERIFIER_VEHICLE_HPP
