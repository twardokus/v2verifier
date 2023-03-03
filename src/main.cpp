// Copyright (c) 2022. Geoff Twardokus
// Reuse permitted under the MIT License as specified in the LICENSE file within this project.

#include <iostream>
#include <thread>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

#include "Vehicle.h"
#include "arguments.h"
#include "threading.cpp"

void print_usage() {
    std::cout << "Usage: v2verifer {dsrc | cv2x} {transmitter | receiver | both} [--test] [--gui]" << std::endl;
}

int main(int argc, char *argv[]) {

    if(argc < 3 || argc > 5) {
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

    if(std::string(argv[2]) == "transmitter") {
        args.sim_mode = TRANSMITTER;
    }
    else if(std::string(argv[2]) == "receiver")
        args.sim_mode = RECEIVER;
    else if(std::string(argv[2]) == "both") {
        //create threads here
        std::cout << "making threads";
        args.sim_mode = BOTH;
    }
    else {
        std::cout << R"(Error: second argument must be "transmitter" or "receiver")" << std::endl;
        print_usage();
        exit(EXIT_FAILURE);
    }

    if(argc == 4) {
        if (std::string(argv[3]) == "--test")
            args.test = true;
        else {
            std::cout << R"(Error: optional third argument can only be "--test")" << std::endl;
            print_usage();
            exit(EXIT_FAILURE);
        }
    }

    if(argc == 5) {
        if(std::string(argv[4]) == "--gui")
            args.gui = true;
        else{
            std::cout << R"(Error: optional fourth argument must be "--gui")" << std::endl;
            print_usage();
            exit(EXIT_FAILURE);
        }
    }

    boost::property_tree::ptree tree;
    boost::property_tree::json_parser::read_json("../config.json",tree);

    auto num_vehicles = tree.get<uint8_t>("scenario.numVehicles");
    auto num_msgs = tree.get<uint16_t>("scenario.numMessages");

    if(args.sim_mode == TRANSMITTER) {
        beginTransmitter(num_vehicles, num_msgs, args);
    }
    else if (args.sim_mode == RECEIVER) {
        beginReceiver(num_vehicles, num_msgs, args);
    }
    else if (args.sim_mode == BOTH) {
        beginReceiver(num_vehicles, num_msgs, args); //TODO make this a thread
        beginTransmitter(num_vehicles, num_msgs, args);
    }
}
