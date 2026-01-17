#!/usr/bin/env bash
set -euo pipefail

# 目标：
# 1) 在每个一级子模块里：如果其内部子模块（第二层）指针有更新（git submodule status 行首为 +），
#    则把这些 gitlink 指针更新提交到该一级子模块的 origin/main，并 push。
# 2) 回到根仓库：把一级子模块指针更新提交到根仓库的 origin/main，并 push。
#
# 约束/假设（来自你的需求）：
# - 根仓库默认分支：main
# - 一级子模块允许直接 push 到 main
# - 子模块中的子模块（第二层）工作区一定是干净的：我们不进入第二层提交任何代码，只提交指针更新

ROOT_REMOTE="origin"
ROOT_BRANCH="main"
SUB_REMOTE="origin"
SUB_BRANCH="main"

INIT_SUBMODULES=1

msg_join_cn() {
  # 用 '、' 拼接数组
  local out=""
  for s in "$@"; do
    if [[ -z "$out" ]]; then
      out="$s"
    else
      out="${out}、${s}"
    fi
  done
  printf "%s" "$out"
}

info() { echo "[INFO] $*"; }
warn() { echo "[WARN] $*" >&2; }
die() { echo "[ERROR] $*" >&2; exit 1; }

cleanup_git_lock_if_any() {
  local dir="$1"
  # 注意：子模块的 .git 往往是一个“gitdir 指针文件”，index.lock 实际在 gitdir 下。
  # 使用 git rev-parse --git-path 可正确解析真实路径。
  local lock_path=""
  lock_path="$(git -C "$dir" rev-parse --git-path index.lock 2>/dev/null || true)"
  if [[ -n "$lock_path" && -f "$dir/$lock_path" ]]; then
    warn "发现并清理 $dir/$lock_path"
    rm -f "$dir/$lock_path"
  fi
}

ensure_git_repo() {
  local dir="$1"
  git -C "$dir" rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "不是 git 仓库：$dir"
}

checkout_main_or_die() {
  local dir="$1"
  local remote="$2"
  local branch="$3"

  ensure_git_repo "$dir"
  cleanup_git_lock_if_any "$dir"

  git -C "$dir" fetch "$remote" "$branch" >/dev/null 2>&1 || true

  if git -C "$dir" show-ref --verify --quiet "refs/heads/$branch"; then
    git -C "$dir" checkout "$branch" >/dev/null 2>&1
  else
    git -C "$dir" checkout -b "$branch" "$remote/$branch" >/dev/null 2>&1 \
      || die "无法在 $dir 切到 $remote/$branch（远端分支可能不存在或无权限）"
  fi

  local cur
  cur="$(git -C "$dir" rev-parse --abbrev-ref HEAD)"
  [[ "$cur" != "HEAD" ]] || die "$dir 仍处于 detached HEAD，已终止以避免误操作"
}

list_top_level_submodules() {
  # 读取根仓库 .gitmodules 的 path 列表
  git config -f .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null | awk '{print $2}'
}

list_bumped_submodules_in_repo() {
  # 在某个父仓库内，列出“指针前进”的子模块路径（git submodule status 行首为 +）
  local dir="$1"
  ensure_git_repo "$dir"
  git -C "$dir" submodule status 2>/dev/null | awk '$1 ~ /^\+/ {print $2}'
}

ensure_worktree_clean_or_die() {
  # 防止把意外改动带进“指针更新提交”
  local dir="$1"
  ensure_git_repo "$dir"

  if [[ -n "$(git -C "$dir" status --porcelain)" ]]; then
    die "$dir 工作区不干净（存在未提交/未暂存改动）。请先处理后再运行脚本。"
  fi
}

commit_and_push_if_staged() {
  local dir="$1"
  local remote="$2"
  local branch="$3"
  local msg="$4"

  ensure_git_repo "$dir"

  if git -C "$dir" diff --cached --quiet; then
    info "$dir 没有 staged 变更，跳过提交"
    return 0
  fi

  git -C "$dir" commit -m "$msg"
  git -C "$dir" push "$remote" "$branch"
}

main() {
  local root
  root="$(git rev-parse --show-toplevel 2>/dev/null)" || die "当前目录不在 git 仓库内"
  cd "$root"

  info "根仓库：$root"

  if [[ "$INIT_SUBMODULES" == "1" ]]; then
    info "初始化/更新子模块（递归）"
    git submodule update --init --recursive
  fi

  # 1) 先处理一级子模块：提交其内部子模块（第二层）的指针更新
  local top_subs=()
  while IFS= read -r p; do
    [[ -n "$p" ]] && top_subs+=("$p")
  done < <(list_top_level_submodules)

  if [[ "${#top_subs[@]}" -eq 0 ]]; then
    warn "根仓库 .gitmodules 未发现一级子模块，直接进入根仓库更新步骤"
  fi

  for sm in "${top_subs[@]}"; do
    info "处理一级子模块：$sm"

    ensure_git_repo "$root/$sm"
    checkout_main_or_die "$root/$sm" "$SUB_REMOTE" "$SUB_BRANCH"

    # 需求假设：二级子模块工作区干净；但一级子模块本身也应干净（否则不清楚你想不想提交它的代码改动）
    ensure_worktree_clean_or_die "$root/$sm"

    local nested_bumped=()
    while IFS= read -r np; do
      [[ -n "$np" ]] && nested_bumped+=("$np")
    done < <(list_bumped_submodules_in_repo "$root/$sm")

    if [[ "${#nested_bumped[@]}" -eq 0 ]]; then
      info "$sm：未发现二级子模块指针更新（+），跳过"
      continue
    fi

    # 只 add 二级子模块路径（gitlink 指针更新）
    for np in "${nested_bumped[@]}"; do
      git -C "$root/$sm" add "$np"
    done

    local joined_nested
    joined_nested="$(msg_join_cn "${nested_bumped[@]}")"
    local msg_sub
    msg_sub="chore(submodule): 更新二级子模块指针：${joined_nested}"
    info "$sm：提交并推送 -> $SUB_REMOTE/$SUB_BRANCH"
    commit_and_push_if_staged "$root/$sm" "$SUB_REMOTE" "$SUB_BRANCH" "$msg_sub"
  done

  # 2) 回到根仓库：提交一级子模块指针更新
  checkout_main_or_die "$root" "$ROOT_REMOTE" "$ROOT_BRANCH"

  # 根仓库允许有自己的文件改动，但本脚本只自动提交“一级子模块指针更新”
  local bumped_top=()
  while IFS= read -r p; do
    [[ -n "$p" ]] && bumped_top+=("$p")
  done < <(list_bumped_submodules_in_repo "$root")

  if [[ "${#bumped_top[@]}" -eq 0 ]]; then
    info "根仓库未发现一级子模块指针更新（+）。如果你只是更新了二级子模块指针，说明未产生新的一级子模块提交。"
    exit 0
  fi

  for p in "${bumped_top[@]}"; do
    git add "$p"
  done

  local joined_top
  joined_top="$(msg_join_cn "${bumped_top[@]}")"
  local msg_root
  msg_root="chore(submodule): 更新一级子模块指针：${joined_top}"

  info "根仓库：提交并推送 -> $ROOT_REMOTE/$ROOT_BRANCH"
  commit_and_push_if_staged "$root" "$ROOT_REMOTE" "$ROOT_BRANCH" "$msg_root"

  info "完成"
}

main "$@"