#include "TextProcessor.hpp"

TextProcessor::TextProcessor(const std::string& configPath) {
    converter = new opencc::SimpleConverter(configPath);
}

TextProcessor::~TextProcessor() {
    if (converter) {
        delete converter;
        converter = nullptr;
    }
}

std::string TextProcessor::convertText(const std::string& text) {
    return converter->Convert(text);
}

std::vector<std::string> TextProcessor::convertBatch(const std::vector<std::string>& texts) {
    std::vector<std::string> results;
    results.reserve(texts.size());
    
    for (const auto& text : texts) {
        results.push_back(converter->Convert(text));
    }
    
    return results;
}