set(TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/test_test.cpp)

add_executable(test_test ${TEST_SOURCE_FILES} ${SOURCE_FILES})

add_test(
    NAME test_test
    COMMAND $<TARGET_FILE:test_test>
)