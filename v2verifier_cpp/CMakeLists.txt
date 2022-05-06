#cmake_minimum_required(VERSION 3.)
project(v2verifier)

set(CMAKE_CXX_STANDARD 14)

add_executable(v2verifier main.cpp Vehicle.cpp Vehicle.h ieee16092.h bsm.h certificates.h v2vcrypto.h v2vcrypto.cpp arguments.h)


target_link_libraries(v2verifier crypto)
