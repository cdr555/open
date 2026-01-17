#!/usr/bin/env bash
set -euo pipefail

# 目标：
# 1) 在每个一级子模块里：如果其内部子模块（第二层）指针有更新（git submodule status 行首为 +），
#    则把这些 gitlink 指针更新提交到该一级子模块的 origin/main，并 push。
# 2) 回到根仓库：把一级子模块指针更新提交到根仓库的 origin/main，并 push。
#
# 约束：
# - 根仓库与一级子模块仓库均使用 origin/main
# - 不做 rebase（只允许 fast-forward）
# - 不允许在一级子模块中提交“非二级子模块指针（gitlink=160000）”的改动

ROOT_REMOTE="origin"
ROOT_BRANCH="main"
SUB_REMOTE="origin"
SUB_BRANCH="main"

# 是否初始化缺失的子模块：
# 0: 不做任何 submodule update（推荐：避免覆盖你本地已前移的子模块指针）
# 1: 仅初始化缺失的子模块（只处理 status 以 '-' 开头的条目，不会重置已初始化子模块的指针）
INIT_SUBMODULES="${INIT_SUBMODULES:-1}"

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

init_missing_submodules_only() {
  local dir="$1"
  ensure_git_repo "$dir"

  local missing=()
  # '-' 表示未初始化的子模块
  while IFS= read -r p; do
    [[ -n "$p" ]] && missing+=("$p")
  done < <(git -C "$dir" submodule status --recursive 2>/dev/null | awk '/^-/{print $2}')

  if [[ "${#missing[@]}" -eq 0 ]]; then
    info "子模块已初始化，跳过 submodule update"
    return 0
  fi

  info "初始化缺失子模块：${missing[*]}"
  git -C "$dir" submodule update --init --recursive "${missing[@]}"
}

checkout_main_or_die() {
  local dir="$1"
  local remote="$2"
  local branch="${3:-}"
  if [[ -z "$branch" ]]; then
    warn "函数 checkout_main_or_die 在 $dir 缺少分支参数，跳过"
    return 1
  fi

  ensure_git_repo "$dir"
  cleanup_git_lock_if_any "$dir"

  git -C "$dir" fetch "$remote" "${branch}" >/dev/null 2>&1 || true

  if git -C "$dir" show-ref --verify --quiet "refs/heads/${branch}"; then
    git -C "$dir" checkout "${branch}" >/dev/null 2>&1
  else
    git -C "$dir" checkout -b "${branch}" "${remote}/${branch}" >/dev/null 2>&1 || {
      warn "无法在 $dir 切到 ${remote}/${branch}（远端分支可能不存在或无权限），跳过"
      return 1
    }
  fi

  local cur
  cur="$(git -C "$dir" rev-parse --abbrev-ref HEAD)"
  if [[ "$cur" == "HEAD" ]]; then
    warn "$dir 仍处于 detached HEAD，跳过"
    return 1
  fi
  return 0
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

ensure_only_submodule_pointer_changes_or_skip() {
  # 仅允许 gitlink（mode 160000）变化；若存在其它文件改动则跳过（不报错）
  local dir="$1"
  ensure_git_repo "$dir"

  local porcelain
  porcelain="$(git -C "$dir" status --porcelain)"
  [[ -n "$porcelain" ]] || return 0

  local ok=1
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local path="${line:3}"

    # 只允许“gitlink（mode 160000）”路径发生变化
    # 例如：' M modules/cylindrical-correction'
    local mode
    mode="$(git -C "$dir" ls-files --stage -- "$path" 2>/dev/null | awk 'NR==1{print $1}' || true)"
    if [[ "$mode" != "160000" ]]; then
      ok=0
      warn "$dir 存在非子模块指针改动：$line"
    fi
  done <<< "$porcelain"

  if [[ "$ok" -ne 1 ]]; then
    warn "$dir 检测到非子模块指针改动，本次跳过自动提交"
    return 1
  fi
  return 0
}

pull_ff_only_or_skip() {
  local dir="$1"
  local remote="$2"
  local branch="$3"
  ensure_git_repo "$dir"
  git -C "$dir" fetch "$remote" "$branch" >/dev/null 2>&1 || true
  if ! git -C "$dir" pull --ff-only "$remote" "$branch" >/dev/null 2>&1; then
    warn "$dir 无法 fast-forward 到 $remote/$branch（按约束不允许 rebase/merge），本次跳过"
    return 1
  fi
  return 0
}

commit_and_push_if_staged() {
  local dir="$1"
  local remote="$2"
  local branch="${3:-}"
  local msg="$4"

  if [[ -z "$branch" ]]; then
    die "函数 commit_and_push_if_staged 在 $dir 缺少分支参数"
  fi

  ensure_git_repo "$dir"

  if git -C "$dir" diff --cached --quiet; then
    info "$dir 没有 staged 变更，跳过提交"
    return 0
  fi

  git -C "$dir" commit -m "$msg"
  git -C "$dir" push "$remote" "${branch}"
}

main() {
  local root
  root="$(git rev-parse --show-toplevel 2>/dev/null)" || die "当前目录不在 git 仓库内"
  cd "$root"

  info "根仓库：$root"

  if [[ "$INIT_SUBMODULES" == "1" ]]; then
    info "仅初始化缺失子模块（不重置已前移的指针）"
    init_missing_submodules_only "$root"
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
    if ! checkout_main_or_die "$root/$sm" "$SUB_REMOTE" "$SUB_BRANCH"; then
      warn "[$sm] checkout 失败，本次跳过"
      continue
    fi
    if ! pull_ff_only_or_skip "$root/$sm" "$SUB_REMOTE" "$SUB_BRANCH"; then
      continue
    fi

    # 这里允许“仅二级子模块指针变化”，以便把 gitlink 更新提交到一级子模块
    if ! ensure_only_submodule_pointer_changes_or_skip "$root/$sm"; then
      continue
    fi

    local nested_bumped=()
    while IFS= read -r np; do
      [[ -n "$np" ]] && nested_bumped+=("$np")
    done < <(list_bumped_submodules_in_repo "$root/$sm")

    if [[ "${#nested_bumped[@]}" -eq 0 ]]; then
      info "[$sm] 未发现二级子模块指针更新(+)，跳过"
      continue
    fi

    # 只 add 二级子模块路径（gitlink 指针更新）
    for np in "${nested_bumped[@]}"; do
      git -C "$root/$sm" add "$np"
    done

    local joined_nested
    joined_nested="$(msg_join_cn "${nested_bumped[@]}")"
    local msg_sub
    msg_sub="chore(submodule): 更新二级子模块指针: ${joined_nested}"
    info "[$sm] 提交并推送 -> $SUB_REMOTE/$SUB_BRANCH"
    commit_and_push_if_staged "$root/$sm" "$SUB_REMOTE" "$SUB_BRANCH" "$msg_sub"
  done

  # 2) 回到根仓库：提交一级子模块指针更新
  checkout_main_or_die "$root" "$ROOT_REMOTE" "$ROOT_BRANCH" || true
  pull_ff_only_or_skip "$root" "$ROOT_REMOTE" "$ROOT_BRANCH" || true

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