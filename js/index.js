/**
 * 位图转矢量图工具 - 精简版
 * 使用potrace库实现位图到SVG的转换
 */

const potrace = require('potrace');
const Jimp = require('jimp');
const fs = require('fs-extra');
const path = require('path');

/**
 * 将单个位图转换为SVG
 */
async function convertToSvg(inputPath, outputPath, options = {}) {
  // 默认选项
  const defaultOptions = {
    threshold: 128,       // 阈值，用于将图像转换为黑白
    turdSize: 2,          // 忽略小于此尺寸的区域
    optCurve: true,       // 优化曲线
    color: '#000000'      // 输出SVG的颜色
  };

  // 合并选项
  const opts = { ...defaultOptions, ...options };
  
  // 确保输出目录存在
  fs.ensureDirSync(path.dirname(outputPath));

  return new Promise((resolve, reject) => {
    potrace.trace(inputPath, opts, (err, svg) => {
      if (err) return reject(err);
      fs.writeFileSync(outputPath, svg);
      resolve({ inputPath, outputPath, svg });
    });
  });
}

/**
 * 将彩色图像转换为SVG
 */
async function convertColorImageToSvg(inputPath, outputPath, options = {}) {
  try {
    // 确保输出目录存在
    fs.ensureDirSync(path.dirname(outputPath));

    // 读取图片并转换为灰度
    const image = await Jimp.read(inputPath);
    image.grayscale();
    
    // 临时文件路径
    const tempFile = path.join(path.dirname(outputPath), `_temp_${Date.now()}.png`);
    
    try {
      // 保存为临时文件
      await new Promise((resolve, reject) => {
        image.write(tempFile, err => err ? reject(err) : resolve());
      });
      
      // 转换为SVG
      const result = await convertToSvg(tempFile, outputPath, options);
      return result;
    } finally {
      // 清理临时文件
      if (fs.existsSync(tempFile)) {
        fs.removeSync(tempFile);
      }
    }
  } catch (error) {
    throw error;
  }
}

/**
 * 批量转换文件夹中的所有位图
 */
async function batchConvert(inputDir, outputDir, options = {}, extensions = ['.png', '.jpg', '.jpeg']) {
  // 确保输出目录存在
  fs.ensureDirSync(outputDir);

  // 获取所有图片文件
  const files = fs.readdirSync(inputDir)
    .filter(file => extensions.includes(path.extname(file).toLowerCase()));

  if (files.length === 0) {
    return { 
      success: false, 
      message: '没有找到符合条件的图片文件', 
      results: [] 
    };
  }

  try {
    // 转换所有文件
    const results = await Promise.all(files.map(async file => {
      try {
        const inputPath = path.join(inputDir, file);
        const outputPath = path.join(outputDir, `${path.basename(file, path.extname(file))}.svg`);
        return await convertToSvg(inputPath, outputPath, options);
      } catch (err) {
        return { 
          inputPath: path.join(inputDir, file), 
          error: err.message || err 
        };
      }
    }));

    return {
      success: true,
      message: `成功转换 ${results.filter(r => !r.error).length} 个文件，失败 ${results.filter(r => r.error).length} 个文件`,
      results
    };
  } catch (error) {
    return {
      success: false,
      message: error.message || '批量转换失败',
      error
    };
  }
}

// 导出所有可用方法
module.exports = { convertToSvg, convertColorImageToSvg, batchConvert }; 