#include <iostream>
#include <string>

// 定义一个命名空间
namespace TextProcessing {
    // 在命名空间内定义一个类
    class TextFormatter {
    private:
        std::string text;
        bool isBold;
        bool isItalic;
        
    public:
        // 构造函数
        TextFormatter(const std::string& inputText) 
            : text(inputText), isBold(false), isItalic(false) {}
        
        // 设置文本为粗体
        void setBold(bool bold) {
            isBold = bold;
        }
        
        // 设置文本为斜体
        void setItalic(bool italic) {
            isItalic = italic;
        }
        
        // 格式化文本并返回
        std::string format() const {
            std::string result = text;
            
            if (isBold) {
                result = "**" + result + "**";
            }
            
            if (isItalic) {
                result = "_" + result + "_";
            }
            
            return result;
        }
    };
    
    // 在命名空间内定义一个函数
    std::string processText(const std::string& input, bool makeBold, bool makeItalic) {
        TextFormatter formatter(input);
        formatter.setBold(makeBold);
        formatter.setItalic(makeItalic);
        return formatter.format();
    }
}

// 使用命名空间的示例函数
void demonstrateNamespace() {
    std::string input = "Hello, World!";
    
    // 使用完全限定名称
    std::string result1 = TextProcessing::processText(input, true, false);
    std::cout << "使用粗体格式: " << result1 << std::endl;
    
    // 使用using声明
    using TextProcessing::TextFormatter;
    TextFormatter formatter(input);
    formatter.setItalic(true);
    std::string result2 = formatter.format();
    std::cout << "使用斜体格式: " << result2 << std::endl;
    
    // 使用using namespace指令
    using namespace TextProcessing;
    std::string result3 = processText(input, true, true);
    std::cout << "使用粗体和斜体格式: " << result3 << std::endl;
}
