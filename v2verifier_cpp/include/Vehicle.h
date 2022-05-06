//
// Created by geoff on 10/14/21.
//

#ifndef CPP_VEHICLE_H
#define CPP_VEHICLE_H

#include <string>
#include <openssl/sha.h>
#include "ieee16092.h"
#include "bsm.h"
#include <openssl/crypto.h>
#include <openssl/ec.h>
#include "v2vcrypto.h"
#include <vector>

class Vehicle {

private:
    std::string hostname;
    EC_KEY *private_ec_key = nullptr, *cert_private_ec_key = nullptr;
    ecdsa_explicit_certificate vehicle_certificate_ecdsa;

    unsigned char certificate_signature[72];
    unsigned int certificate_buffer_length;

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

    void generate_ecdsa_spdu(Vehicle::ecdsa_spdu &spdu);

    static bsm generate_bsm();
    static void print_bsm(Vehicle::ecdsa_spdu &spdu);
    static void print_spdu(Vehicle::ecdsa_spdu &spdu, bool valid);

    static void load_key_from_file_ecdsa(const char* filepath, EC_KEY *&key_to_store);

    void sign_message_ecdsa(Vehicle::ecdsa_spdu &spdu);
    bool verify_message_ecdsa(Vehicle::ecdsa_spdu &spdu, std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds> received_time);

public:
    Vehicle(const char *cert_key_filepath, const char *key_filepath) {
        hostname = "null_hostname";

        Vehicle::load_key_from_file_ecdsa(key_filepath, private_ec_key);
        Vehicle::load_key_from_file_ecdsa(cert_key_filepath, cert_private_ec_key);

    };

    std::string get_hostname();
    void transmit(int num_msgs, bool test);
    void receive(int num_msgs, bool test);
};


#endif //CPP_VEHICLE_H
