#include <iostream>
#include <thread>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

#include "Vehicle.h"
#include "arguments.h"

//#include "VehicleUtil.h"

void print_usage() {
    std::cout << "Usage: v2verifer {dsrc | cv2x} {transmitter | receiver} [--test] " << std::endl;
}

int main(int argc, char *argv[]) {

    if(argc < 3 || argc > 4) {
        print_usage();
        exit(EXIT_FAILURE);
    }

    program_arguments args;

    if(std::string(argv[1]) == "dsrc")
        args.tech_choice = DSRC;
    else if(std::string(argv[1]) == "cv2x")
        args.tech_choice = CV2X;
    else {
        std::cout << "Error: first argument must be DSRC or C_V2X" << std::endl;
        print_usage();
        exit(EXIT_FAILURE);
    }

    if(std::string(argv[2]) == "transmitter")
        args.sim_mode = TRANSMITTER;
    else if(std::string(argv[2]) == "receiver")
        args.sim_mode = RECEIVER;
    else {
        std::cout << R"(Error: second argument must be "transmitter" or "receiver")" << std::endl;
        print_usage();
        exit(EXIT_FAILURE);
    }

    if(argc == 4) {
        if(std::string(argv[3]) == "--test")
            args.test = true;
        else {
            std::cout << R"(Error: optional third argument can only be "--test")" << std::endl;
            print_usage();
            exit(EXIT_FAILURE);
        }
    }

    boost::property_tree::ptree tree;
    boost::property_tree::json_parser::read_json("../config.json",tree);

    auto num_vehicles = tree.get<uint8_t>("scenario.numVehicles");
    auto num_msgs = tree.get<uint16_t>("scenario.numMessages");

    if(args.sim_mode == TRANSMITTER) {
        std::vector<Vehicle> vehicles;
        std::vector<std::thread> workers;

        // initialize vehicles - has to be in a separate loop to prevent vector issues
        for(int i = 0; i < num_vehicles; i++) {
            vehicles.emplace_back(Vehicle(i));
        }

        // start a thread for each vehicle
        for(int i = 0; i < num_vehicles; i++) {
            workers.emplace_back(std::thread(vehicles.at(i).transmit_static, &vehicles.at(i), num_msgs, args.test));
        }

        // wait for each vehicle thread to finish
        for(int i = 0; i < num_vehicles; i++) {
            workers.at(i).join();
        }

    }
    else if (args.sim_mode == RECEIVER) {
        Vehicle v1(0);
        v1.receive(num_msgs, args.test);
    }



}
