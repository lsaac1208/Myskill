#!/usr/bin/env python3
"""
Skills 健康检查工具

检查所有 Skills 的完整性、元数据、依赖等
"""

import os
import sys
import yaml
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class SkillHealthChecker:
    """Skills 健康检查器"""

    def __init__(self, skills_root):
        self.skills_root = Path(skills_root)
        self.issues = []
        self.warnings = []
        self.stats = {
            'total': 0,
            'healthy': 0,
            'with_issues': 0,
            'with_warnings': 0
        }

    def check_all_skills(self):
        """检查所有 Skills"""
        results = []

        if not self.skills_root.exists():
            print(f"❌ Skills 目录不存在: {self.skills_root}")
            return results

        for item in self.skills_root.iterdir():
            if not item.is_dir() or item.name.startswith('.'):
                continue

            skill_result = self.check_skill(item)
            if skill_result:
                results.append(skill_result)
                self.stats['total'] += 1

                if skill_result['issues']:
                    self.stats['with_issues'] += 1
                elif skill_result['warnings']:
                    self.stats['with_warnings'] += 1
                else:
                    self.stats['healthy'] += 1

        return results

    def check_skill(self, skill_dir):
        """检查单个 Skill"""
        skill_name = skill_dir.name
        result = {
            'name': skill_name,
            'path': str(skill_dir),
            'issues': [],
            'warnings': [],
            'metadata': {},
            'health_score': 100
        }

        # 检查 SKILL.md 是否存在
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            result['issues'].append("缺少 SKILL.md 文件")
            result['health_score'] -= 50
            return result

        # 解析 frontmatter
        try:
            metadata = self.parse_frontmatter(skill_md)
            result['metadata'] = metadata
        except Exception as e:
            result['issues'].append(f"无法解析 frontmatter: {e}")
            result['health_score'] -= 30
            return result

        # 检查必需字段
        required_fields = ['name', 'description', 'version', 'entry_point']
        for field in required_fields:
            if field not in metadata:
                result['issues'].append(f"缺少必需字段: {field}")
                result['health_score'] -= 10

        # 检查推荐字段
        recommended_fields = ['created_at', 'updated_at', 'dependencies', 'license']
        for field in recommended_fields:
            if field not in metadata:
                result['warnings'].append(f"缺少推荐字段: {field}")
                result['health_score'] -= 5

        # 检查 entry_point 是否存在
        if 'entry_point' in metadata:
            entry_point = skill_dir / metadata['entry_point']
            if not entry_point.exists():
                result['issues'].append(f"entry_point 文件不存在: {metadata['entry_point']}")
                result['health_score'] -= 15

        # 检查依赖
        if 'dependencies' in metadata:
            dep_issues = self.check_dependencies(metadata['dependencies'])
            if dep_issues:
                result['warnings'].extend(dep_issues)
                result['health_score'] -= len(dep_issues) * 3

        # 检查 GitHub 追踪（如果有）
        if 'github_url' in metadata:
            if 'github_hash' not in metadata:
                result['warnings'].append("有 github_url 但缺少 github_hash")
                result['health_score'] -= 5

        # 检查版本号格式
        if 'version' in metadata:
            if not self.is_valid_version(metadata['version']):
                result['warnings'].append(f"版本号格式不规范: {metadata['version']}")
                result['health_score'] -= 3

        # 检查文档内容
        content = skill_md.read_text()
        if 'TODO' in content:
            result['warnings'].append("文档中包含 TODO 标记")
            result['health_score'] -= 5

        # 确保分数不低于 0
        result['health_score'] = max(0, result['health_score'])

        return result

    def parse_frontmatter(self, skill_md):
        """解析 SKILL.md 的 frontmatter"""
        content = skill_md.read_text()
        parts = content.split('---')

        if len(parts) < 3:
            raise ValueError("无效的 frontmatter 格式")

        return yaml.safe_load(parts[1])

    def check_dependencies(self, dependencies):
        """检查依赖是否已安装"""
        issues = []

        if isinstance(dependencies, str):
            # 处理字符串格式的依赖列表
            try:
                dependencies = eval(dependencies)
            except:
                return [f"无法解析依赖列表: {dependencies}"]

        if not isinstance(dependencies, list):
            return [f"依赖格式错误: {dependencies}"]

        for dep in dependencies:
            if not self.is_dependency_installed(dep):
                issues.append(f"依赖未安装: {dep}")

        return issues

    def is_dependency_installed(self, dep):
        """检查依赖是否已安装"""
        # 移除版本号
        dep_name = dep.split('>=')[0].split('==')[0].split('<')[0].strip()

        # 检查常见的命令行工具
        if shutil.which(dep_name):
            return True

        # 检查 Python 包
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'show', dep_name],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def is_valid_version(self, version):
        """检查版本号是否符合语义化版本规范"""
        import re
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, str(version)))

    def generate_report(self, results):
        """生成健康报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.stats,
            'skills': results
        }

        return report

    def print_report(self, results):
        """打印可读的报告"""
        print("\n" + "="*60)
        print("Skills 健康检查报告")
        print("="*60)
        print(f"\n📊 总体统计:")
        print(f"  总计: {self.stats['total']} 个 Skills")
        print(f"  ✅ 健康: {self.stats['healthy']} 个")
        print(f"  ⚠️  有警告: {self.stats['with_warnings']} 个")
        print(f"  ❌ 有问题: {self.stats['with_issues']} 个")

        # 按健康分数排序
        sorted_results = sorted(results, key=lambda x: x['health_score'])

        print(f"\n📋 详细结果:\n")

        for result in sorted_results:
            score = result['health_score']

            # 根据分数显示不同的图标
            if score >= 90:
                icon = "✅"
            elif score >= 70:
                icon = "⚠️ "
            else:
                icon = "❌"

            print(f"{icon} {result['name']} (健康分数: {score}/100)")

            if result['issues']:
                print(f"   问题:")
                for issue in result['issues']:
                    print(f"     - {issue}")

            if result['warnings']:
                print(f"   警告:")
                for warning in result['warnings']:
                    print(f"     - {warning}")

            print()

        print("="*60)

def main():
    if len(sys.argv) < 2:
        print("用法: python health_check.py <skills_dir> [--json]")
        sys.exit(1)

    skills_dir = sys.argv[1]
    output_json = '--json' in sys.argv

    checker = SkillHealthChecker(skills_dir)
    results = checker.check_all_skills()

    if output_json:
        report = checker.generate_report(results)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        checker.print_report(results)

if __name__ == "__main__":
    main()
