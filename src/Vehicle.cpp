#include <sys/socket.h>
#include <netinet/in.h>
#include <cstring>
#include <unistd.h>
#include <iostream>
#include <chrono>
#include <openssl/err.h>
#include "Vehicle.h"
#include <openssl/pem.h>
#include <thread>
#include <sstream>


std::string Vehicle::get_hostname() {
   return hostname;
}

void Vehicle::transmit(int num_msgs, bool test) {

    // create socket and send data
    //std::cout << "Vehicle " << this->number << " made it here" << std::endl;

    int sockfd;
    struct sockaddr_in servaddr;

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));

    servaddr.sin_family = AF_INET;
    if(test)
        servaddr.sin_port = htons(6666);
    else
        servaddr.sin_port = htons(52001);
    servaddr.sin_addr.s_addr = INADDR_ANY;

    int n, len;

    for(int i =0; i < num_msgs; i++) {

        ecdsa_spdu next_spdu;
        generate_ecdsa_spdu(next_spdu);
        sendto(sockfd, (struct ecdsa_spdu *) &next_spdu, sizeof(next_spdu), MSG_CONFIRM,
               (const struct sockaddr *) &servaddr, sizeof(servaddr));

        std::this_thread::sleep_for(std::chrono::milliseconds(100));

    }

    close(sockfd);

}

void Vehicle::receive(int num_msgs, bool test) {

    int sockfd;
    struct sockaddr_in servaddr, cliaddr;

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));

    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    //std::cout << arg_pars.istest << std::endl;

    uint16_t port = test ? 6666 : 4444;
    std::cout << port << std::endl;
    servaddr.sin_port = htons(port);

    if(bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("Socket bind failed");
        exit(EXIT_FAILURE);
    }

    unsigned int len;

    len = sizeof(cliaddr);

    ecdsa_spdu incoming_spdu;

    // this is to prevent a truly infinite loop
    int received_message_counter = 0;

    // for getting times when BSMs are received (security check for replay attacks)
    using timestamp = std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds>;

    while (received_message_counter < num_msgs) {
        recvfrom(sockfd, (struct ecdsa_spdu *) &incoming_spdu, sizeof(ecdsa_spdu), 0, (struct sockaddr *) &cliaddr,
                 (socklen_t *) len);

        timestamp received_time = std::chrono::time_point_cast<std::chrono::microseconds>(std::chrono::system_clock::now());

        std::cout << incoming_spdu.vehicle_id << std::endl;
        int vehicle_id_number = incoming_spdu.vehicle_id;


        bool valid_spdu = verify_message_ecdsa(incoming_spdu, received_time, vehicle_id_number);
        for(int i = 0; i < 80; i++) std::cout << "-"; std::cout << std::endl;
        print_spdu(incoming_spdu, valid_spdu);
        print_bsm(incoming_spdu);
        received_message_counter++;

    }

    exit(0);

}

void Vehicle::generate_ecdsa_spdu(Vehicle::ecdsa_spdu &spdu) {
    spdu.vehicle_id = this->number;

    // BSM
    spdu.data.signedData.tbsData.message = generate_bsm();

    // timestamp
    using timestamp = std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds>;
    timestamp ts = std::chrono::time_point_cast<std::chrono::microseconds>(std::chrono::system_clock::now());
    spdu.data.signedData.tbsData.headerInfo.timestamp = ts;

    spdu.data.signedData.cert = vehicle_certificate_ecdsa;

    // sign the certificate
    unsigned char certificate_digest[SHA256_DIGEST_LENGTH];
    sha256sum(&spdu.data.signedData.cert,sizeof(spdu.data.signedData.cert), certificate_digest);
    ecdsa_sign(certificate_digest, cert_private_ec_key, &certificate_buffer_length, certificate_signature);

    // copy the certificate signature buffer and certificate signature into the SPDU
    spdu.certificate_signature_buffer_length = certificate_buffer_length;
    for(int i = 0; i < certificate_buffer_length; i++) {
        spdu.data.certificate_signature[i] = certificate_signature[i];
    }

    sign_message_ecdsa(spdu);

}

bsm Vehicle::generate_bsm() {
    bsm new_bsm = {10, 10, 10, 30, 0};
    return new_bsm;
}

void Vehicle::print_bsm(Vehicle::ecdsa_spdu &spdu) {

    std::cout << "BSM received!" << std::endl;
    std::cout << "\tLocation:\t";
    std::cout << spdu.data.signedData.tbsData.message.latitude;
    std::cout << ", ";
    std::cout << spdu.data.signedData.tbsData.message.longitude;
    std::cout <<", ";
    std::cout << spdu.data.signedData.tbsData.message.elevation;
    std::cout << std::endl;
    std::cout << "\tSpeed:\t\t" << spdu.data.signedData.tbsData.message.speed << std::endl;
    std::cout << "\tHeading:\t" << spdu.data.signedData.tbsData.message.heading << std::endl;
}

/*
 * This is largely a debugging function so we can print and view received data, e.g., to make sure that things are being
 * sent and received properly.
 */
void Vehicle::print_spdu(Vehicle::ecdsa_spdu &spdu, bool valid) {
    std::cout << "SPDU received!" << std::endl;
    std::cout << "\tID:\t" << (int) spdu.vehicle_id << std::endl;
    std::cout << "\tValid:\t";
    valid ? std::cout << "TRUE" : std::cout << "FALSE";
    std::cout << std::endl;

    std::cout << "\tSent:\t" << std::chrono::system_clock::to_time_t(spdu.data.signedData.tbsData.headerInfo.timestamp) << std::endl;
}

void Vehicle::sign_message_ecdsa(Vehicle::ecdsa_spdu &spdu) {

    unsigned char hash[SHA256_DIGEST_LENGTH];
    sha256sum(&spdu.data.signedData.tbsData, sizeof(spdu.data.signedData.tbsData), hash);

    unsigned int signature_buffer_length = ECDSA_size(private_ec_key);
    auto signature = (unsigned char*) OPENSSL_malloc(signature_buffer_length);
    ecdsa_sign(hash, private_ec_key, &signature_buffer_length, signature);

    spdu.signature_buffer_length = signature_buffer_length;

    for(int i = 0; i < signature_buffer_length; i++) {
        spdu.signature[i] = signature[i];
    }

}

bool Vehicle::verify_message_ecdsa(Vehicle::ecdsa_spdu &spdu, std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds> received_time, int vehicle_id) {

    EC_KEY *verification_private_ec_key = nullptr, *verification_cert_private_ec_key = nullptr;

    load_key(vehicle_id, false, verification_private_ec_key);
    load_key(vehicle_id, true, verification_cert_private_ec_key);

    // Verify certificate signature
    unsigned char certificate_hash[SHA256_DIGEST_LENGTH];
    sha256sum(&spdu.data.signedData.cert, sizeof(spdu.data.signedData.cert), certificate_hash);
    bool cert_result = ecdsa_verify(certificate_hash, spdu.data.certificate_signature, &spdu.certificate_signature_buffer_length, verification_cert_private_ec_key);

    // Verify message signature
    unsigned char hash[SHA256_DIGEST_LENGTH];
    sha256sum(&spdu.data.signedData.tbsData, sizeof(spdu.data.signedData.tbsData), hash);
    bool sig_result = ecdsa_verify(hash, spdu.signature, &spdu.signature_buffer_length, verification_private_ec_key);

    // Verify time constraint: message is valid if less than 30 seconds (30000ms) have elapsed since transmission
    std::chrono::duration<double, std::milli> elapsed_time =  received_time -  spdu.data.signedData.tbsData.headerInfo.timestamp;
    bool recent = elapsed_time.count() < 30000;

    // Return result
    return cert_result && sig_result && recent;
}

void Vehicle::load_key(int number,  bool certificate, EC_KEY *&key_to_store){

    std::string temp = certificate ? "../cert_keys/" + std::to_string(number) + "/p256.key" :
            "../keys/" + std::to_string(number) + "/p256.key";

    const char* filepath = temp.c_str();

    FILE *fp = fopen(filepath,"r");
    if(fp != nullptr) {
        EVP_PKEY *key = nullptr;
        PEM_read_PrivateKey(fp, &key, nullptr, nullptr);
        key_to_store = nullptr;
        if (!key) {
            perror("Error while loading the key from file\n");
            exit(EXIT_FAILURE);
        }
        if (!(key_to_store = EVP_PKEY_get1_EC_KEY(key))) {
            perror("Error while getting EC key from loaded key\n");
            exit(EXIT_FAILURE);
        }
    }
    else {
        std::cout << filepath << std::endl;
        std::cout << "Error while opening file from path. Error number : " << errno << std::endl;
        exit(EXIT_FAILURE);
    }

}
