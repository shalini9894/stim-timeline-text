cmake_minimum_required(VERSION 3.20)
project(stim_timeline_text LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/cpp/vendor/stim/VENDORED_FILE_ALLOWLIST.txt" VENDOR_ALL)
set(VENDOR_SOURCES "")
foreach(rel ${VENDOR_ALL})
  if(rel MATCHES "\\.cc$")
    list(APPEND VENDOR_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/cpp/vendor/stim/${rel}")
  endif()
endforeach()
list(LENGTH VENDOR_SOURCES N_VENDOR)
message(STATUS "Vendored Stim translation units: ${N_VENDOR}")

pybind11_add_module(_native MODULE
  ${VENDOR_SOURCES}
  cpp/tsim_gate_labels.cc
  cpp/render_timeline_text.cc
  cpp/python_module.cc
)
target_include_directories(_native PRIVATE
  "${CMAKE_CURRENT_SOURCE_DIR}/cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/cpp/vendor/stim/src"
)
install(TARGETS _native DESTINATION stim_timeline_text)
