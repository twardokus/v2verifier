//
// Created by geoff on 11/13/21.
//

#include <iostream>
#include <openssl/ec.h>
#include <openssl/sha.h>
#include <oqs.h>


void ecdsa_sign(unsigned char *hash, EC_KEY *signing_key, unsigned int* signature_buffer_length, unsigned char *signature) {

    if(ECDSA_sign(0, hash, 32, signature, signature_buffer_length, signing_key) != 1) {
        perror("Error in call to ECDSA_sign");
        exit(EXIT_FAILURE);
    }

}

bool ecdsa_verify(unsigned char *hash, unsigned char *signature, const unsigned int* signature_buffer_length, EC_KEY *verification_key) {

    return ECDSA_verify(0, hash,32, signature, (int)*signature_buffer_length, verification_key);

}

void falcon_sign(uint8_t *signature, size_t &signature_len, uint8_t *message, size_t message_len, uint8_t *private_key) {

    if (OQS_SIG_falcon_512_sign(signature, &signature_len, message, message_len, private_key) != OQS_SUCCESS) {
        perror("Error in call to falcon_sign");
        exit(EXIT_FAILURE);
    }
}

bool falcon_verify(uint8_t *message, size_t message_len, uint8_t *signature, size_t signature_len, uint8_t *public_key) {

    OQS_STATUS result = OQS_SIG_falcon_512_verify(message, message_len, signature, signature_len, public_key);
    return result == OQS_SUCCESS;

}

void sha256sum(void* data, unsigned long length, unsigned char* md) {

    SHA256_CTX context;
    if(!SHA256_Init(&context)) {
        perror("Error initializing SHA256 context");
        exit(EXIT_FAILURE);
    }

    if(!SHA256_Update(&context, (unsigned char*) data, length)) {
        perror("Error hashing provided input.");
        exit(EXIT_FAILURE);
    }

    if(!SHA256_Final(md, &context)) {
        perror("Error storing hash digest");
        exit(EXIT_FAILURE);
    }

}