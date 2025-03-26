/**
 * 转换单个图片到SVG
 */
const { convertToSvg } = require('../index');
const fs = require('fs-extra');
const path = require('path');

// 确保目录存在
fs.ensureDirSync(path.join(__dirname, '../images'));
fs.ensureDirSync(path.join(__dirname, '../output'));

async function convertSingleImage() {
  const inputPath = path.join(__dirname, '../images/sample.png');
  const outputPath = path.join(__dirname, '../output/sample.svg');

  // 检查输入文件是否存在
  if (!fs.existsSync(inputPath)) {
    console.log('\n警告: 示例图片不存在!');
    return;
  }
  
  try {
    // 转换参数
    const options = {
      threshold: 128,       // 阈值（0-255）
      turdSize: 2,          // 忽略小于此尺寸的区域
      optCurve: true,       // 优化曲线
      color: '#000000'      // 输出SVG的颜色
    };
    
    // 执行转换
    const result = await convertToSvg(inputPath, outputPath, options);
    console.log('\n✅ 转换成功!');
    console.log(`输入文件: ${inputPath}`);
    console.log(`输出文件: ${outputPath}`);
  } catch (error) {
    console.error('\n❌ 转换失败:', error);
  }
}

// 如果直接运行此文件
if (require.main === module) {
  convertSingleImage().then(() => {
    console.log('\n转换过程完成');
  });
}

module.exports = convertSingleImage; 