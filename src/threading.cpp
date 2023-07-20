//
// Created by Brandon Greet on 3/2/2023.
//

#include <iostream>
#include <thread>

#include "Vehicle.h"
#include "arguments.h"

void beginReceiver(int num_vehicles, int num_msgs, program_arguments args) {
    Vehicle v1(0);
    v1.receive(num_msgs * num_vehicles, args.test, args.tkgui, args.webgui);
}

void beginTransmitter(int num_vehicles, int num_msgs, program_arguments args) {
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