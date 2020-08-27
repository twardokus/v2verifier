"""
The proposed design is to build the structure using a standard Python dictionary. Then, the dictionary can be converted to a standard-compliant bytestring for realistic 
transmission encapsulated within a WSMP packet.
On reception, the string can be decoded back into a Python dictionary for further processing.
"""

IEEE1609Dot2Data = {
    
    "ProtocolVersion":3,
    "IEEE1609Dot2Content":{
        "SignedData":{
                "hashID":"SHA256",
                "ToBeSignedData":{
                        "SignedDataPayload":{
                                "data":None,
                                "extDataHash":None,
                            },
                        "headerInfo":{
                                "PSID":32,
                                "generationTime":None,
                                "expirationTime":None
                            }
                    },
                "SignerIdentifier":{
                    "digest":None,
                    "certificate":None,
                    "self":None
                    },
                "Signature":{
                    "ecdsaP256Signature":{
                            "r":None,
                            "s":None
                        }
                    }
                
            }
        }
    }


if __name__=="__main__":
    print()