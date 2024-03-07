set(IEEE1609DOT2DATA_TEST_SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/IEEE1609Dot2Data_TEST.cpp)

set(IEEE1609DOT2CONTENT_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/IEEE1609Dot2Content_TEST.cpp)

set(HEADERINFO_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/HeaderInfo_TEST.cpp)

set(ECCCURVEPOINT_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/EccP256CurvePoint_TEST.cpp)

set(SIGNERIDENTIFIER_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/SignerIdentifier_TEST.cpp)

set(TOBESIGNEDDATA_TEST_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/ToBeSignedData_TEST.cpp)

add_executable(ieee16092data_test           ${IEEE1609DOT2DATA_TEST_SOURCE_FILES}       ${SOURCE_FILES})
add_executable(ieee1609Dot2Content_test     ${IEEE1609DOT2CONTENT_TEST_SOURCE_FILES}    ${SOURCE_FILES})
add_executable(headerInfo_test              ${HEADERINFO_TEST_SOURCE_FILES}             ${SOURCE_FILES})
add_executable(eccCurvePoint_test           ${ECCCURVEPOINT_TEST_SOURCE_FILES}          ${SOURCE_FILES})
add_executable(signerIdentifier_test        ${SIGNERIDENTIFIER_TEST_SOURCE_FILES}       ${SOURCE_FILES})
add_executable(toBeSignedData_test          ${TOBESIGNEDDATA_TEST_SOURCE_FILES}         ${SOURCE_FILES})

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
        COMMAND $<TARGET_FILE:eccCurvePoint_test>
)

add_test(
        NAME signerIdentifier_test
        COMMAND $<TARGET_FILE:signerIdentifier_test>
)

add_test(
        NAME toBeSignedData_test
        COMMAND $<TARGET_FILE:toBeSignedData_test>
)