set(SOURCE_FILES
    include/test.hpp
    src/test.cpp)

set(APP_NAME v2verifier)

add_executable(${APP_NAME} ${SOURCE_FILES})
target_link_libraries(${APP_NAME} ${V2V_LIBRARIES})