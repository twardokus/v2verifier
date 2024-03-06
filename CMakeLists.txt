cmake_minimum_required(VERSION 3.10)
project(v2verifier)

set(SOURCE_FILES
    src/main.cpp
    src/Vehicle.cpp
    src/v2vcrypto.cpp
    src/bsm.cpp
    src/threading.cpp)


if(${CMAKE_SYSTEM_NAME} STREQUAL "Darwin")
    ##------------------------------------------------------------
    ## macOS stuff
    set(CMAKE_OSX_ARCHITECTURES arm64)
    set(OPENSSL_ROOT_DIR /opt/homebrew/Cellar/openssl@3/3.2.1)
    set(Boost_NO_SYSTEM_PATHS TRUE)
    set(BOOST_ROOT /opt/homebrew/Cellar/boost/1.84.0)
    set(Boost_LIBRARY_DIRS "${BOOST_ROOT}/lib/")
    ##------------------------------------------------------------
endif()

find_package(OpenSSL REQUIRED)
find_package(Boost REQUIRED)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

target_link_libraries(${PROJECT_NAME} OpenSSL::Crypto)

if(${CMAKE_SYSTEM_NAME} STREQUAL "Darwin")
    ##------------------------------------------------------------
    ## macOS stuff
    target_link_libraries(${PROJECT_NAME} Boost::boost)
    target_include_directories(${PROJECT_NAME} PRIVATE ${BOOST_INCLUDE_DIRS})
    target_include_directories(${PROJECT_NAME} PUBLIC ${OPENSSL_INCLUDE_DIR})
    ##------------------------------------------------------------
endif()

target_include_directories(${PROJECT_NAME} PRIVATE ${PROJECT_SOURCE_DIR}/include)

set_property(TARGET v2verifier PROPERTY CXX_STANDARD 20)