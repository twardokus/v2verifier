// Copyright (c) 2022. Geoff Twardokus
// Reuse permitted under the MIT License as specified in the LICENSE file within this project.

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
#include <fstream>
#include <stdio.h>
#include <bitset>


std::string Vehicle::get_hostname() {
   return hostname;
}

void Vehicle::transmit(int num_msgs, bool test) {

    // create socket and send data
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
        generate_ecdsa_spdu(next_spdu, i);
        sendto(sockfd, (struct ecdsa_spdu *) &next_spdu, sizeof(next_spdu), MSG_CONFIRM,
               (const struct sockaddr *) &servaddr, sizeof(servaddr));

        std::this_thread::sleep_for(std::chrono::milliseconds(100));

    }

    close(sockfd);

}

void Vehicle::transmitLearnRequest(bool test) {
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

    ecdsa_spdu spdu;
    generate_ecdsa_spdu(spdu, 0);

    //TODO: this splicing should probably be moved to when the certificate is created.
    ((uint16_t *)&spdu.data.signedData.cert.commonCertFields)[1] = 0;
    ((uint16_t *)&spdu.data.signedData.cert.commonCertFields)[11] = 0;
    ((uint16_t *)&spdu.data.signedData.cert.commonCertFields)[5] = 0x84;
    printHex(&spdu.data.signedData.cert, sizeof(spdu.data.signedData.cert));

    unsigned char hash[SHA256_DIGEST_LENGTH];
    sha256sum(&spdu.data.signedData.cert, sizeof(spdu.data.signedData.cert), hash);

    unsigned char certHash[4];
    certHash[0] = hash[29];
    certHash[1] = hash[30];
    certHash[2] = hash[31];
    certHash[3] = '\0';

    //printHex(hash, sizeof(hash));
    //printHex(certHash, sizeof(certHash));

    strncpy(spdu.data.signedData.tbsData.headerInfo.p2pLearningRequest, (const char *) certHash, 4);

    std::cout << "Outbound learn request";
    printHex(&spdu, sizeof(spdu));
    std::cout << std::endl;
    sendto(sockfd, (struct ecdsa_spdu *) &spdu, sizeof(spdu), MSG_CONFIRM, (const struct sockaddr *) &servaddr, sizeof(servaddr));

    close(sockfd);
}

void Vehicle::transmitLearnResponse(char* cert, bool test) {
    // create socket and send data
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

    // Create a P2PCD response PDU
    std::cout << "Making PDU:";
    Ieee1609dot2Peer2PeerPDU pdu;
    ((uint16_t *)&pdu.caCerts[0].commonCertFields)[1] = 0;
    ((uint16_t *)&pdu.caCerts[0].commonCertFields)[11] = 0;
    ((uint16_t *)&pdu.caCerts[0].commonCertFields)[5] = 0x84;
    ((uint8_t *)&pdu.caCerts[0])[37] = 0;
    printHex(&pdu, sizeof(pdu));

    ecdsa_explicit_certificate testCert;
    ((uint16_t *)&testCert.commonCertFields)[1] = 0;
    ((uint16_t *)&testCert.commonCertFields)[11] = 0;
    ((uint16_t *)&testCert.commonCertFields)[5] = 0x84;
    std::cout << "The certificate that should be placed into response PDU:";
    printHex(&testCert, sizeof(ecdsa_explicit_certificate));

    std::cout << "Certificate placed into response PDU:";
    printHex(&pdu.caCerts[0], sizeof(pdu.caCerts[0]));

    unsigned char hash[SHA256_DIGEST_LENGTH];
    sha256sum(&pdu.caCerts[0], sizeof(ecdsa_explicit_certificate), hash);
    std::cout << "sha256sum of response cert:";
    printHex(hash, SHA256_DIGEST_LENGTH);

    sendto(sockfd, (struct ecdsa_spdu *) &pdu, sizeof(pdu), MSG_CONFIRM,(const struct sockaddr *) &servaddr, sizeof(servaddr));

    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    close(sockfd);
}

void Vehicle::receive(int num_msgs, bool test, bool tkgui) {

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

    uint16_t port = test ? 6666 : 4444;
    servaddr.sin_port = ntohs(port);

    if(bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("Socket bind failed");
        exit(EXIT_FAILURE);
    }

    /***********************************/
    // tkgui socket
    int sockfd2;
    struct sockaddr_in servaddr2;

    if ((sockfd2 = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr2, 0, sizeof(servaddr2));

    servaddr2.sin_family = AF_INET;
    servaddr2.sin_port = ntohs(9999);
    servaddr2.sin_addr.s_addr = INADDR_ANY;

    int n2, len2;
    /***********************************/


    unsigned int len;
    len = sizeof(cliaddr);

    ecdsa_spdu incoming_spdu;

    // this is to prevent a truly infinite loop
    int received_message_counter = 0;

    // for getting times when BSMs are received (security check for replay attacks)
    using timestamp = std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds>;

    while (received_message_counter < num_msgs) {
        if(test) {
            recvfrom(sockfd, (struct ecdsa_spdu *) &incoming_spdu, sizeof(ecdsa_spdu), 0, (struct sockaddr *) &cliaddr,
                     (socklen_t *) len);
        }
        else {
            // with DSRC headers (when data is from SDR), we have an extra 57 bytes (304 + 57 = 361)
            uint8_t buffer[361];
            recvfrom(sockfd,  &buffer, 361, 0, (struct sockaddr *) &cliaddr,
                     (socklen_t *) len);

            uint8_t spdu_buffer[sizeof(incoming_spdu)];
            for(int i = 360, j = sizeof(incoming_spdu) - 1; i > 57; i--, j--) {
                spdu_buffer[j] = buffer[i];
            }

            memcpy(&incoming_spdu, spdu_buffer, sizeof(incoming_spdu));

        }
        timestamp received_time = std::chrono::time_point_cast<std::chrono::microseconds>(std::chrono::system_clock::now());

        std::cout << incoming_spdu.vehicle_id << std::endl;
        int vehicle_id_number = incoming_spdu.vehicle_id;


        bool valid_spdu = verify_message_ecdsa(incoming_spdu, received_time, vehicle_id_number);

        // forward to GUI if applicable
        if(tkgui) {
            packed_bsm_for_gui data_for_gui = {incoming_spdu.data.signedData.tbsData.message.latitude,
                                               incoming_spdu.data.signedData.tbsData.message.longitude,
                                               incoming_spdu.data.signedData.tbsData.message.elevation,
                                               incoming_spdu.data.signedData.tbsData.message.speed,
                                               incoming_spdu.data.signedData.tbsData.message.heading,
                                               valid_spdu,
                                               true,
                                               7,
                                               (float) vehicle_id_number};
            sendto(sockfd2, (struct packed_bsm_for_gui *) &data_for_gui, sizeof(data_for_gui),
                    MSG_CONFIRM, (const struct sockaddr *) &servaddr2, sizeof(servaddr2));
        }
        // print results
        for(int i = 0; i < 80; i++) std::cout << "-"; std::cout << std::endl;
        print_spdu(incoming_spdu, valid_spdu);
        print_bsm(incoming_spdu);
        received_message_counter++;

    }
    close(sockfd2);
    close(sockfd);
}

void Vehicle::receiveLearnRequest(char* dest, bool test, bool tkgui) {
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

    uint16_t port = test ? 6666 : 4444;
    servaddr.sin_port = ntohs(port);

    if(bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("Socket bind failed");
        exit(EXIT_FAILURE);
    }

    /***********************************/
    // tkgui socket
    int sockfd2;
    struct sockaddr_in servaddr2;

    if ((sockfd2 = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr2, 0, sizeof(servaddr2));

    servaddr2.sin_family = AF_INET;
    servaddr2.sin_port = ntohs(9999);
    servaddr2.sin_addr.s_addr = INADDR_ANY;

    int n2, len2;
    /***********************************/


    unsigned int len;
    len = sizeof(cliaddr);

    ecdsa_spdu incoming_spdu;
    std::cout << "Request length: " << sizeof(ecdsa_spdu) << std::endl;

    if(test) {
        recvfrom(sockfd, (struct ecdsa_spdu *) &incoming_spdu, sizeof(ecdsa_spdu), 0, (struct sockaddr *) &cliaddr,
                 (socklen_t *) len);
        std::cout << "Inbound learn request:";
        printHex(&incoming_spdu, sizeof(incoming_spdu));
        std::cout << std::endl;
    }
    else {
        // with DSRC headers (when data is from SDR transceiver), we have an extra 80 bytes (280 + 80 = 360)
        uint8_t buffer[360];
        recvfrom(sockfd,  &buffer, 360, 0, (struct sockaddr *) &cliaddr,
                 (socklen_t *) len);

        uint8_t spdu_buffer[sizeof(incoming_spdu)];
        for(int i = 360, j = sizeof(incoming_spdu) - 1; i > 80; i--, j--) {
            spdu_buffer[j] = buffer[i];
        }

        memcpy(&incoming_spdu, spdu_buffer, sizeof(incoming_spdu));

        std::cout << "Inbound SPDU from radio";
        printHex(&incoming_spdu, sizeof(incoming_spdu));
        std::cout << std::endl;
    }
    std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds> received_time =
            std::chrono::time_point_cast<std::chrono::microseconds>(std::chrono::system_clock::now());

    std::cout << incoming_spdu.vehicle_id << std::endl;
    int vehicle_id_number = incoming_spdu.vehicle_id;


    bool valid_spdu = verify_message_ecdsa(incoming_spdu, received_time, vehicle_id_number);
    bool learnRequestPresent = strcmp(incoming_spdu.data.signedData.tbsData.headerInfo.p2pLearningRequest, "000");

    /******************************************************************************************************************/
    // forward to GUI if applicable
    if(tkgui) {
        packed_bsm_for_gui data_for_gui = {incoming_spdu.data.signedData.tbsData.message.latitude,
                                           incoming_spdu.data.signedData.tbsData.message.longitude,
                                           incoming_spdu.data.signedData.tbsData.message.elevation,
                                           incoming_spdu.data.signedData.tbsData.message.speed,
                                           incoming_spdu.data.signedData.tbsData.message.heading,
                                           valid_spdu,
                                           true,
                                           7,
                                           (float) vehicle_id_number};
        sendto(sockfd2, (struct packed_bsm_for_gui *) &data_for_gui, sizeof(data_for_gui),
               MSG_CONFIRM, (const struct sockaddr *) &servaddr2, sizeof(servaddr2));
    }
    /******************************************************************************************************************/

    close(sockfd);

    char certHash[4];
    strncpy(certHash, incoming_spdu.data.signedData.tbsData.headerInfo.p2pLearningRequest, 4);

    std::cout << "Received HashedID3: " << std::endl;
    printHex(&certHash, sizeof(certHash));

    strncpy(dest, certHash, 3);
}

void Vehicle::receiveLearnResponse(bool test, bool tkgui) {
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

    // The response uses a separate port because GNUradio needs a separate UDP sink block to listen for a smaller
    // packet. This block needs a new port num.
    uint16_t port = test ? 6666 : 4445;
    servaddr.sin_port = ntohs(port);

    if(bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("Socket bind failed");
        exit(EXIT_FAILURE);
    }

    /***********************************/
    // tkgui socket
    int sockfd2;
    struct sockaddr_in servaddr2;

    if ((sockfd2 = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr2, 0, sizeof(servaddr2));

    servaddr2.sin_family = AF_INET;
    servaddr2.sin_port = ntohs(9999);
    servaddr2.sin_addr.s_addr = INADDR_ANY;

    int n2, len2;
    /***********************************/


    unsigned int len;
    len = sizeof(cliaddr);

    Ieee1609dot2Peer2PeerPDU incoming_pdu;
    std::cout << "Response length: " << sizeof(incoming_pdu) << std::endl;

    if(test) {
        recvfrom(sockfd, (struct ecdsa_spdu *) &incoming_pdu, sizeof(incoming_pdu), 0, (struct sockaddr *) &cliaddr,
                 (socklen_t *) len);
    }
    else {
        // with DSRC headers (when data is from SDR), we have an extra 80 bytes (48 + 80 = 128)
        uint8_t buffer[128];
        recvfrom(sockfd,  &buffer, 128, 0, (struct sockaddr *) &cliaddr,
                 (socklen_t *) len);

        std::cout << "raw buffer contains:";
        printHex(buffer, sizeof(buffer));

        uint8_t spdu_buffer[sizeof(incoming_pdu)];
        std::memset(&spdu_buffer, 0, sizeof(incoming_pdu));
        /*for(int i = 128, j = sizeof(incoming_pdu) - 1; i > 80; i--, j--) {
            spdu_buffer[j] = buffer[i];
        }*/
        for (int i = 81, j = 0; i < 125; i++, j++) spdu_buffer[j] = buffer[i];

        std::cout << "spdu_buffer contains: ";
        printHex(spdu_buffer, sizeof(spdu_buffer));

        memcpy(&incoming_pdu, spdu_buffer, sizeof(incoming_pdu));

    }
    std::chrono::time_point<std::chrono::system_clock, std::chrono::microseconds> received_time =
            std::chrono::time_point_cast<std::chrono::microseconds>(std::chrono::system_clock::now());

    close(sockfd);

    std::cout << "Received Ieee1609dot2Peer2PeerPDU:";
    printHex(&incoming_pdu, sizeof(incoming_pdu));

    std::cout << "Received certificate";
    printHex(&incoming_pdu.caCerts[0], sizeof(incoming_pdu.caCerts[0]));

    unsigned char hash[SHA256_DIGEST_LENGTH];
    sha256sum(&incoming_pdu.caCerts[0], sizeof(ecdsa_explicit_certificate), hash);

    std::cout << "sha256sum of received certificate:";
    printHex(hash, SHA256_DIGEST_LENGTH);

    std::cout << "Received HashedID3:";
    unsigned char certHash[4];
    certHash[0] = hash[29];
    certHash[1] = hash[30];
    certHash[2] = hash[31];
    certHash[3] = '\0';
    printHex(certHash, 3);
}

void Vehicle::generate_ecdsa_spdu(Vehicle::ecdsa_spdu &spdu, int timestep) {
    spdu.vehicle_id = this->number;

    // BSM
    spdu.data.signedData.tbsData.message = generate_bsm(timestep);

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


bsm Vehicle::generate_bsm(int timestep) {
    float latitude = this->timestep[timestep][0];
    float longitude = this->timestep[timestep][1];
    float elevation = this->timestep[timestep][2];
    float speed = 0;
    float heading = 0;
    if(timestep != 0) {
        speed = calculate_speed_kph(this->timestep[timestep - 1][0],
                                    latitude,
                                    this->timestep[timestep - 1][1],
                                    longitude,
                                    100);

        heading = calculate_heading(this->timestep[timestep - 1][0],
                                    latitude,
                                    this->timestep[timestep - 1][1],
                                    longitude);
    }
    bsm new_bsm = {latitude, longitude, elevation, speed, heading};
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

void Vehicle::print_spdu(Vehicle::ecdsa_spdu &spdu, bool valid, bool learnRequest) {
    std::cout << "SPDU received!" << std::endl;
    std::cout << "\tID:\t" << (int) spdu.vehicle_id << std::endl;
    std::cout << "\tLearning Request Field contains: " << spdu.data.signedData.tbsData.headerInfo.p2pLearningRequest << std::endl;
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

void Vehicle::load_trace(int number) {
    std::string line;
    std::string word;

    std::fstream file("../trace_files/" + std::to_string(number) + ".csv", std::ios::in);
    if(file.is_open()) {
        while(getline(file, line)) {
            timestep_data.clear();
            std::stringstream str(line);
            while(getline(str, word, ',')) {
                timestep_data.push_back(std::stof(word));
            }
            timestep.push_back(timestep_data);
        }
    }
    else {
        perror(("Error opening trace file for vehicle " + std::to_string(number)).c_str());
        exit(EXIT_FAILURE);
    }
}

/**
 * Debugging method for checking byte-level values. Added to investigate inconsistent hash values.
 * Prints hexadecimal values in batches of shorts with alignment.
 * @param ptr A pointer to the object to print out
 * @param size The size of the object in bytes. sizeof() will suffice.
 */
void Vehicle::printHex(void* ptr, int size) {
    int N = size % 2 == 1 ? size / 2 + 1 : size / 2; // never tested with an odd size just beware

    for (int i = 0; i < N; i++) {
        if (i % 4 == 0) std::cout << std::endl; //new line every 4 shorts/8bytes to show memory alignment
        uint16_t c = htons(((uint16_t *)ptr)[i]); // We cast ptr to uint16_t* to treat it as an array of shorts
        std::cout << std::hex << c << ' ';
    }
    /*for (int i = 0; i < size; i++) {
        if (i % 8 == 0) std::cout << std::endl;
        unsigned int c = ((unsigned int*)ptr)[i];
        std::cout << std::hex << c;
        if (i % 2 == 0) std::cout << ' ';
    }*/

    std::cout << std::endl << std::endl << std::flush;
}