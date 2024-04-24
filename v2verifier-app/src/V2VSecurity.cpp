//
// Created by Geoff Twardokus on 4/23/24.
//

#include <openssl/pem.h>
#include <iostream>
#include <openssl/bio.h>

#include "../include/V2VSecurity.hpp"


V2VSecurity::V2VSecurity(std::string &pemFilename) {
    loadPEMFile(pemFilename);
    this->setupSigningState();
}

V2VSecurity::~V2VSecurity() {
    EVP_PKEY_free(this->pkey);

    if(this->pemfile.is_open())
        this->pemfile.close();

    EVP_MD_CTX_destroy(this->mdctx_sign);
}

void V2VSecurity::loadPEMFile(std::string &filename) {

    try {
        this->pemfile.open(filename);
        if (!pemfile.is_open()) {
            throw std::runtime_error("Fatal error! Failed to load key: invalid PEM filename specified.");
        }
    }
    catch (std::runtime_error &e) {
        std::cerr << e.what() << std::endl;
        exit(-1);
    }

    std::string keyContents((std::istreambuf_iterator<char>(pemfile)), std::istreambuf_iterator<char>());

    BIO* bo = BIO_new(BIO_s_mem());
    BIO_write(bo, keyContents.c_str(), strlen(keyContents.c_str()));
    EVP_PKEY* _pkey = nullptr;
    try {
        PEM_read_bio_PrivateKey(bo, &_pkey, nullptr, nullptr);
        if(_pkey == nullptr) {
            throw std::runtime_error("Fatal error! Could not read key from PEM file.");
        }
        this->pkey = _pkey;
    }
    catch(std::runtime_error &e) {
        std::cerr << e.what() << std::endl;
        exit(-1);
    }
    BIO_free(bo);

}

void V2VSecurity::setupSigningState() {

    this->mdctx_sign = EVP_MD_CTX_create();
    if(!this->mdctx_sign) {
        throw std::runtime_error("Fatal error - could not create signer context.");
    }

    if(EVP_DigestSignInit(this->mdctx_sign, nullptr, EVP_sha256(), nullptr, this->pkey) != 1) {
        throw std::runtime_error("Fatal error - could not initialize EVP digest");
    }

    this->mdctx_verify = EVP_MD_CTX_create();
    if(!this->mdctx_verify) {
        throw std::runtime_error("Fatal error - could not create verifier context");

    }

}

bool V2VSecurity::signMessage(char* msg, unsigned char* &sig, size_t &sig_len) {

    unsigned char* localSig = nullptr;

    if(EVP_DigestSignUpdate(this->mdctx_sign, msg, strlen(msg)) != 1) {
        return false;
    }

    if(EVP_DigestSignFinal(this->mdctx_sign, nullptr, &sig_len) != 1) {
        return false;
    }

    if(!(localSig = (unsigned char*) OPENSSL_malloc(sizeof(unsigned char) * (sig_len)))) {
        OPENSSL_free(localSig);
        return false;
    }

    if(EVP_DigestSignFinal(this->mdctx_sign, localSig, &sig_len) != 1) {
        return false;
    }

    sig = new unsigned char[sig_len];

    memcpy(sig, localSig, sig_len);

    OPENSSL_free(localSig);

    return true;
}

bool V2VSecurity::verifyMessage(char *msg, evp_pkey_st *publicKey, const unsigned char* signature, size_t sig_len) {

    if(EVP_DigestVerifyInit(this->mdctx_verify, nullptr, EVP_sha256(), nullptr, publicKey) != 1) {
        return false;
    }

    if(EVP_DigestVerifyUpdate(this->mdctx_verify, msg, strlen(msg)) != 1) {
        return false;
    }

    if(EVP_DigestVerifyFinal(this->mdctx_verify, signature, sig_len) == 1) {
        return true;
    }
    else {
        return false;
    }


}