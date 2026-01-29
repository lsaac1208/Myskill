---
name: yt-dlp
description: 视频下载时自动触发 - 下载视频、youtube下载、yt-dlp、视频解析、视频下载器、音视频下载。支持数千个网站的音视频下载工具，是 youtube-dl 的活跃分支。
github_url: https://github.com/yt-dlp/yt-dlp
github_hash: e3f0d8b731b40176bcc632bf92cfe5149402b202
version: 1.2.0
created_at: 2025-01-24
updated_at: 2025-01-25
entry_point: scripts/wrapper.sh
dependencies: []
---

# yt-dlp Skill

功能丰富的命令行音视频下载器，支持数千个网站。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **视频下载**: "下载 xxx 视频"、"xxx 下载"、"保存视频"
- **YouTube**: "youtube 下载"、"yt-dlp"、"从 YouTube 下载"
- **音视频**: "下载音频"、"提取视频"、"下载影片"
- **哔哩哔哩**: "下载 B站视频"、"bilibili 下载"
- **工具使用**: "使用 yt-dlp 下载"

## ✨ 新增功能（v1.1.0）

- ✅ **智能检测**: 自动检测 `yt-dlp` 和 `python3 -m yt_dlp`
- ✅ **FFmpeg 自动发现**: 自动查找系统中的 ffmpeg（包括 BambuStudio 附带版本）
- ✅ **自动合并**: 检测到 ffmpeg 时自动合并视频和音频
- ✅ **手动合并**: 支持手动合并已下载的视频和音频文件
- ✅ **环境检测**: `env` 命令查看工具安装状态
- ✅ **哔哩哔哩优化**: 针对哔哩哔哩的专门提示和错误处理
- ✅ **国内镜像**: 支持使用清华大学镜像加速安装

## 🚀 使用方法

### 检查环境
```bash
# 检查 yt-dlp 和 ffmpeg 安装状态
~/.claude/skills/yt-dlp/scripts/wrapper.sh env
```

### 下载视频
```bash
# 下载单个视频（自动合并）
~/.claude/skills/yt-dlp/scripts/wrapper.sh download "视频URL"

# 下载到指定目录
~/.claude/skills/yt-dlp/scripts/wrapper.sh download "视频URL" ./videos

# 下载指定格式
~/.claude/skills/yt-dlp/scripts/wrapper.sh download "视频URL" ./videos best

# 下载带字幕
~/.claude/skills/yt-dlp/scripts/wrapper.sh download "视频URL" ./videos best --subtitle
```

### 提取音频
```bash
~/.claude/skills/yt-dlp/scripts/wrapper.sh audio "视频URL"
```

### 列出格式
```bash
~/.claude/skills/yt-dlp/scripts/wrapper.sh formats "视频URL"
```

### 合并视频和音频
```bash
~/.claude/skills/yt-dlp/scripts/wrapper.sh merge video.mp4 audio.m4a output.mp4
```

## 📋 支持的功能

| 功能 | 说明 |
|------|------|
| **多平台支持** | Windows、macOS、Linux |
| **智能检测** | 自动检测多种 yt-dlp 安装方式 |
| **格式选择** | 视频/音频/字幕单独或组合 |
| **自动合并** | 检测到 ffmpeg 时自动合并视频音频 |
| **播放列表** | 支持整个播放列表下载 |
| **元数据** | 保存视频标题、描述、缩略图 |
| **哔哩哔哩优化** | 针对性提示和错误处理 |

## 🔧 安装

### yt-dlp 安装

**方法 1: pip 安装（推荐）**
```bash
pip3 install yt-dlp
```

**方法 2: 使用国内镜像（更快）**
```bash
pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple yt-dlp
```

### ffmpeg 安装

**macOS - Homebrew（推荐）**
```bash
brew install ffmpeg
```

**macOS - 查找系统自带**
```bash
# 检查是否已安装（如 BambuStudio 附带）
~/.claude/skills/yt-dlp/scripts/wrapper.sh env
```

**常见 ffmpeg 位置:**
- BambuStudio: `~/Library/Application Support/BambuStudio/cameratools/ffmpeg`
- Homebrew Intel: `/usr/local/bin/ffmpeg`
- Homebrew ARM: `/opt/homebrew/bin/ffmpeg`

## 🎬 哔哩哔哩使用指南

### 格式说明

| 格式代码 | 分辨率 | 说明 |
|---------|--------|------|
| 30080 | 1412x1080 | 1080P AVC（推荐） |
| 30077 | 1412x1080 | 1080P HEVC（文件更小） |
| 100026 | 1412x1080 | 1080P AV1（最新编码） |
| 30064 | 940x720 | 720P |
| 30032 | 628x480 | 480P |

### 下载示例

```bash
# 下载 1080P 最佳质量
~/.claude/skills/yt-dlp/scripts/wrapper.sh download "https://www.bilibili.com/video/BV1xx411c7mD" ./videos 30077

# 下载带字幕
~/.claude/skills/yt-dlp/scripts/wrapper.sh download "URL" ./videos best --subtitle
```

### 高清视频提示

**1080P+ 高清视频需要大会员:**

方法 1 - 使用浏览器 Cookies:
```bash
# 导出浏览器 cookies
yt-dlp --cookies-from-browser safari "URL"
```

方法 2 - 手动上传 cookies:
```bash
# 1. 导出浏览器 cookie 为 cookies.txt
# 2. 使用 cookies 下载
yt-dlp --cookies cookies.txt "URL"
```

## 🐛 常见问题

### 1. yt-dlp 未找到
**症状**: `yt-dlp: command not found`

**解决方案**:
```bash
pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple yt-dlp
```

### 2. 视频和音频分开下载
**症状**: 下载了 .mp4 和 .m4a 两个文件

**解决方案**:
```bash
# 方法 1: 安装 ffmpeg 后重新下载（自动合并）
brew install ffmpeg

# 方法 2: 手动合并已有文件
~/.claude/skills/yt-dlp/scripts/wrapper.sh merge video.mp4 audio.m4a output.mp4
```

### 3. 哔哩哔哩 1080P 无法下载
**症状**: 提示需要 Premium 会员

**解决方案**:
- 登录哔哩哔哩大会员账号
- 使用 `--cookies-from-browser` 参数
- 或接受 720P 画质

### 4. macOS 13 无法安装 ffmpeg
**症状**: Homebrew 安装失败，提示系统版本太老

**解决方案**:
- 检查系统是否已有 ffmpeg（如 BambuStudio）
- 使用 `env` 命令查看
- 或升级到 macOS 14+

## 📖 参考资料

- **官方文档**: https://github.com/yt-dlp/yt-dlp
- **支持网站**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
- **安装指南**: https://github.com/yt-dlp/yt-dlp/wiki/Installation
- **FAQ**: https://github.com/yt-dlp/yt-dlp/wiki/FAQ
- **格式选择**: https://github.com/yt-dlp/yt-dlp#format-selection

## 📝 更新日志

### v1.2.0 (2026-01-26)
- ✨ 更新到最新版本 (e3f0d8b)
- 🔄 同步上游最新功能和修复

### v1.1.0 (2025-01-25)
- ✨ 新增智能 yt-dlp 检测（支持 `python3 -m yt_dlp`）
- ✨ 新增 ffmpeg 自动发现功能
- ✨ 新增视频音频自动合并
- ✨ 新增手动合并命令
- ✨ 新增环境检测命令
- ✨ 优化哔哩哔哩支持和错误提示
- ✨ 添加国内镜像安装方式
- 📝 完善文档和常见问题

### v1.0.0 (2025-01-24)
- 🎉 初始版本
- 支持基础视频下载、音频提取、格式列表

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 优先使用 python3 -m yt_dlp 而不是 yt-dlp 命令
- 下载哔哩哔哩视频时优先使用 HEVC 格式（30077）
- 使用国内镜像（清华大学）加速 pip 安装

### Known Fixes & Workarounds
- yt-dlp 命令未找到时，自动尝试 python3 -m yt_dlp
- ffmpeg 未安装时，自动搜索系统常见位置（如 BambuStudio）
- 哔哩哔哩 1080P+ 下载失败时，提示使用 --cookies-from-browser
- macOS 13 Homebrew 安装失败时，查找系统已有 ffmpeg

### Custom Instruction Injection

# yt-dlp 使用提示

## 调用方式
- 优先使用: python3 -m yt_dlp
- 备用: yt-dlp

## ffmpeg 检测
- PATH 搜索
- BambuStudio: ~/Library/Application Support/BambuStudio/cameratools/ffmpeg
- Homebrew: /usr/local/bin/ffmpeg 或 /opt/homebrew/bin/ffmpeg

## 哔哩哔哩格式
- 30077: 1080P HEVC（推荐）
- 30080: 1080P AVC
- 100026: 1080P AV1

## 安装命令
pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple yt-dlp