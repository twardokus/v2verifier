//
// Created by Geoff Twardokus on 10/19/23.
//

#include "Ieee1609Dot2Data.h"

Ieee1609Dot2Data::Ieee1609Dot2Data(UnsecuredData _data, bool _secure) {
    if(_secure) {
        this->contentTypeIndicator = signedData;
    }
    else {
        this->contentTypeIndicator = unsecuredData;
        this->unsecuredDataContent = UnsecuredData(_data);
    }
}

Ieee1609Dot2Data::Ieee1609Dot2Data(Ieee1609Dot2Data &_data) {
    this->contentTypeIndicator = _data.getContentTypeIndicator();
    this->signedDataContent = SignedData(_data.getSignedDataContent());
    this->unsecuredDataContent = UnsecuredData(_data.getUnsecuredDataContent());
}