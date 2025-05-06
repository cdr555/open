#include "../modules/opencc/src/SimpleConverter.hpp"
#include <iostream>
#include <string>

int main() {
    try {
        // 指定配置文件路径
        std::string config_path = "config/s2t.json";
        
        // 创建简体到繁体转换器
        opencc::SimpleConverter converter(config_path);
        
        // 要转换的文本
        std::string input = "简体中文";
        
        // 进行转换
        std::string converted = converter.Convert(input);
        
        // 输出结果
        std::cout << "原文: " << input << std::endl;
        std::cout << "转换结果: " << converted << std::endl;
        
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "错误: " << e.what() << std::endl;
        return 1;
    }
} 