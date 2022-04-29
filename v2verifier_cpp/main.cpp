#include <iostream>
#include <thread>

#include "Vehicle.h"
#include "VehicleUtil.h"

int main(int argc, char *argv[]) {

    int num_msgs = 10000;

    ArgumentParser Parsed_args;
    if(argc == 7 || argc == 6 || argc == 2)
        Parsed_args = parse_args(argc,argv);
    else{
        perror("1(-h), 5 or 6 arguments are required for execution\n");
        exit(EXIT_FAILURE);
    }

    if(Parsed_args.perspective==TRANSMITTER) {
        Vehicle v1;
        v1.transmit(num_msgs, Parsed_args);
        v1.get_average_sign_times();
    }
    else if (Parsed_args.perspective==RECEIVER) {
        Vehicle v1;
        v1.receive(num_msgs, Parsed_args);
        v1.get_average_verify_times();
    }
}
