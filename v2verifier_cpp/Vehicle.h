//
// Created by geoff on 10/14/21.
//

#ifndef CPP_VEHICLE_H
#define CPP_VEHICLE_H

#include <string>
#include <openssl/sha.h>
#include "VehicleUtil.h"
#include "ieee16092.h"
#include "bsm.h"
#include <openssl/crypto.h>
#include <openssl/ec.h>
#include <oqs/oqs.h>
#include "v2vcrypto.h"
#include <vector>

class Vehicle {

private:
    std::string hostname;
    EC_KEY *private_ec_key = nullptr, *cert_private_ec_key = nullptr;
    ecdsa_explicit_certificate vehicle_certificate_ecdsa;
    falcon_explicit_certificate vehicle_certificate_falcon;

    unsigned char certificate_signature[72];
    unsigned int certificate_buffer_length;

    uint8_t falcon_public_key[OQS_SIG_falcon_512_length_public_key];
    uint8_t falcon_private_key[OQS_SIG_falcon_512_length_secret_key];

    std::vector<int64_t> sign_times;
    std::vector<int64_t> verify_times;

    struct ecdsa_spdu {
        uint32_t llc_dsap_ssap = 43690;
        uint8_t  llc_control = 3;
        uint32_t llc_type = 35036;
        uint8_t wsmp_n_subtype_opt_version = 3;
        uint8_t wsmp_n_tpid = 0;
        uint8_t wsmp_t_header_length_and_psid = 32;
        uint8_t wsmp_t_length = 0;
        unsigned int signature_buffer_length;
        unsigned int certificate_signature_buffer_length;
        ieee1609dot2data_ecdsa_explicit data;
        unsigned char signature[72]; // 72 bytes is the size of the DER-encoded ECDSA signature
    };

    struct falcon_spdu {
        uint32_t llc_dsap_ssap = 43690;
        uint8_t  llc_control = 3;
        uint32_t llc_type = 35036;
        uint8_t wsmp_n_subtype_opt_version = 3;
        uint8_t wsmp_n_tpid = 0;
        uint8_t wsmp_t_header_length_and_psid = 32;
        uint8_t wsmp_t_length = 0;
        unsigned int signature_buffer_length;
        unsigned int certificate_signature_buffer_length;
        ieee1609dot2data_falcon_explicit data;
        unsigned char signature[OQS_SIG_falcon_512_length_signature];
    };

    void generate_ecdsa_spdu(Vehicle::ecdsa_spdu &spdu);
    void generate_falcon_spdu(Vehicle::falcon_spdu &spdu);

    static bsm generate_bsm();
    static void print_bsm(Vehicle::ecdsa_spdu &spdu);
    static void print_spdu(Vehicle::ecdsa_spdu & spdu);

    static void load_key_from_file_ecdsa(const char* filepath, EC_KEY *&key_to_store);

    void sign_message_ecdsa(Vehicle::ecdsa_spdu &spdu);
    void verify_message_ecdsa(Vehicle::ecdsa_spdu &spdu);
    void sign_message_falcon(Vehicle::falcon_spdu &spdu);
    void verify_message_falcon(Vehicle::falcon_spdu &spdu);

public:
    Vehicle() {
        hostname = "null_hostname";

        const char *cert_key_filepath = "cert_keys/0/p256.key";
        const char *key_filepath = "keys/0/p256.key";
        Vehicle::load_key_from_file_ecdsa(key_filepath, private_ec_key);
        Vehicle::load_key_from_file_ecdsa(cert_key_filepath, cert_private_ec_key);

        if(OQS_SIG_falcon_512_keypair(falcon_public_key, falcon_private_key) != OQS_SUCCESS) {
            perror("Error generating Falcon keypair");
            exit(EXIT_FAILURE);
        }

    };

    std::string get_hostname();
    void transmit(int num_msgs,ArgumentParser arg_pars);
    void receive(int num_msgs, ArgumentParser arg_pars);
    void get_average_sign_times();
    void get_average_verify_times();
};


#endif //CPP_VEHICLE_H
