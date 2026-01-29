#!/usr/bin/env bash
# 为自定义 Skills 创建 GitHub 仓库的快速脚本

set -e

SKILLS_DIR="$HOME/.claude/skills"
GITHUB_USERNAME="${1:-YOUR_USERNAME}"

if [ "$GITHUB_USERNAME" = "YOUR_USERNAME" ]; then
    echo "❌ 请提供 GitHub 用户名"
    echo "用法: $0 <github-username>"
    exit 1
fi

echo "🚀 为自定义 Skills 创建 GitHub 仓库"
echo "GitHub 用户名: $GITHUB_USERNAME"
echo "="

# Skills 列表
SKILLS=(
    "docx"
    "xlsx"
    "pptx"
    "local-search"
    "mcp-builder"
    "artifacts-builder"
    "skill-manager"
    "skill-evolution-manager"
    "github-to-skills"
    "webapp-testing"
)

echo "将处理 ${#SKILLS[@]} 个 Skills"
echo ""
read -p "按 Enter 继续..."

for skill in "${SKILLS[@]}"; do
    echo ""
    echo "========================================="
    echo "处理: $skill"
    echo "========================================="

    cd "$SKILLS_DIR/$skill"

    # 初始化 Git（如果还没有）
    if [ ! -d ".git" ]; then
        echo "📦 初始化 Git 仓库..."
        git init
    fi

    # 添加所有文件
    echo "📝 添加文件..."
    git add .

    # 创建初始提交
    if ! git rev-parse HEAD >/dev/null 2>&1; then
        echo "💾 创建初始提交..."
        git commit -m "Initial commit: $skill"
    fi

    # 设置主分支
    git branch -M main

    # 添加远程仓库
    if ! git remote get-url origin >/dev/null 2>&1; then
        echo "🔗 添加远程仓库..."
        git remote add origin "https://github.com/$GITHUB_USERNAME/$skill.git"
    fi

    echo "✅ $skill 准备完成"
    echo ""
    echo "📋 下一步:"
    echo "1. 在 GitHub 创建仓库: https://github.com/new"
    echo "   仓库名: $skill"
    echo "2. 推送代码:"
    echo "   cd $SKILLS_DIR/$skill"
    echo "   git push -u origin main"
    echo ""
done

echo "========================================="
echo "✅ 所有 Skills 已准备完成!"
echo "========================================="
echo ""
echo "📝 后续步骤:"
echo "1. 在 GitHub 上为每个 Skill 创建仓库"
echo "2. 推送代码到远程仓库"
echo "3. 运行更新脚本:"
echo "   python3 $SKILLS_DIR/.tools/update-github-info.py"
