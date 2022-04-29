#include <iostream>
#include "VehicleUtil.h"

ArgumentParser parse_args  (int argc, char *argv[]){
    ArgumentParser Args;
    if((std::string)argv[1] == RECEIVER || (std::string)argv[1] == TRANSMITTER)
        Args.perspective = argv[1];
    else if((std::string)argv[1] == HELP){
        help_function();
        exit(EXIT_SUCCESS);
    }
    else{
        perror("First argument should be either 'receiver' or 'transmitter' or '--help'\n");
        exit(EXIT_FAILURE);
    }

    if((std::string)argv[2] == ECDSA)
        Args.sig_alg = argv[2];
    else{
        perror("Second argument should be 'ecdsa'\n");
        exit(EXIT_FAILURE);
    }

    if((std::string)argv[3] == ECDSA)
        Args.cert_alg = argv[3];
    else{
        perror("Third argument should be 'ecdsa'\n");
        exit(EXIT_FAILURE);
    }

    if((std::string)argv[4] == IMPLICIT ||(std::string) argv[4] == EXPLICIT)
        Args.cert_type = argv[4];
    else{
        perror("Fourth argument should be either 'implicit' or 'explicit'\n");
        exit(EXIT_FAILURE);
    }

    if((std::string)argv[5] == DSRC || (std::string)argv[5] == CV2X)
        Args.technology = argv[5];
    else{
        perror("Fifth argument should be either 'dsrc' or 'cv2x'\n");
        exit(EXIT_FAILURE);
    }

    if(argc == 7){
        if ((std::string)argv[6] == TESTREQ)
            Args.istest = true;
        else{
            perror("Sixth argument (if provided) should be '--test' \n");
            exit(EXIT_FAILURE);
        }
    }
    else if(argc == 6)
        Args.istest = false;
    else{
        perror("Number of arguments is wrong.\n");
        exit(EXIT_FAILURE);
    }

    return Args;
}

void help_function(){
    std::cout<<"A testbed for V2V security"<<std::endl;
    std::cout<<"\n\nPositional Arguments:\n{receiver,transmitter} - Choice of role\n{ecdsa} - Signature algorithm to use\n"
               "{ecdsa} - Certificate algorithm to use\n{implicit,explicit} - Certificate type to use\n{dsrc,cv2x} - Choice of technology"<<std::endl;
    std::cout<<"\n\nOptional Arguments:\n '-h' - Shows this help message and exits\n'--test' - Runs in test mode without SDRs or GNURadio\n\n"<<std::endl;
    std::cout<<"./cpp [-h] {receiver,transmitter} {ecdsa} {ecdsa} {implicit,explicit} {dsrc,cv2x} [--test]"<<std::endl;
}
