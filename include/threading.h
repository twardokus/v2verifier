//
// Created by greet on 3/2/2023.
//
#ifndef V2VERIFIER_THREADING_H
#define V2VERIFIER_THREADING_H

#include "arguments.h"

void beginReceiver(int num_vehicles, int num_msgs, program_arguments args);
void beginTransmitter(int num_vehicles, int num_msgs, program_arguments args);

#endif //V2VERIFIER_THREADING_H
