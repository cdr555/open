const { batchConvert: batchConvertImages } = require('../index');
const fs = require('fs-extra');
const path = require('path');

// 确保目录存在
fs.ensureDirSync(path.join(__dirname, '../images'));
fs.ensureDirSync(path.join(__dirname, '../output'));

async function batchProcess() {
  const inputPath = path.join(__dirname, '../images');
  const outputPath = path.join(__dirname, '../output');

  // 检查输入文件是否存在
  if (!fs.existsSync(inputPath)) {
    console.log('\n警告: 示例图片不存在!');
    return;
  }
  
  try {
    // 转换参数
    const options = {
      threshold: 150,       // 阈值（0-255）
      turdSize: 2,          // 忽略小于此尺寸的区域
      optCurve: true,       // 优化曲线
      color: '#3498db'      // 输出SVG的颜色
    };
    
    // 批量转换
    const result = await batchConvertImages(inputPath, outputPath, options);
    console.log('\n✅ 批量转换完成!');
    console.log(`输入目录: ${inputPath}`);
    console.log(`输出目录: ${outputPath}`);
    console.log(`${result.message}`);
    
    // 打印成功的文件
    if (result.success && result.results.length > 0) {
      console.log('\n成功转换的文件:');
      result.results.forEach((item, index) => {
        if (!item.error) {
          console.log(`${index + 1}. ${path.basename(item.outputPath)}`);
        }
      });
    }
  } catch (error) {
    console.error('\n❌ 转换失败:', error);
  }
}

// 如果直接运行此文件
if (require.main === module) {
    batchProcess().then(() => {
    console.log('\n批量转换过程完成');
  });
}

module.exports = batchProcess; 