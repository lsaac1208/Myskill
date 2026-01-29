#!/usr/bin/env python3
"""
为自定义 Skills 添加 GitHub 版本追踪 - 完整指南

本指南将帮助您为所有自定义 Skills 创建 GitHub 仓库并建立版本追踪机制。
"""

import os
from pathlib import Path

SKILLS_DIR = Path("/Users/wang/.claude/skills")

GUIDE = """
# 为自定义 Skills 添加 GitHub 版本追踪

## 📋 概述

本指南将帮助您为以下 10 个自定义 Skills 创建 GitHub 仓库：

1. docx - Word 文档处理
2. xlsx - Excel 表格处理
3. pptx - PowerPoint 演示文稿处理
4. local-search - 本地搜索引擎
5. mcp-builder - MCP 服务器构建器
6. artifacts-builder - Artifacts 构建器
7. skill-manager - Skills 管理器
8. skill-evolution-manager - Skills 进化管理器
9. github-to-skills - GitHub 仓库转 Skill 工具
10. webapp-testing - Web 应用测试工具

## 🎯 目标

完成后，您将能够：
- ✅ 使用 skill-manager 统一管理所有 Skills 的更新
- ✅ 追踪每个 Skill 的版本历史
- ✅ 在多台设备间同步 Skills
- ✅ 与他人分享您的 Skills

## 📝 前置要求

1. **GitHub 账号**: 确保您有 GitHub 账号
2. **Git 安装**: 确保系统已安装 Git
3. **GitHub CLI (可选)**: 安装 gh 可以简化仓库创建

验证环境：
```bash
git --version
gh --version  # 可选
```

## 🚀 快速开始

### 方法 1: 使用自动化脚本（推荐）

```bash
# 1. 运行初始化脚本
python3 ~/.claude/skills/.tools/init-github-repos.py

# 2. 按照脚本提示在 GitHub 上创建仓库

# 3. 推送代码到 GitHub

# 4. 更新 SKILL.md 的 frontmatter
python3 ~/.claude/skills/.tools/update-github-info.py
```

### 方法 2: 使用快速脚本

```bash
# 一键准备所有仓库
bash ~/.claude/skills/.tools/quick-setup.sh YOUR_GITHUB_USERNAME
```

### 方法 3: 手动操作

参见下面的详细步骤。

## 📖 详细步骤

### 步骤 1: 准备本地仓库

为每个 Skill 初始化 Git 仓库：

```bash
cd ~/.claude/skills/docx

# 初始化 Git
git init

# 创建 .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.DS_Store
*.log
.vscode/
EOF

# 创建 README.md
cat > README.md << 'EOF'
# docx

Word 文档处理 Skill

详细文档请参考 [SKILL.md](SKILL.md)
EOF

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: docx v1.0.0"

# 设置主分支
git branch -M main
```

对其他 9 个 Skills 重复此过程。

### 步骤 2: 在 GitHub 上创建仓库

#### 方法 A: 使用 GitHub CLI（推荐）

```bash
cd ~/.claude/skills/docx

# 创建仓库并推送
gh repo create docx --public --source=. --remote=origin --push

# 设置仓库描述
gh repo edit --description "Word 文档处理 Skill for Claude Code"
```

对其他 Skills 重复此过程。

#### 方法 B: 使用 Web 界面

1. 访问 https://github.com/new
2. 填写信息：
   - Repository name: `docx`
   - Description: `Word 文档处理 Skill for Claude Code`
   - Public/Private: 根据需要选择
   - **不要**初始化 README、.gitignore 或 LICENSE
3. 点击 "Create repository"
4. 按照页面提示推送代码：

```bash
cd ~/.claude/skills/docx
git remote add origin https://github.com/YOUR_USERNAME/docx.git
git push -u origin main
```

对其他 9 个 Skills 重复此过程。

### 步骤 3: 更新 SKILL.md

为每个 Skill 的 SKILL.md 添加 GitHub 信息：

```bash
cd ~/.claude/skills/docx

# 获取当前 commit hash
HASH=$(git rev-parse HEAD)

# 编辑 SKILL.md，在 frontmatter 中添加：
# github_url: https://github.com/YOUR_USERNAME/docx
# github_hash: $HASH
```

或使用自动化脚本：

```bash
python3 ~/.claude/skills/.tools/update-github-info.py
```

### 步骤 4: 验证设置

运行 skill-manager 验证所有 Skills 的 GitHub 追踪：

```bash
cd ~/.claude/skills/skill-manager
python scripts/scan_and_check.py ~/.claude/skills
```

您应该看到所有 10 个自定义 Skills 都有 GitHub 信息。

## 📊 预期结果

完成后，运行 `skill-manager` 应该显示：

```json
{
  "name": "docx",
  "github_url": "https://github.com/YOUR_USERNAME/docx",
  "local_hash": "abc123...",
  "remote_hash": "abc123...",
  "status": "current",
  "message": "Up to date"
}
```

## 🔄 日常使用

### 更新 Skill

```bash
cd ~/.claude/skills/docx

# 修改代码...

# 提交更改
git add .
git commit -m "Add new feature"
git push

# 更新 SKILL.md 中的 github_hash
HASH=$(git rev-parse HEAD)
# 编辑 SKILL.md，更新 github_hash
```

### 检查更新

```bash
cd ~/.claude/skills/skill-manager
python scripts/scan_and_check.py ~/.claude/skills
```

### 同步到其他设备

```bash
cd ~/.claude/skills
git clone https://github.com/YOUR_USERNAME/docx.git
git clone https://github.com/YOUR_USERNAME/xlsx.git
# ... 其他 Skills
```

## 🐛 常见问题

### 1. Git 仓库已存在

**症状**: `fatal: destination path 'docx' already exists`

**解决方案**:
```bash
cd ~/.claude/skills/docx
git remote add origin https://github.com/YOUR_USERNAME/docx.git
git push -u origin main
```

### 2. 推送被拒绝

**症状**: `error: failed to push some refs`

**解决方案**:
```bash
git pull origin main --rebase
git push -u origin main
```

### 3. 无法获取 commit hash

**症状**: `fatal: ambiguous argument 'HEAD'`

**解决方案**: 确保已创建至少一个提交
```bash
git add .
git commit -m "Initial commit"
```

## 📝 最佳实践

1. **提交信息规范**:
   - `feat: 添加新功能`
   - `fix: 修复 bug`
   - `docs: 更新文档`
   - `refactor: 重构代码`

2. **版本号管理**:
   - 遵循语义化版本 (Semantic Versioning)
   - 主版本.次版本.修订号 (如 1.2.3)

3. **定期同步**:
   - 每次修改后及时提交和推送
   - 定期运行 skill-manager 检查更新

4. **文档维护**:
   - 保持 SKILL.md 和 README.md 同步
   - 更新版本号和更新日志

## 🔗 相关工具

- **skill-manager**: 管理和更新 Skills
- **skill-evolution-manager**: 优化和迭代 Skills
- **github-to-skills**: 从 GitHub 创建新 Skills

## 📞 获取帮助

如果遇到问题：

1. 查看本指南的常见问题部分
2. 检查 Git 和 GitHub 的官方文档
3. 运行 `git status` 查看当前状态

---

**创建日期**: 2026-01-26
**版本**: 1.0.0
"""

def main():
    print(GUIDE)

    # 保存指南到文件
    guide_path = SKILLS_DIR / ".tools" / "GITHUB_SETUP_GUIDE.md"
    guide_path.write_text(GUIDE)
    print(f"\n✅ 指南已保存到: {guide_path}")

if __name__ == "__main__":
    main()
