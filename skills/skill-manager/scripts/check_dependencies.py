#!/usr/bin/env python3
"""
Skills 依赖验证工具

检查所有 Skills 的依赖是否已安装，并提供安装建议
"""

import os
import sys
import yaml
import json
import subprocess
import shutil
from pathlib import Path
from collections import defaultdict

class DependencyChecker:
    """依赖检查器"""

    def __init__(self, skills_root):
        self.skills_root = Path(skills_root)
        self.all_dependencies = defaultdict(list)  # dep -> [skills]
        self.missing_dependencies = defaultdict(list)
        self.installed_dependencies = set()

    def scan_all_dependencies(self):
        """扫描所有 Skills 的依赖"""
        for item in self.skills_root.iterdir():
            if not item.is_dir() or item.name.startswith('.'):
                continue

            skill_md = item / "SKILL.md"
            if not skill_md.exists():
                continue

            try:
                metadata = self.parse_frontmatter(skill_md)
                skill_name = metadata.get('name', item.name)

                if 'dependencies' in metadata:
                    deps = self.parse_dependencies(metadata['dependencies'])
                    for dep in deps:
                        self.all_dependencies[dep].append(skill_name)
            except:
                pass

    def parse_frontmatter(self, skill_md):
        """解析 frontmatter"""
        content = skill_md.read_text()
        parts = content.split('---')
        if len(parts) < 3:
            return {}
        return yaml.safe_load(parts[1])

    def parse_dependencies(self, dependencies):
        """解析依赖列表"""
        if isinstance(dependencies, str):
            try:
                dependencies = eval(dependencies)
            except:
                return []

        if not isinstance(dependencies, list):
            return []

        return dependencies

    def check_all_dependencies(self):
        """检查所有依赖的安装状态"""
        for dep in self.all_dependencies.keys():
            if self.is_installed(dep):
                self.installed_dependencies.add(dep)
            else:
                skills = self.all_dependencies[dep]
                self.missing_dependencies[dep] = skills

    def is_installed(self, dep):
        """检查依赖是否已安装"""
        # 移除版本号
        dep_name = dep.split('>=')[0].split('==')[0].split('<')[0].strip()

        # 检查命令行工具
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
            pass

        # 检查常见的别名
        aliases = {
            'python3': 'python',
            'node': 'nodejs',
            'gh': 'github-cli'
        }

        if dep_name in aliases:
            return shutil.which(aliases[dep_name]) is not None

        return False

    def get_install_command(self, dep):
        """获取依赖的安装命令"""
        dep_name = dep.split('>=')[0].split('==')[0].split('<')[0].strip()

        # Python 包
        python_packages = ['pandas', 'openpyxl', 'docx', 'pptx', 'playwright',
                          'PyYAML', 'requests', 'beautifulsoup4', 'feedparser',
                          'jieba', 'ddgs', 'googlesearch-python', 'defusedxml']

        if dep_name in python_packages or dep_name.startswith('python-'):
            return f"pip3 install {dep}"

        # 命令行工具
        cli_tools = {
            'gh': 'brew install gh',
            'task': 'brew install go-task/tap/go-task',
            'just': 'brew install just',
            'zx': 'npm install -g zx',
            'pandoc': 'brew install pandoc',
            'ffmpeg': 'brew install ffmpeg',
            'libreoffice': 'brew install --cask libreoffice'
        }

        if dep_name in cli_tools:
            return cli_tools[dep_name]

        # 默认建议
        return f"# 请手动安装: {dep_name}"

    def print_report(self):
        """打印依赖报告"""
        print("\n" + "="*60)
        print("Skills 依赖检查报告")
        print("="*60)

        total_deps = len(self.all_dependencies)
        installed = len(self.installed_dependencies)
        missing = len(self.missing_dependencies)

        print(f"\n📊 总体统计:")
        print(f"  总依赖数: {total_deps}")
        print(f"  ✅ 已安装: {installed}")
        print(f"  ❌ 未安装: {missing}")

        if self.installed_dependencies:
            print(f"\n✅ 已安装的依赖 ({len(self.installed_dependencies)}):")
            for dep in sorted(self.installed_dependencies):
                skills = self.all_dependencies[dep]
                print(f"  - {dep} (用于 {len(skills)} 个 Skills)")

        if self.missing_dependencies:
            print(f"\n❌ 未安装的依赖 ({len(self.missing_dependencies)}):")
            for dep, skills in sorted(self.missing_dependencies.items()):
                print(f"\n  {dep}")
                print(f"    需要此依赖的 Skills: {', '.join(skills)}")
                print(f"    安装命令: {self.get_install_command(dep)}")

        if missing > 0:
            print(f"\n💡 建议:")
            print(f"  1. 安装缺失的依赖以确保 Skills 正常工作")
            print(f"  2. 如果某些依赖不需要，可以从 SKILL.md 中移除")
            print(f"  3. 运行 'pip3 install <package>' 安装 Python 包")
            print(f"  4. 运行 'brew install <tool>' 安装命令行工具")

        print("\n" + "="*60)

    def generate_install_script(self):
        """生成安装脚本"""
        script = "#!/usr/bin/env bash\n"
        script += "# Skills 依赖自动安装脚本\n"
        script += "# 生成时间: " + str(Path.cwd()) + "\n\n"
        script += "set -e\n\n"

        if not self.missing_dependencies:
            script += "echo '✅ 所有依赖都已安装！'\n"
            return script

        script += "echo '开始安装缺失的依赖...'\n\n"

        for dep in sorted(self.missing_dependencies.keys()):
            cmd = self.get_install_command(dep)
            if not cmd.startswith('#'):
                script += f"echo '安装 {dep}...'\n"
                script += f"{cmd}\n\n"

        script += "echo '✅ 依赖安装完成！'\n"

        return script

def main():
    if len(sys.argv) < 2:
        print("用法: python check_dependencies.py <skills_dir> [--install-script]")
        sys.exit(1)

    skills_dir = sys.argv[1]
    generate_script = '--install-script' in sys.argv

    checker = DependencyChecker(skills_dir)

    print("🔍 扫描 Skills 依赖...")
    checker.scan_all_dependencies()

    print("✅ 检查依赖安装状态...")
    checker.check_all_dependencies()

    if generate_script:
        script = checker.generate_install_script()
        script_path = Path(skills_dir) / ".tools" / "install_dependencies.sh"
        script_path.parent.mkdir(exist_ok=True)
        script_path.write_text(script)
        os.chmod(script_path, 0o755)
        print(f"\n✅ 安装脚本已生成: {script_path}")
    else:
        checker.print_report()

if __name__ == "__main__":
    main()
