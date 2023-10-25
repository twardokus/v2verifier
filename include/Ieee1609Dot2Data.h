//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_IEEE1609DOT2DATA_H
#define V2VERIFIER_IEEE1609DOT2DATA_H


#include <cstdint>

#include "Ieee1609Dot2Content.h"
#include "SignedData.h"
#include "UnsecuredData.h"

enum contentType {
    unsecuredData,
    signedData
};

class Ieee1609Dot2Data {

public:

    Ieee1609Dot2Data(UnsecuredData _data, bool _secure);
    Ieee1609Dot2Data(Ieee1609Dot2Data& _data);

    uint8_t getProtocolVerstion() const;
    contentType getContentTypeIndicator() const;
    SignedData getSignedDataContent() const;
    UnsecuredData getUnsecuredDataContent() const;

    void setContentType(contentType _type);
    void setUnsecuredDataContent(SignedData& _unsecuredData);
    void setSignedDataContent(SignedData& _signedData);

private:
    /** Always 3 in IEEE1609.2-2022 */
    const uint8_t protocolVersion = 3;
    contentType contentTypeIndicator;
    SignedData signedDataContent;
    UnsecuredData unsecuredDataContent;
};


#endif //V2VERIFIER_IEEE1609DOT2DATA_H
