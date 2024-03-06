set(SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/include/test.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/test.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/test.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/V2XMessage.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/IEEE1609Dot2Data.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/IEEE1609Dot2Content.hpp)

set(LIB_NAME v2xmessage)

add_library(${LIB_NAME} ${SOURCE_FILES})

enable_testing()
add_subdirectory(test)