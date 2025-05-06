#include "TextProcessor.hpp"
#include <iostream>
#include <vector>

int main() {
    try {
        // 配置文件路径
        std::string configPath = "config/s2t.json";
        
        // 创建文本处理器
        TextProcessor processor(configPath);
        
        // 单个文本转换
        std::string singleText = "简体中文测试";
        std::string converted = processor.convertText(singleText);
        std::cout << "单个文本转换：" << std::endl;
        std::cout << "  原文: " << singleText << std::endl;
        std::cout << "  结果: " << converted << std::endl;
        
        // 批量文本转换
        std::vector<std::string> batchTexts;
        batchTexts.push_back("中国");
        batchTexts.push_back("北京");
        batchTexts.push_back("上海");
        batchTexts.push_back("广州");
        batchTexts.push_back("深圳");
        
        std::cout << "\n批量文本转换：" << std::endl;
        std::vector<std::string> batchResults = processor.convertBatch(batchTexts);
        
        for (size_t i = 0; i < batchTexts.size(); ++i) {
            std::cout << "  原文: " << batchTexts[i] << " -> 结果: " << batchResults[i] << std::endl;
        }
        
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "错误: " << e.what() << std::endl;
        return 1;
    }
} 