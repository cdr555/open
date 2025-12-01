#!/bin/bash
set -euo pipefail

# 设置Git仓库的目录
REPO_DIR=$(pwd)

# 进入Git仓库目录
cd "$REPO_DIR"


git submodule update --init --recursive
# 递归遍历所有 submodule（子仓库中的子仓库也会一起遍历）
git submodule foreach --recursive '
  echo "进入子模块: $name ($path)"

  # 清理子模块可能存在的 git lock 文件
  if [ -f ".git/index.lock" ]; then
      echo "  清理子模块 git index.lock 文件..."
      rm -f .git/index.lock
  fi

  # 同步远端并确定分支
  git fetch --all --tags --prune || true

  current_branch=$(git symbolic-ref --short -q HEAD || true)
  if [ -z "$current_branch" ]; then
      # detached HEAD，优先用 origin 的默认分支
      default_branch=$(git remote show origin 2>/dev/null | sed -n '"'"'/HEAD branch/s/.*: //p'"'"')
      if [ -z "$default_branch" ]; then
          if git show-ref --verify --quiet refs/heads/main; then
              default_branch=main
          elif git show-ref --verify --quiet refs/heads/master; then
              default_branch=master
          else
              echo "  找不到可用分支，跳过该子模块"
              exit 0
          fi
      fi
      echo "  当前为 detached HEAD，切换到 $default_branch 分支"
      git checkout "$default_branch"
  else
      echo "  当前分支为 $current_branch"
  fi

  # 同步远端分支
  git pull --ff-only || git pull --rebase || true

  # 确保子模块的子模块也被初始化
  git submodule update --init --recursive
 
  # 先将所有变更（含未跟踪）加入暂存区
  git add -A
 
  # 将下一级子模块指针变更也加入暂存区（+ 改变、U 冲突、- 未初始化）
  changed_sub=$(git submodule status | awk '"'"'/^[+U-]/ {print $2}'"'"')
  if [ -n "$changed_sub" ]; then
    while IFS= read -r m; do
      [ -z "$m" ] && continue
      git add "$m"
    done <<< "$changed_sub"
  fi
 
  # 若暂存区有内容则提交并推送
  if ! git diff --cached --quiet; then
      echo "  子模块有变动，开始自动提交..."
      msg="chore(auto-commit): 更新子模块 $name"
      echo "  提交信息: $msg"
      if git commit -m "$msg"; then
          git push || echo "  push 失败，请手动处理"
      fi
  else
      echo "  子模块无变动，跳过"
  fi
'

# 二次遍历：在子子模块更新/推送完成后，再次检查各级父子模块是否有“子模块指针变化”并提交推送
git submodule foreach --recursive '
  echo "二次提交检查: $name ($path)"
  # 将可能遗漏的变更纳入暂存区
  git add -A
  changed_sub=$(git submodule status | awk '"'"'/^[+U-]/ {print $2}'"'"')
  if [ -n "$changed_sub" ]; then
    while IFS= read -r m; do
      [ -z "$m" ] && continue
      git add "$m"
    done <<< "$changed_sub"
  fi
  if ! git diff --cached --quiet; then
    msg="chore(auto-commit): 同步子模块指针 $name"
    echo "  提交信息: $msg"
    git commit -m "$msg" && git push || true
  else
    echo "  无需二次提交"
  fi
'

# 检查是否有文件变动（不包括未跟踪的文件）
if git diff-index --quiet HEAD --; then
    echo "没有变动，无需提交。"
else
    combined_prefix1=""
    tmp_file=$(mktemp)

    #检查主库本地是否有修改（排除 modules 下的子模块路径，按你原逻辑收集文件名）
        git ls-files --modified | grep -Ev '(example/P2UserCalibSync/data/local_preview_2nd.bmp|example/P2UserCalibSync/data/local_correct.png)' | while IFS= read -r line; do
        prefix=$(echo "$line" | cut -d'/' -f1)

        if [ "$prefix" == "modules" ]; then
        echo "The $prefix is '"'"'modules'"'"'."
        else
        echo "The $prefix is not '"'"'modules'"'"'."
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
        git commit -m "$commit_msg" || true
        # 推送到远程仓库
        git push || true
    fi
    
    rm "$tmp_file"

    # 检查顶层 submodule 指针是否变化（包含因为“子仓库中的子仓库”更新而导致的父级指针变化）
    # 符号含义：+ 工作树HEAD与记录的commit不同；U 冲突；- 未初始化
    changed_modules=$(git submodule status | awk '/^[+U-]/ {print $2}')
    if [[ -n "${changed_modules}" ]]; then
        module_names=""
        while IFS= read -r module; do
            [[ -z "$module" ]] && continue
            git add "$module"
            if [[ -z "$module_names" ]]; then
                module_names="$module"
            else
                module_names="$module_names、$module"
            fi
        done <<< "$changed_modules"

        if [[ -n "$module_names" ]]; then
            commit_msg="feat: 更新${module_names}模块"
            echo "Commit message: $commit_msg"
            git commit -m "$commit_msg" || true
            git push || true
        fi
    fi
fi