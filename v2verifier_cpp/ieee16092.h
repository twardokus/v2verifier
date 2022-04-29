//
// Created by geoff on 10/19/21.
//

#ifndef CPP_IEEE16092_H
#define CPP_IEEE16092_H

#include "bsm.h"
#include "certificates.h"

struct header_info {
    uint8_t psid = 32;
    std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds> timestamp;
};

struct to_be_signed_data {
    uint8_t protocol_version = 3;
    bsm message;
    header_info headerInfo;
};

struct signed_data_ecdsa_implicit_certificate {
    uint8_t hashID = 0; // SHA-256
    to_be_signed_data tbsData;
    ecdsa_implicit_certificate cert = {};
};

struct signed_data_ecdsa_explicit_certificate {
    uint8_t hashID = 0; // SHA-256
    to_be_signed_data tbsData;
    ecdsa_explicit_certificate cert = {};
};

struct signed_data {
    uint8_t hashID = 0;
    to_be_signed_data tbsData;
};

struct ieee1609dot2data_ecdsa_implicit {
    uint8_t protocol_version = 3;
    signed_data_ecdsa_implicit_certificate signedData;
};

struct ieee1609dot2data_ecdsa_explicit {
    uint8_t protocol_version = 3;
    signed_data_ecdsa_explicit_certificate signedData;
    unsigned char certificate_signature[72];
};

struct ieee1609dot2data {
    uint8_t protocol_version = 3;
    signed_data signedData;
};

#endif //CPP_IEEE16092_H
