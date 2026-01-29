#!/bin/bash
#
# 本地搜索工具 - Bash 包装器 v2.2.0
#

set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PYTHON_SCRIPT="$HOME/.claude/skills/local-search/scripts/local_search.py"

# 显示帮助
show_help() {
    cat << EOF
${BLUE}本地搜索工具 v2.2.0${NC} - 不消耗 GLM MCP 额度

${YELLOW}用法:${NC}
    $0 <命令> [参数]

${YELLOW}命令:${NC}
    search <关键词>        通用搜索（自动识别意图）
    github <关键词>        GitHub 搜索（仓库/代码/Issue/PR）
    help                   显示此帮助

${YELLOW}通用搜索选项:${NC}
    -n <数量>              结果数量（默认: 10）
    --json                 输出 JSON 格式
    -e <引擎>              指定搜索引擎 (google baidu duckduckgo)
    -q, --quiet            简洁模式

${YELLOW}GitHub 搜索选项:${NC}
    -t <类型>              搜索类型: repos/code/issues/prs/users
    -n <数量>              结果数量（默认: 10）
    -q, --quiet            简洁模式

${YELLOW}示例:${NC}
    $0 search "武汉天气"
    $0 search "AI 最新进展" -n 20 -e google baidu
    $0 github "rust" -t repos
    $0 github "search" -t code -q

${YELLOW}优势:${NC}
    ✅ 完全本地运行
    ✅ 不消耗 GLM MCP 额度
    ✅ 无限次使用
    ✅ 智能意图识别
    ✅ 多引擎聚合
EOF
}

# 主函数
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    local command="$1"
    shift

    case "$command" in
        search)
            if [ $# -eq 0 ]; then
                echo -e "${RED}❌ 错误: search 命令需要指定关键词${NC}"
                exit 1
            fi
            python3 "$PYTHON_SCRIPT" search "$@"
            ;;
        github|gh)
            if [ $# -eq 0 ]; then
                echo -e "${RED}❌ 错误: github 命令需要指定关键词${NC}"
                exit 1
            fi
            python3 "$PYTHON_SCRIPT" github "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ 未知命令: $command${NC}"
            echo -e "${YELLOW}使用 '$0 help' 查看帮助${NC}"
            exit 1
            ;;
    esac
}

main "$@"
