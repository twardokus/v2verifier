//
// Created by Bharath Suresh on 10/20/21.
//

#ifndef POST_QUANTUM_V2VERIFIER_VEHICLEUTIL_H
#define POST_QUANTUM_V2VERIFIER_VEHICLEUTIL_H

#include <iostream>
#include <string>

#define RECEIVER "receiver"
#define TRANSMITTER "transmitter"
#define ECDSA "ecdsa"
#define IMPLICIT "implicit"
#define EXPLICIT "explicit"
#define DSRC "dsrc"
#define CV2X "cv2x"
#define TESTREQ "--test"
#define HELP "-h"

struct ArgumentParser{
    std::string perspective;
    std::string sig_alg;
    std::string cert_alg;
    std::string cert_type;
    std::string technology;
    bool istest;
};

struct temp_cert_struct{
    unsigned int temp_buflen;
    unsigned char temp_final_sign[72];
};


ArgumentParser parse_args(int argc, char *argv[]);
void help_function();

#endif //POST_QUANTUM_V2VERIFIER_VEHICLEUTIL_H
