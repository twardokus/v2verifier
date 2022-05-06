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
        Vehicle v1("/home/geoff/CLionProjects/v2verifier/v2verifier_cpp/cert_keys/0/p256.key",
                   "/home/geoff/CLionProjects/v2verifier/v2verifier_cpp/keys/0/p256.key");
        v1.transmit(num_msgs, args.test);
    }
    else if (args.sim_mode == RECEIVER) {
        Vehicle v1("/home/geoff/CLionProjects/v2verifier/v2verifier_cpp/cert_keys/0/p256.key",
                   "/home/geoff/CLionProjects/v2verifier/v2verifier_cpp/keys/0/p256.key");;
        v1.receive(num_msgs, args.test);
    }

}
