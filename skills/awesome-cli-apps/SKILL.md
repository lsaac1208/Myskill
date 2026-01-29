---
name: awesome-cli-apps
description: CLI工具查询时自动触发 - cli工具、命令行工具、终端工具、cli应用、awesome cli、查找cli、搜索cli工具。精选命令行应用列表，提供各类 CLI 工具的查询和搜索功能。
github_url: https://github.com/agarrharr/awesome-cli-apps
github_hash: a50370d6ffd9e9bec41d36f007d15fb8738a7b76
version: 0.2.0
created_at: 2026-01-25T14:21:13.075353
updated_at: 2026-01-26
entry_point: scripts/wrapper.py
dependencies: []
license: CC0-1.0
---

# Awesome CLI Apps Skill

精选命令行应用大全，涵盖各类实用的终端工具和 CLI 应用。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **CLI 工具**: "cli 工具"、"命令行工具"、"终端工具"
- **工具查找**: "找 cli 工具"、"搜索命令行工具"
- **效率工具**: "提高效率"、"终端效率工具"
- **开发工具**: "开发者工具"、"程序员工具"

## ✨ 核心功能

- ✅ **分类齐全**: 涵盖 20+ 个工具分类
- ✅ **精选推荐**: 社区精选的优质工具
- ✅ **持续更新**: 定期添加新工具
- ✅ **跨平台**: 支持 Linux、macOS、Windows
- ✅ **开源免费**: 大部分工具开源且免费
- ✅ **实用导向**: 注重工具的实用性

## 🚀 工具分类

### 📁 文件管理

#### 文件浏览器
- **ranger**: 强大的文件管理器
- **nnn**: 快速轻量的文件浏览器
- **lf**: 类似 ranger 的文件管理器
- **vifm**: Vi 风格的文件管理器

#### 文件搜索
- **fd**: find 的现代替代品
- **fzf**: 命令行模糊查找器
- **ripgrep (rg)**: 超快的文本搜索工具
- **ag (The Silver Searcher)**: 代码搜索工具

#### 文件操作
- **trash-cli**: 安全删除文件（移到回收站）
- **rsync**: 文件同步工具
- **rclone**: 云存储同步工具
- **duf**: 磁盘使用情况查看器

### 💻 系统工具

#### 系统监控
- **htop**: 交互式进程查看器
- **btop**: 资源监控器
- **glances**: 跨平台系统监控工具
- **bottom**: 图形化系统监控

#### 进程管理
- **procs**: ps 的现代替代品
- **killall**: 批量终止进程
- **pgrep**: 按名称查找进程

#### 网络工具
- **httpie**: 用户友好的 HTTP 客户端
- **curl**: 数据传输工具
- **wget**: 文件下载工具
- **speedtest-cli**: 网速测试

### 🎨 终端美化

#### Shell 增强
- **oh-my-zsh**: Zsh 配置框架
- **starship**: 跨 Shell 的提示符
- **powerlevel10k**: Zsh 主题
- **fish**: 友好的交互式 Shell

#### 终端模拟器
- **alacritty**: GPU 加速的终端
- **kitty**: 功能丰富的终端
- **wezterm**: GPU 加速的跨平台终端
- **tmux**: 终端复用器

#### 颜色和主题
- **lolcat**: 彩虹色输出
- **figlet**: ASCII 艺术字
- **toilet**: ASCII 艺术生成器

### 📝 文本处理

#### 文本编辑
- **vim/neovim**: 强大的文本编辑器
- **emacs**: 可扩展的文本编辑器
- **nano**: 简单易用的编辑器
- **micro**: 现代化的终端编辑器

#### 文本查看
- **bat**: cat 的增强版
- **less**: 分页查看器
- **most**: 彩色分页查看器

#### 文本处理
- **jq**: JSON 处理工具
- **yq**: YAML 处理工具
- **sed**: 流编辑器
- **awk**: 文本处理语言

### 🔧 开发工具

#### 版本控制
- **git**: 分布式版本控制
- **lazygit**: Git 的 TUI 界面
- **tig**: Git 的文本界面
- **gh**: GitHub CLI

#### 代码工具
- **prettier**: 代码格式化
- **eslint**: JavaScript 代码检查
- **black**: Python 代码格式化
- **rustfmt**: Rust 代码格式化

#### 构建工具
- **make**: 构建自动化工具
- **cmake**: 跨平台构建系统
- **ninja**: 小型构建系统
- **task**: 任务运行器

### 📦 包管理

#### 系统包管理
- **apt**: Debian/Ubuntu 包管理器
- **yum/dnf**: RedHat/Fedora 包管理器
- **pacman**: Arch Linux 包管理器
- **brew**: macOS 包管理器

#### 语言包管理
- **npm**: Node.js 包管理器
- **pip**: Python 包管理器
- **cargo**: Rust 包管理器
- **gem**: Ruby 包管理器

### 🌐 网络工具

#### HTTP 工具
- **httpie**: 现代 HTTP 客户端
- **curl**: 数据传输工具
- **wget**: 文件下载工具
- **aria2**: 多线程下载工具

#### 网络诊断
- **ping**: 网络连通性测试
- **traceroute**: 路由追踪
- **nmap**: 网络扫描工具
- **netcat**: 网络工具瑞士军刀

#### SSH 工具
- **ssh**: 安全远程登录
- **scp**: 安全文件传输
- **rsync**: 远程同步工具
- **mosh**: 移动 Shell

### 📊 数据处理

#### 数据转换
- **jq**: JSON 处理
- **yq**: YAML 处理
- **csvkit**: CSV 工具集
- **xmlstarlet**: XML 处理

#### 数据分析
- **pandas**: Python 数据分析
- **datamash**: 命令行数据处理
- **miller**: CSV/JSON 处理

### 🎵 多媒体

#### 音频工具
- **ffmpeg**: 音视频处理
- **sox**: 音频处理
- **mpv**: 媒体播放器
- **cmus**: 音乐播放器

#### 图像工具
- **imagemagick**: 图像处理
- **ffmpeg**: 视频处理
- **gifsicle**: GIF 处理

#### 视频工具
- **youtube-dl**: 视频下载
- **yt-dlp**: youtube-dl 的分支
- **ffmpeg**: 视频转换

### 🔐 安全工具

#### 密码管理
- **pass**: Unix 密码管理器
- **1password-cli**: 1Password CLI
- **bitwarden-cli**: Bitwarden CLI

#### 加密工具
- **gpg**: 加密和签名
- **openssl**: 加密工具包
- **age**: 现代加密工具

#### 安全扫描
- **nmap**: 网络扫描
- **nikto**: Web 服务器扫描
- **sqlmap**: SQL 注入工具

### 📚 文档工具

#### 文档生成
- **pandoc**: 文档转换工具
- **asciidoctor**: AsciiDoc 处理器
- **sphinx**: Python 文档生成器

#### Markdown 工具
- **glow**: Markdown 渲染器
- **mdcat**: Markdown 查看器
- **grip**: GitHub 风格 Markdown 预览

### 🎮 娱乐工具

#### 游戏
- **nethack**: 经典 Roguelike 游戏
- **2048**: 2048 游戏
- **tetris**: 俄罗斯方块

#### 趣味工具
- **cowsay**: 会说话的牛
- **fortune**: 随机名言
- **sl**: 蒸汽火车动画

## 📋 推荐工具

### 🔥 必装工具

| 工具 | 描述 | 用途 |
|------|------|------|
| **fzf** | 模糊查找器 | 文件/命令查找 |
| **ripgrep** | 文本搜索 | 代码搜索 |
| **bat** | cat 增强版 | 文件查看 |
| **fd** | find 替代品 | 文件搜索 |
| **htop** | 进程查看器 | 系统监控 |
| **tmux** | 终端复用器 | 会话管理 |
| **git** | 版本控制 | 代码管理 |
| **vim** | 文本编辑器 | 文件编辑 |

### 🌟 效率工具

| 工具 | 描述 | 提升效率 |
|------|------|---------|
| **zoxide** | 智能目录跳转 | 快速导航 |
| **autojump** | 目录跳转 | 快速切换 |
| **thefuck** | 命令纠错 | 自动修正 |
| **tldr** | 简化的 man 页面 | 快速查询 |
| **exa** | ls 增强版 | 文件列表 |
| **delta** | Git diff 美化 | 代码对比 |

### 💎 现代替代品

| 传统工具 | 现代替代品 | 优势 |
|---------|-----------|------|
| **cat** | bat | 语法高亮、行号 |
| **ls** | exa/lsd | 彩色、图标、树形 |
| **find** | fd | 更快、更简单 |
| **grep** | ripgrep | 更快、更智能 |
| **du** | dust/duf | 可视化、更直观 |
| **top** | htop/btop | 交互式、更美观 |
| **ps** | procs | 彩色、更多信息 |
| **cd** | zoxide | 智能跳转 |

## 🔧 安装方法

### macOS - Homebrew

```bash
# 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装工具
brew install fzf ripgrep bat fd htop tmux
brew install exa zoxide tldr
```

### Linux - apt (Debian/Ubuntu)

```bash
# 更新包列表
sudo apt update

# 安装工具
sudo apt install fzf ripgrep bat fd-find htop tmux
sudo apt install exa zoxide tldr
```

### Linux - pacman (Arch)

```bash
# 安装工具
sudo pacman -S fzf ripgrep bat fd htop tmux
sudo pacman -S exa zoxide tldr
```

### 通用 - Cargo (Rust)

```bash
# 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装工具
cargo install ripgrep fd-find bat exa zoxide
```

## 📝 使用示例

### 示例 1: 文件搜索组合

```bash
# 使用 fd 查找文件，fzf 选择，bat 预览
fd --type f | fzf --preview 'bat --color=always {}'

# 使用 ripgrep 搜索内容，fzf 选择
rg --line-number . | fzf --preview 'bat --color=always {1} --highlight-line {2}'

# 快速跳转到目录
z project  # 使用 zoxide 跳转
```

### 示例 2: Git 工作流

```bash
# 使用 lazygit 管理 Git
lazygit

# 使用 delta 美化 diff
git diff | delta

# 使用 gh 管理 GitHub
gh pr list
gh issue create
```

### 示例 3: 系统监控

```bash
# 使用 htop 查看进程
htop

# 使用 btop 查看资源
btop

# 使用 duf 查看磁盘
duf

# 使用 procs 查看进程
procs
```

### 示例 4: 文本处理

```bash
# 使用 jq 处理 JSON
curl https://api.github.com/users/github | jq '.name'

# 使用 bat 查看文件
bat README.md

# 使用 ripgrep 搜索代码
rg "function" --type js
```

## 🐛 常见问题

### 1. 工具安装失败

**症状**: 包管理器找不到工具

**解决方案**:
```bash
# 更新包列表
sudo apt update  # Debian/Ubuntu
brew update      # macOS

# 检查工具名称
# 有些工具在不同系统中名称不同
# 例如: fd-find (Ubuntu) vs fd (macOS)
```

### 2. 命令冲突

**症状**: 新工具与系统命令冲突

**解决方案**:
```bash
# 使用别名
alias cat='bat'
alias ls='exa'
alias find='fd'

# 或使用完整路径
/usr/bin/cat file.txt
```

### 3. 配置文件位置

**症状**: 不知道配置文件在哪里

**解决方案**:
```bash
# 常见配置文件位置
~/.config/      # 大多数现代工具
~/.zshrc        # Zsh 配置
~/.bashrc       # Bash 配置
~/.vimrc        # Vim 配置
~/.tmux.conf    # Tmux 配置
```

### 4. 性能问题

**症状**: 工具运行缓慢

**解决方案**:
```bash
# 检查是否有大量文件
# 使用 --max-depth 限制搜索深度
fd --max-depth 3

# 排除不需要的目录
rg "pattern" --glob '!node_modules'

# 使用缓存
zoxide query --list
```

## 📖 推荐配置

### Zsh 配置

```bash
# ~/.zshrc

# 使用 Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"

# 插件
plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  fzf
  zoxide
)

# 别名
alias cat='bat'
alias ls='exa --icons'
alias ll='exa -l --icons'
alias la='exa -la --icons'
alias tree='exa --tree --icons'
alias find='fd'
alias grep='rg'

# 初始化 zoxide
eval "$(zoxide init zsh)"

# 初始化 starship
eval "$(starship init zsh)"
```

### Tmux 配置

```bash
# ~/.tmux.conf

# 使用 Ctrl+a 作为前缀
set -g prefix C-a
unbind C-b

# 启用鼠标
set -g mouse on

# 窗口编号从 1 开始
set -g base-index 1
setw -g pane-base-index 1

# 快速重载配置
bind r source-file ~/.tmux.conf \; display "Reloaded!"

# 分割窗口
bind | split-window -h
bind - split-window -v
```

### Git 配置

```bash
# ~/.gitconfig

[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true
    light = false
    side-by-side = true

[merge]
    conflictstyle = diff3

[diff]
    colorMoved = default
```

## 📖 学习资源

### 在线资源

- **Awesome CLI Apps**: https://github.com/agarrharr/awesome-cli-apps
- **命令行的艺术**: https://github.com/jlevy/the-art-of-command-line
- **Linux 命令大全**: https://wangchujiang.com/linux-command/
- **ExplainShell**: https://explainshell.com/

### 推荐书籍

- **《Linux 命令行与 Shell 脚本编程大全》**
- **《鸟哥的 Linux 私房菜》**
- **《Unix/Linux 编程实践教程》**

### 视频教程

- **Linux 命令行基础**
- **Vim 从入门到精通**
- **Tmux 使用教程**

## 📖 参考资料

- **GitHub 仓库**: https://github.com/agarrharr/awesome-cli-apps
- **命令行工具对比**: https://github.com/ibraheemdev/modern-unix
- **终端工具推荐**: https://github.com/rothgar/awesome-tuis

## 📝 更新日志

### v0.2.0 (2026-01-26)
- ✨ 更新到最新版本 (a50370d)
- 📝 完善文档和工具分类
- ✨ 添加工具推荐和对比
- ✨ 添加安装方法和使用示例
- ✨ 添加配置文件示例
- ✨ 添加常见问题解答

### v0.1.0 (2026-01-25)
- 🎉 初始版本
