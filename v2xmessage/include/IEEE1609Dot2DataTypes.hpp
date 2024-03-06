//
// Created by Geoff Twardokus on 3/6/24.
//

#ifndef V2VERIFIER_IEEE1609DOT2DATATYPES_HPP
#define V2VERIFIER_IEEE1609DOT2DATATYPES_HPP

namespace IEEE1609Dot2DataTypes {

    /*
    HashAlgorithm ::= ENUMERATED {
            sha256,
            ...,
            sha384,
            sm3
    }
    */
    enum HashAlgorithm {
        sha256,
        sha384,
        sm3
    };

}

#endif //V2VERIFIER_IEEE1609DOT2DATATYPES_HPP
