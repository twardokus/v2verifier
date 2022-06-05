set(CMAKE_CXX_STANDARD 14)
set(PROJECT_SOURCE_DIR src)

set(CMAKE_CXX_FLAGS "-pthread")

set(SOURCES main.cpp Vehicle.cpp v2vcrypto.cpp)
add_executable(v2verifier ${SOURCES})
include_directories(${v2verifier_SOURCE_DIR}/include)
target_link_libraries(v2verifier crypto)
