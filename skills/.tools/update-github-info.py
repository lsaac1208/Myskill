#!/usr/bin/env python3
"""
批量更新自定义 Skills 的 GitHub 信息

在创建 GitHub 仓库并推送代码后，使用此脚本更新 SKILL.md 的 frontmatter
"""

import os
import re
import subprocess
from pathlib import Path

SKILLS_DIR = Path("/Users/wang/.claude/skills")

# 自定义 Skills 列表
CUSTOM_SKILLS = [
    "docx",
    "xlsx",
    "pptx",
    "local-search",
    "mcp-builder",
    "artifacts-builder",
    "skill-manager",
    "skill-evolution-manager",
    "github-to-skills",
    "webapp-testing"
]

def get_git_hash(skill_dir):
    """获取当前 Git commit hash"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=skill_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return None

def update_skill_frontmatter(skill_name, github_username):
    """更新 Skill 的 frontmatter，添加 GitHub 信息"""
    skill_dir = SKILLS_DIR / skill_name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        print(f"❌ {skill_name}: SKILL.md 不存在")
        return False

    # 检查是否是 Git 仓库
    if not (skill_dir / ".git").exists():
        print(f"⚠️  {skill_name}: 不是 Git 仓库，跳过")
        return False

    # 获取 Git hash
    git_hash = get_git_hash(skill_dir)
    if not git_hash:
        print(f"❌ {skill_name}: 无法获取 Git hash")
        return False

    # 读取文件
    content = skill_md.read_text()

    # 提取 frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print(f"❌ {skill_name}: 无法解析 frontmatter")
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    # 解析字段
    fields = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()

    # 检查是否已有 GitHub 信息
    if 'github_url' in fields:
        print(f"✅ {skill_name}: 已有 GitHub 信息")
        return True

    # 添加 GitHub 信息
    github_url = f"https://github.com/{github_username}/{skill_name}"
    fields['github_url'] = github_url
    fields['github_hash'] = git_hash

    # 重新构建 frontmatter
    ordered_fields = [
        'name', 'description', 'github_url', 'github_hash', 'version',
        'created_at', 'updated_at', 'entry_point', 'dependencies', 'license'
    ]

    new_frontmatter = "---\n"
    for field in ordered_fields:
        if field in fields:
            new_frontmatter += f"{field}: {fields[field]}\n"
    new_frontmatter += "---\n"

    # 写回文件
    new_content = new_frontmatter + body
    skill_md.write_text(new_content)

    print(f"✅ {skill_name}: 已添加 GitHub 信息")
    print(f"   URL: {github_url}")
    print(f"   Hash: {git_hash[:8]}")

    return True

def main():
    print("🔄 批量更新自定义 Skills 的 GitHub 信息")
    print("="*60)

    # 获取 GitHub 用户名
    github_username = input("请输入您的 GitHub 用户名: ").strip()
    if not github_username:
        print("❌ 用户名不能为空")
        return

    print(f"\n将为以下 Skills 添加 GitHub 信息:")
    print(f"GitHub 用户名: {github_username}")
    print(f"Skills 数量: {len(CUSTOM_SKILLS)}")
    print(f"\n按 Enter 继续，或 Ctrl+C 取消...")
    input()

    success_count = 0
    for skill_name in CUSTOM_SKILLS:
        print(f"\n处理: {skill_name}")
        if update_skill_frontmatter(skill_name, github_username):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"✅ 完成! 成功更新 {success_count}/{len(CUSTOM_SKILLS)} 个 Skills")
    print(f"{'='*60}")

    if success_count > 0:
        print(f"\n📝 下一步:")
        print(f"1. 运行 skill-manager 验证更新:")
        print(f"   cd ~/.claude/skills/skill-manager")
        print(f"   python scripts/scan_and_check.py ~/.claude/skills")
        print(f"\n2. 提交更新:")
        print(f"   cd ~/.claude/skills/[skill-name]")
        print(f"   git add SKILL.md")
        print(f"   git commit -m \"Add GitHub tracking info\"")
        print(f"   git push")

if __name__ == "__main__":
    main()
