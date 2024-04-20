set(SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/Log.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/Log.h
)

set(LIB_NAME logger)

add_library(${LIB_NAME} ${SOURCE_FILES})

#enable_testing()