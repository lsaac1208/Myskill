#!/bin/bash
#
# yt-dlp wrapper - Bash 包装器（增强版）
#

set -e

PYTHON_SCRIPT="$HOME/.claude/skills/yt-dlp/scripts/wrapper.py"

# 显示帮助
show_help() {
    cat << EOF
🎬 yt-dlp 视频下载工具（增强版）

用法:
    $0 <command> [args...]

命令:
    download <url> [dir] [format] [--subtitle]    下载视频（自动合并）
    audio <url> [dir]                          提取音频
    formats <url>                                 列出可用格式
    merge <video> <audio> <output>                合并视频和音频
    env                                          显示环境信息
    help                                         显示此帮助

参数:
    url          视频/音频 URL（必需）
    dir          输出目录（可选，默认：当前目录）
    format       视频格式（可选，默认：best）
    --subtitle   包含字幕（可选）

示例:
    # 下载视频
    $0 download "https://www.bilibili.com/video/BV1xx411c7mD"
    $0 download "视频URL" ./videos best
    $0 download "视频URL" ./videos best --subtitle

    # 提取音频
    $0 audio "https://www.bilibili.com/video/BV1xx411c7mD"

    # 列出格式
    $0 formats "https://www.bilibili.com/video/BV1xx411c7mD"

    # 合并视频和音频
    $0 merge video.mp4 audio.m4a output.mp4

    # 检查环境
    $0 env

安装 yt-dlp:
    pip3 install yt-dlp

或使用国内镜像:
    pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple yt-dlp

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
        download)
            if [ $# -eq 0 ]; then
                echo "❌ 错误: download 命令需要 URL"
                exit 1
            fi

            url="$1"
            dir="${2:-.}"
            format="${3:-best}"
            subtitle="${4:-}"

            if [ "$subtitle" = "--subtitle" ]; then
                python3 "$PYTHON_SCRIPT" download "$url" "$dir" "$format" --subtitle
            else
                python3 "$PYTHON_SCRIPT" download "$url" "$dir" "$format"
            fi
            ;;
        audio)
            if [ $# -eq 0 ]; then
                echo "❌ 错误: audio 命令需要 URL"
                exit 1
            fi

            url="$1"
            dir="${2:-.}"

            python3 "$PYTHON_SCRIPT" audio "$url" "$dir"
            ;;
        formats)
            if [ $# -eq 0 ]; then
                echo "❌ 错误: formats 命令需要 URL"
                exit 1
            fi

            python3 "$PYTHON_SCRIPT" formats "$1"
            ;;
        merge)
            if [ $# -lt 3 ]; then
                echo "❌ 错误: merge 命令需要 video audio output 参数"
                exit 1
            fi

            video="$1"
            audio="$2"
            output="$3"

            python3 "$PYTHON_SCRIPT" merge "$video" "$audio" "$output"
            ;;
        env)
            python3 "$PYTHON_SCRIPT" env
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "❌ 未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
