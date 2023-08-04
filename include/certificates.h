// Copyright (c) 2022. Geoff Twardokus
// Reuse permitted under the MIT License as specified in the LICENSE file within this project.

#ifndef CPP_CERTIFICATES_H
#define CPP_CERTIFICATES_H

#include <array>
#include <openssl/ec.h>

struct common_cert_fields {
    uint8_t version = 3;
    uint8_t issuer = 128;
    uint32_t craca_id = 0;
    uint16_t crlseries = 0;
    uint8_t validity_period_choice = 132;
    uint16_t validity_period_duration = 24;
    char hostname[9] = "hostname"; // If you want to update this to use std::string in future, remember the struct needs to be properly serialized before sending over the wire.
    std::chrono::time_point<std::chrono::system_clock, std::chrono::seconds> validity_period_start;
};

struct ecdsa_implicit_certificate {
    common_cert_fields commonCertFields;
    uint8_t certificate_type = 1;
    uint8_t verify_key_indicator = 129;
    uint8_t reconstruction_value_choice = 128;
    std::array<uint8_t, 32> reconstruction_value = {}; // this is 32 null bytes for size
};

struct ecdsa_explicit_certificate {
    common_cert_fields commonCertFields;
    uint8_t certificate_type = 0;
    uint8_t verify_key_indicator = 128;
    uint8_t verify_key_type = 128;
    uint8_t verification_key_type = 128;
    uint8_t verification_key_choice = 132;
};

#endif //CPP_CERTIFICATES_H
