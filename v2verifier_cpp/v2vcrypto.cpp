#include <openssl/ec.h>
#include <openssl/sha.h>


void ecdsa_sign(unsigned char *hash, EC_KEY *signing_key, unsigned int* signature_buffer_length, unsigned char *signature) {

    if(ECDSA_sign(0, hash, 32, signature, signature_buffer_length, signing_key) != 1) {
        perror("Error in call to ECDSA_sign");
        exit(EXIT_FAILURE);
    }

}

int ecdsa_verify(unsigned char *hash, unsigned char *signature, const unsigned int* signature_buffer_length, EC_KEY *verification_key) {
    int result = ECDSA_verify(0, hash,32, signature, (int)*signature_buffer_length, verification_key);
    if(result == -1) {
        perror("Fatal error: ECDSA_verify returned -1");
        exit(EXIT_FAILURE);
    }
    else
        return result;

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