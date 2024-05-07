/** @file   V2VSecurity.hpp
 *  @brief  Message signing and cryptomaterial management functions.
 *
 *  @author Geoff Twardokus
 *
 *  @bug    No known bugs
*/

#ifndef V2VERIFIER_V2VSECURITY_HPP
#define V2VERIFIER_V2VSECURITY_HPP

#define ECDSA_P256_DER_LENGTH_BYTES 72

#include <openssl/evp.h>
#include <string>
#include <fstream>

class V2VSecurity {

public:

    /** @brief  Explicitly deleted default constructor. We never want a security manager module that does not have
     *          a key loaded at initialization. */
    V2VSecurity() = delete;

    /** @brief  Create a new V2VSecurity module from a provided PEM key file.
     *
     *  @param  pemFilename Filepath to the public/private keypair to be used for signing and verifying messages.
     */
    explicit V2VSecurity(std::string &pemFilename);

    /** @brief Destructor */
    ~V2VSecurity();

    /** @brief  Sign arbitrary data with ECDSA P.256. Allocates new memory on the heap to store the `sig` value.
     *
     *  @param  msg     Pointer to the raw message data to be signed.
     *  @param  sig     Pointer to be used to store the signature.
     *  @param  sig_len Length of the generated signature
     *  @return         True if signature is successfully generated, false if errors are encountered.
     */
    bool signMessage(char* msg, unsigned char* &sig, size_t &sig_len);

    /** @brief  Verify ECDSA P.256 signature.
     *
     *  @param msg          Pointer to the raw message data to be verified.
     *  @param publicKey    Pointer to the public key to be used for verification.
     *  @param signature    Pointer to the ECDSA signature to be verified.
     *  @param sig_len      Length of the signature to be verified.
     *  @return             True on successful verification, false on error or verification failure.
     */
    bool verifyMessage(char *msg, evp_pkey_st *publicKey, const unsigned char* signature, size_t sig_len);

    EVP_PKEY *pkey = nullptr;

private:

    std::ifstream pemfile;

    EVP_MD_CTX *mdctx_sign = nullptr;
    EVP_MD_CTX *mdctx_verify = nullptr;

    /** @brief  Load a public/private keypair from a provided filepath.
     *
     * @param   filename  Path to the file from which to load the keypair.
     */
    void loadPEMFile(std::string &filename);

    /** @brief  Initialize various OPENSSL contexts and signature primitives for later use. */
    void setup();

};


#endif //V2VERIFIER_V2VSECURITY_HPP
