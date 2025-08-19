#!/bin/bash




# 设置Git仓库的目录
REPO_DIR=$(pwd)

# 进入Git仓库目录
cd "$REPO_DIR"

# 检查是否有文件变动（不包括未跟踪的文件）
if git diff-index --quiet HEAD --; then
    echo "没有变动，无需提交。"
else
    combined_prefix1=""
    tmp_file=$(mktemp)

    #检查主库本地是否有修改
    git ls-files --modified | grep -Ev '(example/P2UserCalibSync/data/local_preview_2nd.bmp|example/P2UserCalibSync/data/local_correct.png)' | while IFS= read -r line; do
        prefix=$(echo $line | cut -d'/' -f1)

        if [ "$prefix" == "modules" ]; then
        echo "The $prefix is 'modules'."
        else
        echo "The $prefix is not 'modules'."
        basename=$(basename "$line")
        printf "更新%s、" "$basename" >> "$tmp_file"
        # 添加变动文件到暂存区
        git add $line
        fi
    done

    combined_prefix1=$(<"$tmp_file")
    combined_prefix1="${combined_prefix1%、}"

    if [[ $combined_prefix1 != "" ]]; then
        commit_msg="feat: $combined_prefix1"
        echo "Commit message: $commit_msg"
        # 提交更新
        git commit -m "$commit_msg"
        # 推送到远程仓库
        git push 
    fi
    
    rm "$tmp_file"

    #检查子库是否更新，收集所有更新的模块
    updated_modules=()
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            updated_modules+=("$line")
        fi
    done <<< "$(git submodule status | grep "+" | cut -d'/' -f2- | awk '{print $1}')"

    # 批量处理所有更新的子模块
    if [[ ${#updated_modules[@]} -gt 0 ]]; then
        module_names=""
        for module in "${updated_modules[@]}"; do
            git add "modules/$module"
            if [[ -z "$module_names" ]]; then
                module_names="$module"
            else
                module_names="$module_names、$module"
            fi
        done
        
        commit_msg="feat: 更新${module_names}模块"
        echo "Commit message: $commit_msg"
        
        # 一次性提交所有子模块更新
        git commit -m "$commit_msg"
        # 推送到远程仓库
        git push
    fi

fi