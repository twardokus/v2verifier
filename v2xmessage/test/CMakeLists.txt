set(IEEE1609DOT2DATA_TEST_SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/IEEE1609Dot2Data_TEST.cpp)

set(IEEE1609DOT2CONTENT_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/IEEE1609Dot2Content_TEST.cpp)

set(HEADERINFO_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/HeaderInfo_TEST.cpp)

set(ECCCURVEPOINT_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/EccP256CurvePoint_TEST.cpp)

add_executable(ieee16092data_test ${IEEE1609DOT2DATA_TEST_SOURCE_FILES} ${SOURCE_FILES})
add_executable(ieee1609Dot2Content_test ${IEEE1609DOT2CONTENT_TEST_SOURCE_FILES} ${SOURCE_FILES})
add_executable(headerInfo_test ${HEADERINFO_TEST_SOURCE_FILES} ${SOURCE_FILES})
add_executable(eccCurvePointTest ${ECCCURVEPOINT_TEST_SOURCE_FILES} ${SOURCE_FILES})

add_test(
        NAME ieee16092data_test
        COMMAND $<TARGET_FILE:ieee16092data_test>
)

add_test(
        NAME ieee1609Dot2Content_test
        COMMAND $<TARGET_FILE:ieee1609Dot2Content_test>
)

add_test(
        NAME headerInfo_test
        COMMAND $<TARGET_FILE:headerInfo_test>
)

add_test(
        NAME eccCurvePoint_test
        COMMAND $<TARGET_FILE:eccCurvePointTest>
)