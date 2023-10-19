//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_OCTETSTRING_H
#define V2VERIFIER_OCTETSTRING_H

#include <cstdlib>
#include <vector>


class OctetString {

public:

    OctetString() = default;
    OctetString(OctetString& octetString) {
        this->data = octetString.getData();
    }

    OctetString(std::vector<uint8_t> _data) {
        this->data = _data;
    }

    const std::vector<uint8_t>& getData();
    void setData(std::vector<uint8_t> _data);

private:
    std::vector<uint8_t> data;

};


#endif //V2VERIFIER_OCTETSTRING_H
