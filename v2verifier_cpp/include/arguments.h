//
// Created by geoff on 5/6/22.
//

#ifndef V2VERIFIER_ARGUMENTS_H
#define V2VERIFIER_ARGUMENTS_H

enum mode {
    TRANSMITTER,
    RECEIVER
};

enum technology {
    DSRC,
    CV2X
};

struct program_arguments {
    mode sim_mode = RECEIVER;
    technology tech_choice = DSRC;
    bool test = false;
};

#endif //V2VERIFIER_ARGUMENTS_H
