#!/usr/bin/env python3
"""
批量文档更新工具

批量更新所有 Skills 的文档，修复常见问题
"""

import os
import sys
import yaml
import re
from pathlib import Path
from datetime import datetime

class DocumentUpdater:
    """文档更新器"""

    def __init__(self, skills_root):
        self.skills_root = Path(skills_root)
        self.updates = []

    def update_all_skills(self, dry_run=True):
        """更新所有 Skills 的文档"""
        results = []

        for item in self.skills_root.iterdir():
            if not item.is_dir() or item.name.startswith('.'):
                continue

            skill_md = item / "SKILL.md"
            if not skill_md.exists():
                continue

            result = self.update_skill(item, dry_run)
            if result:
                results.append(result)

        return results

    def update_skill(self, skill_dir, dry_run=True):
        """更新单个 Skill 的文档"""
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        result = {
            'name': skill_name,
            'path': str(skill_md),
            'changes': []
        }

        try:
            content = skill_md.read_text()
            original_content = content

            # 解析 frontmatter
            parts = content.split('---')
            if len(parts) < 3:
                result['changes'].append("跳过: 无效的 frontmatter 格式")
                return result

            frontmatter = yaml.safe_load(parts[1])
            body = '---'.join(parts[2:])

            # 更新 updated_at
            if 'updated_at' not in frontmatter or frontmatter['updated_at'] != datetime.now().strftime('%Y-%m-%d'):
                old_date = frontmatter.get('updated_at', '未设置')
                frontmatter['updated_at'] = datetime.now().strftime('%Y-%m-%d')
                result['changes'].append(f"更新 updated_at: {old_date} -> {frontmatter['updated_at']}")

            # 标准化 entry_point
            if 'entry_point' in frontmatter:
                entry_point = frontmatter['entry_point']
                if entry_point.endswith('/'):
                    # 尝试找到实际的入口文件
                    entry_dir = skill_dir / entry_point
                    if entry_dir.exists() and entry_dir.is_dir():
                        # 查找常见的入口文件
                        for candidate in ['main.py', 'wrapper.py', 'index.py', '__init__.py']:
                            candidate_path = entry_dir / candidate
                            if candidate_path.exists():
                                new_entry = str(Path(entry_point) / candidate)
                                frontmatter['entry_point'] = new_entry
                                result['changes'].append(f"修正 entry_point: {entry_point} -> {new_entry}")
                                break

            # 移除 TODO 标记（可选）
            if 'TODO' in body:
                todo_count = body.count('TODO')
                result['changes'].append(f"警告: 文档中包含 {todo_count} 个 TODO 标记")

            # 重新构建文档
            if result['changes']:
                # 重新构建 frontmatter
                ordered_fields = [
                    'name', 'description', 'github_url', 'github_hash', 'version',
                    'created_at', 'updated_at', 'entry_point', 'dependencies', 'license'
                ]

                new_frontmatter = "---\n"
                for field in ordered_fields:
                    if field in frontmatter:
                        value = frontmatter[field]
                        new_frontmatter += f"{field}: {value}\n"
                new_frontmatter += "---"

                new_content = new_frontmatter + body

                if not dry_run:
                    skill_md.write_text(new_content)
                    result['changes'].append("✅ 已保存更改")
                else:
                    result['changes'].append("🔍 预览模式（未保存）")

        except Exception as e:
            result['changes'].append(f"错误: {e}")

        return result if result['changes'] else None

    def print_report(self, results, dry_run=True):
        """打印更新报告"""
        print("\n" + "="*60)
        print("批量文档更新报告")
        print("="*60)

        if dry_run:
            print("\n⚠️  预览模式 - 未实际修改文件")
        else:
            print("\n✅ 已应用更改")

        print(f"\n处理了 {len(results)} 个 Skills:\n")

        for result in results:
            print(f"📄 {result['name']}")
            for change in result['changes']:
                print(f"   {change}")
            print()

        print("="*60)

        if dry_run:
            print("\n💡 提示: 使用 --apply 参数应用更改")

def main():
    if len(sys.argv) < 2:
        print("用法: python batch_update.py <skills_dir> [--apply]")
        print("\n选项:")
        print("  --apply    实际应用更改（默认为预览模式）")
        sys.exit(1)

    skills_dir = sys.argv[1]
    dry_run = '--apply' not in sys.argv

    updater = DocumentUpdater(skills_dir)

    print("🔍 扫描 Skills 文档...")
    results = updater.update_all_skills(dry_run)

    updater.print_report(results, dry_run)

if __name__ == "__main__":
    main()
