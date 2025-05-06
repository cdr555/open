#!/bin/bash

echo_msg() {
    echo "[信息] $1"
}

# 设置Git仓库的目录
REPO_DIR=$(pwd)
echo_msg "当前仓库目录: $REPO_DIR"

# 进入Git仓库目录
cd "$REPO_DIR"

# 检查是否有更改需要提交，包括未跟踪文件和子模块更改
git_status=$(git status --porcelain)
if [ -z "$git_status" ]; then
    echo_msg "检查子模块是否有更新..."
    submodule_changes=$(git submodule status | grep "^+")
    if [ -z "$submodule_changes" ]; then
        echo_msg "没有变动，无需提交。"
        exit 0
    fi
fi

# 处理主仓库的更改
process_main_repo() {
    echo_msg "处理主仓库更改..."
    
    # 忽略某些文件的更改
    tmp_file=$(mktemp)
    combined_prefix=""
    
    # 获取修改的文件列表(排除指定的文件)
    git ls-files --modified --others --exclude-standard | grep -Ev '(example/P2UserCalibSync/data/local_preview_2nd.bmp|example/P2UserCalibSync/data/local_correct.png)' | while IFS= read -r line; do
        prefix=$(echo $line | cut -d'/' -f1)
        
        # 跳过modules目录下的文件，这些会在子模块部分处理
        if [ "$prefix" == "modules" ]; then
            echo_msg "跳过模块文件: $line"
        else
            basename=$(basename "$line")
            # 追加到临时文件，用于构建提交消息
            printf "更新%s、" "$basename" >> "$tmp_file"
            
            # 添加变动文件到暂存区
            git add "$line"
            echo_msg "添加文件: $line"
        fi
    done
    
    # 读取临时文件内容构建提交消息
    if [ -f "$tmp_file" ]; then
        combined_prefix=$(<"$tmp_file")
        combined_prefix="${combined_prefix%、}" # 移除末尾的顿号
        
        if [ -n "$combined_prefix" ]; then
            commit_msg="feat: $combined_prefix"
            echo_msg "主仓库提交信息: $commit_msg"
            
            # 提交更新
            git commit -m "$commit_msg"
            
            # 推送到远程仓库
            if git push; then
                echo_msg "主仓库更新已推送到远程"
            else
                echo_msg "推送主仓库失败"
            fi
        else
            echo_msg "主仓库无需提交修改文件"
        fi
        
        rm "$tmp_file"
    fi
}

# 处理子模块的更改
process_submodules() {
    echo_msg "处理子模块更改..."
    
    # 检查子模块状态，查找有更新的子模块
    git submodule status | grep "^+" | cut -d'/' -f2- | awk '{print $1}' | while IFS= read -r module; do
        echo_msg "处理子模块: $module"
        
        tmp_file=$(mktemp)
        printf "更新%s模块" "$module" >> "$tmp_file"
        
        combined_prefix=$(<"$tmp_file")
        
        if [ -n "$combined_prefix" ]; then
            commit_msg="feat: $combined_prefix"
            echo_msg "子模块提交信息: $commit_msg"
            
            # 添加变动到暂存区
            git add "modules/$module"
            
            # 提交更新
            git commit -m "$commit_msg"
            
            # 推送到远程仓库
            if git push; then
                echo_msg "子模块 $module 更新已推送到远程"
            else
                echo_msg "推送子模块 $module 失败"
            fi
        fi
        
        rm "$tmp_file"
    done
}

# 执行自动提交流程
auto_commit() {
    echo_msg "开始自动提交流程..."
    
    # 首先处理主仓库
    process_main_repo
    
    # 然后处理子模块
    process_submodules
    
    echo_msg "自动提交完成"
}

# 执行自动提交
auto_commit