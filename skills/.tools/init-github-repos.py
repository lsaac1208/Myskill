#!/usr/bin/env python3
"""
为自定义 Skills 创建 GitHub 仓库的辅助工具

此脚本帮助您为每个自定义 Skill 准备 GitHub 仓库所需的文件：
1. 初始化 Git 仓库
2. 创建 README.md
3. 创建 .gitignore
4. 创建 LICENSE
5. 提供创建远程仓库的命令
"""

import os
import sys
from pathlib import Path
from datetime import datetime

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

# 许可证模板
MIT_LICENSE = """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

GITIGNORE_TEMPLATE = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
.cache/

# Build
dist/
build/
*.egg-info/
"""

def read_skill_metadata(skill_name):
    """读取 Skill 的元数据"""
    skill_md = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text()
    lines = content.split('\n')

    metadata = {}
    in_frontmatter = False
    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                break
        elif in_frontmatter and ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()

    return metadata

def create_readme(skill_name, metadata):
    """创建 README.md"""
    description = metadata.get('description', f'{skill_name} skill')
    version = metadata.get('version', '1.0.0')

    readme = f"""# {skill_name}

{description}

## 📦 安装

将此 Skill 添加到您的 Claude Code Skills 目录：

```bash
cd ~/.claude/skills
git clone https://github.com/YOUR_USERNAME/{skill_name}.git
```

## 🚀 使用

此 Skill 会在以下场景自动激活：

{description.split(' - ')[1] if ' - ' in description else '请查看 SKILL.md 了解详细触发场景'}

详细使用方法请参考 [SKILL.md](SKILL.md)

## 📋 依赖

{metadata.get('dependencies', '[]')}

## 📝 版本

当前版本: v{version}

查看 [SKILL.md](SKILL.md) 了解完整的更新日志。

## 📄 许可证

{metadata.get('license', 'MIT')}

## 🔗 相关资源

- [Claude Code](https://github.com/anthropics/claude-code)
- [Skills 文档](https://docs.anthropic.com/claude/docs/skills)

---

**创建日期**: {metadata.get('created_at', datetime.now().strftime('%Y-%m-%d'))}
**最后更新**: {metadata.get('updated_at', datetime.now().strftime('%Y-%m-%d'))}
"""
    return readme

def init_git_repo(skill_name):
    """初始化 Git 仓库并创建必要文件"""
    skill_dir = SKILLS_DIR / skill_name

    if not skill_dir.exists():
        print(f"❌ Skill 目录不存在: {skill_name}")
        return False

    print(f"\n{'='*60}")
    print(f"处理 Skill: {skill_name}")
    print(f"{'='*60}")

    # 读取元数据
    metadata = read_skill_metadata(skill_name)
    if not metadata:
        print(f"⚠️  无法读取 {skill_name} 的元数据")
        return False

    # 检查是否已经是 Git 仓库
    git_dir = skill_dir / ".git"
    if git_dir.exists():
        print(f"✅ 已经是 Git 仓库")
    else:
        print(f"📦 初始化 Git 仓库...")
        os.system(f'cd "{skill_dir}" && git init')

    # 创建 README.md
    readme_path = skill_dir / "README.md"
    if not readme_path.exists():
        print(f"📝 创建 README.md...")
        readme_path.write_text(create_readme(skill_name, metadata))
    else:
        print(f"✅ README.md 已存在")

    # 创建 .gitignore
    gitignore_path = skill_dir / ".gitignore"
    if not gitignore_path.exists():
        print(f"📝 创建 .gitignore...")
        gitignore_path.write_text(GITIGNORE_TEMPLATE)
    else:
        print(f"✅ .gitignore 已存在")

    # 创建 LICENSE（如果是 MIT）
    license_path = skill_dir / "LICENSE"
    if not license_path.exists() and 'MIT' in metadata.get('license', ''):
        print(f"📝 创建 LICENSE...")
        license_text = MIT_LICENSE.format(
            year=datetime.now().year,
            author="YOUR_NAME"  # 用户需要替换
        )
        license_path.write_text(license_text)
    else:
        print(f"✅ LICENSE 已存在或不适用")

    # 提供 Git 命令
    print(f"\n📋 下一步操作：")
    print(f"\n1. 在 GitHub 上创建仓库:")
    print(f"   https://github.com/new")
    print(f"   仓库名: {skill_name}")
    print(f"   描述: {metadata.get('description', '')[:100]}")
    print(f"\n2. 执行以下命令:")
    print(f"   cd ~/.claude/skills/{skill_name}")
    print(f"   git add .")
    print(f"   git commit -m \"Initial commit: {skill_name} v{metadata.get('version', '1.0.0')}\"")
    print(f"   git branch -M main")
    print(f"   git remote add origin https://github.com/YOUR_USERNAME/{skill_name}.git")
    print(f"   git push -u origin main")
    print(f"\n3. 更新 SKILL.md 的 frontmatter:")
    print(f"   添加: github_url: https://github.com/YOUR_USERNAME/{skill_name}")
    print(f"   添加: github_hash: $(git rev-parse HEAD)")

    return True

def main():
    print("🚀 自定义 Skills GitHub 仓库初始化工具")
    print("="*60)

    if len(sys.argv) > 1:
        # 处理指定的 Skill
        skill_name = sys.argv[1]
        if skill_name in CUSTOM_SKILLS:
            init_git_repo(skill_name)
        else:
            print(f"❌ 未知的 Skill: {skill_name}")
            print(f"可用的 Skills: {', '.join(CUSTOM_SKILLS)}")
    else:
        # 处理所有自定义 Skills
        print(f"将为以下 {len(CUSTOM_SKILLS)} 个 Skills 准备 GitHub 仓库：")
        for skill in CUSTOM_SKILLS:
            print(f"  - {skill}")

        print(f"\n按 Enter 继续，或 Ctrl+C 取消...")
        input()

        success_count = 0
        for skill_name in CUSTOM_SKILLS:
            if init_git_repo(skill_name):
                success_count += 1

        print(f"\n{'='*60}")
        print(f"✅ 完成! 成功处理 {success_count}/{len(CUSTOM_SKILLS)} 个 Skills")
        print(f"{'='*60}")
        print(f"\n📝 后续步骤:")
        print(f"1. 在 GitHub 上为每个 Skill 创建仓库")
        print(f"2. 执行上面显示的 git 命令")
        print(f"3. 更新每个 SKILL.md 的 frontmatter")
        print(f"4. 运行 skill-manager 验证更新")

if __name__ == "__main__":
    main()
