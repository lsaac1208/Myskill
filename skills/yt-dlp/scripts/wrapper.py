#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yt-dlp wrapper - 音视频下载工具（增强版）
支持多种调用方式和自动 ffmpeg 检测
"""

import sys
import subprocess
import os
import shutil
from pathlib import Path


def find_yt_dlp():
    """查找可用的 yt-dlp"""
    # 方法1: 检查 PATH 中的 yt-dlp 命令
    if shutil.which('yt-dlp'):
        return 'yt-dlp'

    # 方法2: 尝试 python3 -m yt_dlp
    try:
        result = subprocess.run(
            ['python3', '-m', 'yt_dlp', '--version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            return 'python3 -m yt_dlp'
    except:
        pass

    # 方法3: 尝试 python -m yt_dlp
    try:
        result = subprocess.run(
            ['python', '-m', 'yt_dlp', '--version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            return 'python -m yt_dlp'
    except:
        pass

    return None


def find_ffmpeg():
    """查找系统中的 ffmpeg"""
    # 方法1: 检查 PATH
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return ffmpeg_path

    # 方法2: 检查常见位置
    common_paths = [
        '/usr/local/bin/ffmpeg',
        '/opt/homebrew/bin/ffmpeg',
        '/opt/ffmpeg/bin/ffmpeg',
        os.path.expanduser('~/Library/Application Support/BambuStudio/cameratools/ffmpeg'),
        '/Applications/ffmpeg.app/Contents/MacOS/ffmpeg',
    ]

    for path in common_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path

    return None


def check_installed():
    """检查 yt-dlp 和 ffmpeg 是否已安装"""
    yt_dlp_cmd = find_yt_dlp()
    ffmpeg_path = find_ffmpeg()

    return yt_dlp_cmd is not None, ffmpeg_path is not None


def run_yt_dlp(args):
    """运行 yt-dlp 命令"""
    yt_dlp_cmd = find_yt_dlp()

    if not yt_dlp_cmd:
        print("❌ yt-dlp 未安装")
        print("\n📦 安装方法:")
        print("  pip3 install yt-dlp")
        print("  或")
        print("  pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple yt-dlp")
        return False

    # 构建命令
    if 'python' in yt_dlp_cmd:
        cmd = yt_dlp_cmd.split() + args
    else:
        cmd = [yt_dlp_cmd] + args

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 执行失败: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ 找不到命令: {' '.join(cmd)}")
        return False


def download_video(url, output_dir=".", format="best", subtitle=False, merge=True):
    """
    下载视频

    Args:
        url: 视频 URL
        output_dir: 输出目录
        format: 视频格式（默认 best）
        subtitle: 是否下载字幕（默认 False）
        merge: 是否合并视频和音频（默认 True）
    """
    # 检查环境
    has_yt_dlp, has_ffmpeg = check_installed()

    if not has_yt_dlp:
        print("❌ yt-dlp 未安装")
        print("\n📦 安装方法:")
        print("  pip3 install yt-dlp")
        print("  或")
        print("  pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple yt-dlp")
        return

    if merge and not has_ffmpeg:
        print("⚠️  警告: 未找到 ffmpeg，视频和音频将分别下载")
        print("💡 提示: 安装 ffmpeg 可自动合并视频和音频")
        merge = False

    # 构建命令参数
    args = [url, '-o', f'{output_dir}/%(title)s.%(ext)s']

    if format:
        args.extend(['-f', format])

    if subtitle:
        args.append('--write-subs')

    # 如果有 ffmpeg，添加合并参数
    if merge and has_ffmpeg:
        args.extend(['--merge-output-format', 'mp4'])

    print(f"🎬 下载视频: {url}")
    print(f"📁 输出目录: {output_dir}")
    print(f"🎬 格式: {format}")
    if subtitle:
        print("📝 包含字幕: 是")
    if merge:
        print("🔗 自动合并: 是")

    try:
        yt_dlp_cmd = find_yt_dlp()
        if 'python' in yt_dlp_cmd:
            cmd = yt_dlp_cmd.split() + args
        else:
            cmd = [yt_dlp_cmd] + args

        result = subprocess.run(cmd, check=True)
        print("\n✅ 下载完成")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 下载失败: {e}")

        # 针对哔哩哔哩的特殊提示
        if 'bilibili.com' in url:
            print("\n💡 哔哩哔哩提示:")
            print("  - 1080P+ 高清视频需要大会员权限")
            print("  - 使用 --cookies-from-browser=browser 可登录会员账号")
            print("  - 示例: yt-dlp --cookies-from-browser=safari \"URL\"")


def download_audio(url, output_dir="."):
    """只下载音频"""
    has_yt_dlp, _ = check_installed()

    if not has_yt_dlp:
        print("❌ yt-dlp 未安装")
        return

    args = [url, '-x', '--audio-format', 'best', '-o', f'{output_dir}/%(title)s.%(ext)s']

    print(f"🎵 提取音频: {url}")
    print(f"📁 输出目录: {output_dir}")

    run_yt_dlp(args) and print("\n✅ 音频提取完成")


def list_formats(url):
    """列出可用格式"""
    has_yt_dlp, _ = check_installed()

    if not has_yt_dlp:
        print("❌ yt-dlp 未安装")
        return

    print(f"📋 列出格式: {url}\n")

    yt_dlp_cmd = find_yt_dlp()
    if 'python' in yt_dlp_cmd:
        cmd = yt_dlp_cmd.split() + ['-F', url]
    else:
        cmd = [yt_dlp_cmd, '-F', url]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ 列出格式失败: {e}")


def merge_video_audio(video_file, audio_file, output_file):
    """
    使用 ffmpeg 合并视频和音频

    Args:
        video_file: 视频文件路径
        audio_file: 音频文件路径
        output_file: 输出文件路径
    """
    ffmpeg_path = find_ffmpeg()

    if not ffmpeg_path:
        print("❌ 未找到 ffmpeg")
        print("\n💡 ffmpeg 可能的位置:")
        print("  - BambuStudio: ~/Library/Application Support/BambuStudio/cameratools/ffmpeg")
        print("  - Homebrew: /usr/local/bin/ffmpeg 或 /opt/homebrew/bin/ffmpeg")
        return False

    print(f"🔗 合并视频和音频...")
    print(f"📹 视频: {os.path.basename(video_file)}")
    print(f"🎵 音频: {os.path.basename(audio_file)}")
    print(f"📁 输出: {os.path.basename(output_file)}")

    cmd = [
        ffmpeg_path,
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-y', output_file
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"\n✅ 合并完成: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 合并失败: {e}")
        return False


def show_environment():
    """显示环境信息"""
    print("🔍 环境检测:\n")

    has_yt_dlp, has_ffmpeg = check_installed()

    # yt-dlp 状态
    if has_yt_dlp:
        yt_dlp_cmd = find_yt_dlp()
        print(f"✅ yt-dlp: {yt_dlp_cmd}")
        try:
            result = subprocess.run(
                yt_dlp_cmd.split() + ['--version'],
                capture_output=True,
                text=True
            )
            version = result.stdout.strip()
            print(f"   版本: {version}")
        except:
            pass
    else:
        print("❌ yt-dlp: 未安装")
        print("   安装: pip3 install yt-dlp")

    print()

    # ffmpeg 状态
    if has_ffmpeg:
        ffmpeg_path = find_ffmpeg()
        print(f"✅ ffmpeg: {ffmpeg_path}")
        try:
            result = subprocess.run(
                [ffmpeg_path, '-version'],
                capture_output=True,
                text=True
            )
            version = result.stdout.split('\n')[0]
            print(f"   {version}")
        except:
            pass
    else:
        print("❌ ffmpeg: 未找到")
        print("   提示: 系统中可能已有 ffmpeg（如 BambuStudio）")


def main():
    if len(sys.argv) < 2:
        print("🎬 yt-dlp 音视频下载工具（增强版）")
        print("\n用法:")
        print("  python wrapper.py download <url> [output_dir] [format] [--subtitle]")
        print("  python wrapper.py audio <url> [output_dir]")
        print("  python wrapper.py formats <url>")
        print("  python wrapper.py merge <video> <audio> <output>")
        print("  python wrapper.py env")
        print("\n示例:")
        print("  python wrapper.py download 'https://www.bilibili.com/video/BV1xx411c7mD'")
        print("  python wrapper.py download 'URL' ./videos best --subtitle")
        print("  python wrapper.py audio 'https://youtube.com/watch?v=xxx'")
        print("  python wrapper.py formats 'https://www.bilibili.com/video/BV1xx411c7mD'")
        print("  python wrapper.py merge video.mp4 audio.m4a output.mp4")
        print("  python wrapper.py env")
        return

    command = sys.argv[1]

    if command == "download":
        if len(sys.argv) < 3:
            print("❌ 缺少 URL 参数")
            return

        url = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        format_ = sys.argv[4] if len(sys.argv) > 4 else "best"
        subtitle = "--subtitle" in sys.argv
        download_video(url, output_dir, format_, subtitle)

    elif command == "audio":
        if len(sys.argv) < 3:
            print("❌ 缺少 URL 参数")
            return

        url = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        download_audio(url, output_dir)

    elif command == "formats":
        if len(sys.argv) < 3:
            print("❌ 缺少 URL 参数")
            return

        url = sys.argv[2]
        list_formats(url)

    elif command == "merge":
        if len(sys.argv) < 5:
            print("❌ 缺少参数")
            print("用法: python wrapper.py merge <video> <audio> <output>")
            return

        video_file = sys.argv[2]
        audio_file = sys.argv[3]
        output_file = sys.argv[4]
        merge_video_audio(video_file, audio_file, output_file)

    elif command == "env":
        show_environment()

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
