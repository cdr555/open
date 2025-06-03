#!/bin/bash

# Git自动提交推送脚本
# 使用方法: ./commit-push.sh

echo "=== Git 自动提交推送脚本 ==="
echo

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "❌ 错误: 当前目录不是Git仓库"
    exit 1
fi

# 显示当前仓库状态
echo "📊 当前仓库状态:"
git status --short

echo
echo "📋 详细状态:"
git status

echo
echo "================================"

# 提示用户输入提交信息
echo "请输入提交信息:"
read -p "💬 提交信息: " commit_message

# 检查提交信息是否为空
if [ -z "$commit_message" ]; then
    echo "❌ 提交信息不能为空！"
    exit 1
fi

echo
echo "🔄 开始执行提交流程..."

# 添加所有更改到暂存区
echo "📦 添加文件到暂存区..."
if git add .; then
    echo "✅ 文件添加成功"
else
    echo "❌ 文件添加失败"
    exit 1
fi

# 提交更改
echo "💾 提交更改..."
if git commit -m "$commit_message"; then
    echo "✅ 提交成功"
else
    echo "❌ 提交失败"
    exit 1
fi

# 推送到远程仓库
echo "🚀 推送到远程仓库..."
if git push; then
    echo "✅ 推送成功！"
    echo
    echo "🎉 所有操作完成！"
    echo "📝 提交信息: $commit_message"
else
    echo "❌ 推送失败"
    echo "💡 提示: 请检查网络连接或远程仓库权限"
    exit 1
fi

echo
echo "=== 脚本执行完毕 ===" 