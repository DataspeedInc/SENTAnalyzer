cmake_minimum_required (VERSION 3.11)
project(SENT_analyzer)

# custom CMake Modules are located in the cmake directory.
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

include(ExternalAnalyzerSDK)

set(SOURCES
src/SENTAnalyzer.cpp
src/SENTAnalyzer.h
src/SENTAnalyzerResults.cpp
src/SENTAnalyzerResults.h
src/SENTAnalyzerSettings.cpp
src/SENTAnalyzerSettings.h
src/SENTSimulationDataGenerator.cpp
src/SENTSimulationDataGenerator.h
)

# if(GENERATION_TOOLS MATCHES "True")
#     add_definitions(-DGENERATION_TOOLS)
# else()
#     remove_definitions(-DGENERATION_TOOLS)
# endif()

if(GENERATION_TOOLS STREQUAL "True")
    set(GENERATION_TOOLS False)
    message(STATUS "-- Compiling with Generation Tools! --")
    add_definitions(-DGENERATION_TOOLS)
else()
    message(STATUS "-- Compiling without Generation Tools! --")
    remove_definitions(-DGENERATION_TOOLS)
endif()

add_analyzer_plugin(SENT_analyzer SOURCES ${SOURCES})