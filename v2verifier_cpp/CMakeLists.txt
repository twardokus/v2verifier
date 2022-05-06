cmake_minimum_required(VERSION 3.15)
project(v2verifier)

set(CMAKE_CXX_STANDARD 14)
set(SOURCES main.cpp Vehicle.cpp v2vcrypto.cpp)

add_executable(v2verifier ${SOURCES})
target_include_directories(v2verifier PUBLIC include)

target_link_libraries(v2verifier crypto)
