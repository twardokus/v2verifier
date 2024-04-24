//
// Created by Geoff Twardokus on 4/23/24.
//

#ifndef V2VERIFIER_V2VSECURITY_HPP
#define V2VERIFIER_V2VSECURITY_HPP

#define ECDSA_P256_DER_LENGTH_BYTES 72

#include <openssl/evp.h>
#include <string>
#include <fstream>

class V2VSecurity {

public:

    V2VSecurity() = delete;
    V2VSecurity(std::string &pemFilename);
    ~V2VSecurity();

    bool signMessage(char* msg, unsigned char* &sig, size_t &sig_len);
    bool verifyMessage(char *msg, evp_pkey_st *publicKey, const unsigned char* signature, size_t sig_len);

    EVP_PKEY *pkey = nullptr;

private:

    std::ifstream pemfile;

    EVP_MD_CTX *mdctx_sign = nullptr;
    EVP_MD_CTX *mdctx_verify = nullptr;

    void loadPEMFile(std::string &filename);

    void setupSigningState();

};


#endif //V2VERIFIER_V2VSECURITY_HPP
