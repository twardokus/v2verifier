//
// Created by Geoff Twardokus on 10/19/23.
//

#ifndef V2VERIFIER_BASICSAFETYMESSAGE_H
#define V2VERIFIER_BASICSAFETYMESSAGE_H


class BasicSafetyMessage {

    public:

        BasicSafetyMessage(float _latitude, float _longitude, float _elevation, float _heading, float _speed);

        void setLatitude(float _latitude);
        void setLongitude(float _longitude);
        void setElevation(float _elevation);
        void setSpeed(float _speed);
        void setHeading(float _heading);

    private:

        float latitude;
        float longitude;
        float elevation;
        float speed;
        float heading;
};


#endif //V2VERIFIER_BASICSAFETYMESSAGE_H
