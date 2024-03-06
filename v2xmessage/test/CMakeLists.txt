set(TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/IEEE16092Data_TEST.cpp)

add_executable(ieee16092data_test ${TEST_SOURCE_FILES} ${SOURCE_FILES})

add_test(
        NAME ieee16092data_test
        COMMAND $<TARGET_FILE:ieee16092data_test>
)