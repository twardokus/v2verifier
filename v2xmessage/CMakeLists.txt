set(SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/include/V2XMessage.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/IEEE1609Dot2Content.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/IEEE1609Dot2Data.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/SignedData.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/IEEE1609Dot2DataTypes.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/ToBeSignedData.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/SignedDataPayload.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/UnsecuredData.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/HeaderInfo.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/SignerIdentifier.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/Signature.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/Utility.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/EcdsaP256Signature.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/include/EccP256CurvePoint.hpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/V2XMessage.cpp
)

set(LIB_NAME v2xmessage)

add_library(${LIB_NAME} ${SOURCE_FILES})

enable_testing()
add_subdirectory(test)