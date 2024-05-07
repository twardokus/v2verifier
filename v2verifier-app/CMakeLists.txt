set(MAIN_SOURCE_FILE
    ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp
        src/Vehicle.cpp
        include/Vehicle.hpp
        src/V2VSecurity.cpp
        include/V2VSecurity.hpp)

set(APP_NAME v2verifier)

add_executable(${APP_NAME} ${SOURCE_FILES} ${MAIN_SOURCE_FILE})

target_link_libraries(${PROJECT_NAME} OpenSSL::Crypto)
target_link_libraries(${APP_NAME} ${V2V_LIBRARIES})

enable_testing()
add_subdirectory(test)