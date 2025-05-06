cmake_minimum_required(VERSION 3.10)
project(OpenCCProject VERSION 1.0)

# 设置C++标准为C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置所有可执行文件输出到同一目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 查找OpenCC库
add_subdirectory(modules/opencc)

# 包含头文件目录
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/modules
    ${CMAKE_CURRENT_SOURCE_DIR}/modules/opencc/src
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# 添加src目录的可执行文件
add_executable(opencctest src/opencctest.cpp)
add_executable(simple_test src/test.cpp)
add_executable(main src/main.cpp)
add_executable(app src/app.cpp src/TextProcessor.cpp)

# 链接OpenCC库
target_link_libraries(opencctest PRIVATE libopencc)
target_link_libraries(main PRIVATE libopencc)
target_link_libraries(app PRIVATE libopencc)

# 配置文件复制到bin目录
file(COPY src/config DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

# 确保我们的可执行文件依赖于OpenCC的词典构建
add_dependencies(opencctest Dictionaries)
add_dependencies(main Dictionaries)
add_dependencies(app Dictionaries)

# 获取OpenCC构建后的配置文件和词典文件路径
set(OPENCC_DICT_DIR "${CMAKE_BINARY_DIR}/modules/opencc/data")
set(OPENCC_CONFIG_DIR "${CMAKE_CURRENT_SOURCE_DIR}/modules/opencc/data/config")

# 复制配置和词典文件（在构建后执行）
add_custom_command(
    TARGET main POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        ${OPENCC_CONFIG_DIR}/s2t.json
        ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/config/
    COMMAND ${CMAKE_COMMAND} -E copy
        ${OPENCC_DICT_DIR}/STCharacters.ocd2
        ${OPENCC_DICT_DIR}/STPhrases.ocd2
        ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/config/
    COMMENT "Copying OpenCC dictionary and config files to bin/config directory"
) 