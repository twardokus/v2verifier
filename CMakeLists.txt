cmake_minimum_required(VERSION 3.20)
project(v2verifier)

set(SOURCE_FILES
    src/main.cpp
    src/Vehicle.cpp
    src/v2vcrypto.cpp
    src/bsm.cpp
    src/threading.cpp
    src/BasicSafetyMessage.cpp
    src/Ieee1609Dot2Data.cpp
    src/Ieee1609Dot2Content.cpp
    src/SignedData.cpp
        src/ToBeSignedData.cpp
        include/ToBeSignedData.h
        src/SignedDataPayload.cpp
        include/SignedDataPayload.h
        src/HeaderInfo.cpp
        include/HeaderInfo.h
        src/OctetString.cpp
        include/OctetString.h
        src/UnsecuredData.cpp
        include/UnsecuredData.h
        src/SignerIdentifier.cpp
        include/SignerIdentifier.h
        src/CertificateBase.cpp
        include/CertificateBase.h
        src/ToBeSignedCertificate.cpp
        include/ToBeSignedCertificate.h
)

##------------------------------------------------------------
## macOS stuff
set(CMAKE_OSX_ARCHITECTURES arm64)
set(OPENSSL_ROOT_DIR /opt/homebrew/Cellar/openssl@3/3.1.3)
set(Boost_NO_SYSTEM_PATHS TRUE)
set(BOOST_ROOT /opt/homebrew/Cellar/boost/1.82.0_1)
set(Boost_LIBRARY_DIRS "${BOOST_ROOT}/lib/")
##------------------------------------------------------------


find_package(OpenSSL REQUIRED)
find_package(Boost REQUIRED)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

target_link_libraries(${PROJECT_NAME} OpenSSL::Crypto)

##------------------------------------------------------------
## macOS stuff
target_link_libraries(${PROJECT_NAME} Boost::boost)
target_include_directories(${PROJECT_NAME} PRIVATE ${BOOST_INCLUDE_DIRS})
target_include_directories(${PROJECT_NAME} PUBLIC ${OPENSSL_INCLUDE_DIR})
##------------------------------------------------------------

target_include_directories(${PROJECT_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/include)

set_property(TARGET v2verifier PROPERTY CXX_STANDARD 20)