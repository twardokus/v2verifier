//
// Created by geoff on 11/13/21.
//

#ifndef CPP_V2VCRYPTO_H
#define CPP_V2VCRYPTO_H

void sha256sum(void* data, unsigned long length, unsigned char* md);
void ecdsa_sign(unsigned char *hash, EC_KEY *signing_key, unsigned int* signature_buffer_length, unsigned char *signature);
bool ecdsa_verify(unsigned char *hash, unsigned char *signature, const unsigned int* signature_buffer_length, EC_KEY *verification_key);

#endif //CPP_V2VCRYPTO_H
