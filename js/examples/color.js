/**
 * 转换彩色图片到SVG
 */
const { convertColorImageToSvg } = require('../index');
const fs = require('fs-extra');
const path = require('path');

// 确保目录存在
fs.ensureDirSync(path.join(__dirname, '../images'));
fs.ensureDirSync(path.join(__dirname, '../output'));

/**
 * 转换彩色图片示例
 */
async function convertColorImage() {
  const inputPath = path.join(__dirname, '../images/color-sample.jpg');
  const outputPath = path.join(__dirname, '../output/color-sample.svg');

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
    
    // 执行转换
    const result = await convertColorImageToSvg(inputPath, outputPath, options);
    console.log('\n✅ 彩色图片转换成功!');
    console.log(`输入文件: ${inputPath}`);
    console.log(`输出文件: ${outputPath}`);
  } catch (error) {
    console.error('\n❌ 转换失败:', error);
  }
}

// 如果直接运行此文件
if (require.main === module) {
  convertColorImage().then(() => {
    console.log('\n彩色图片转换过程完成');
  });
}

module.exports = convertColorImage; 