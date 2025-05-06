# 构建说明

本项目使用CMake构建系统来编译和链接C++代码。

## 前提条件

- CMake（版本 >= 3.10）
- C++编译器（支持C++17标准）
- Git（用于获取子模块）

## 构建步骤

1. 确保已克隆所有子模块：

```bash
git submodule update --init --recursive
```

2. 创建并进入构建目录：

```bash
mkdir build
cd build
```

3. 配置CMake项目：

```bash
cmake ..
```

4. 编译项目：

```bash
cmake --build .
```

## 运行程序

构建完成后，可执行文件将位于`build/bin`目录中。程序需要从`bin`目录运行，以便正确找到配置文件：

```bash
cd bin
```

### 可执行文件

- 运行OpenCC测试程序：

```bash
./opencctest
```

- 运行简单测试程序：

```bash
./simple_test
```

- 运行主程序：

```bash
./main
```

- 运行应用程序（使用TextProcessor类）：

```bash
./app
```

### 注意事项

1. 所有程序都需要从`bin`目录运行，因为它们依赖于`config`目录中的配置文件
2. 如果遇到"file not found"错误，请确保您在正确的目录中运行程序

## 项目结构

- `src/` - 包含项目所有源代码
  - `opencctest.cpp` - OpenCC库的测试代码
  - `test.cpp` - 简单的C++测试代码
  - `main.cpp` - 简单的OpenCC示例程序
  - `app.cpp` - 使用TextProcessor的应用程序
  - `TextProcessor.hpp` - 文本处理器类定义
  - `TextProcessor.cpp` - 文本处理器类实现
  - `config/` - 包含OpenCC的配置文件
- `modules/` - 包含子模块
  - `opencc/` - OpenCC库
- `CMakeLists.txt` - CMake构建配置文件 