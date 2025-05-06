#pragma once

#include <string>
#include <vector>
#include "../modules/opencc/src/SimpleConverter.hpp"

class TextProcessor {
public:
    TextProcessor(const std::string& configPath);
    ~TextProcessor();
    
    // 转换单个文本
    std::string convertText(const std::string& text);
    
    // 批量转换文本
    std::vector<std::string> convertBatch(const std::vector<std::string>& texts);
    
private:
    opencc::SimpleConverter* converter;
}; 