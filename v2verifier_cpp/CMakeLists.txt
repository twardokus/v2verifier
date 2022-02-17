cmake_minimum_required(VERSION 3.20)
project(cpp)

set(CMAKE_CXX_STANDARD 14)

add_executable(cpp main.cpp Vehicle.cpp Vehicle.h VehicleUtil.cpp VehicleUtil.h ieee16092.h bsm.h certificates.h v2vcrypto.h v2vcrypto.cpp)
target_include_directories(cpp PRIVATE /usr/local/include/oqs)

target_link_libraries(cpp crypto oqs)
