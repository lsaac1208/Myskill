#!/usr/bin/env python3
"""
Just 任务运行器 Wrapper
提供 just 命令的 Python 封装接口
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any


class JustRunner:
    """Just 任务运行器的 Python 封装类"""

    def __init__(self, working_dir: Optional[str] = None):
        """
        初始化 Just runner

        Args:
            working_dir: 工作目录，默认为当前目录
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()
        self._check_installed()
        self._find_justfile()

    def _check_installed(self) -> None:
        """检查 just 是否已安装"""
        try:
            subprocess.run(
                ["just", "--version"],
                capture_output=True,
                check=True,
                text=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "Just 未安装。请访问 https://github.com/casey/just 安装。"
            )

    def _find_justfile(self) -> None:
        """查找 justfile 文件"""
        justfile_path = self.working_dir / "justfile"
        if not justfile_path.exists():
            # 尝试在上级目录查找
            current = self.working_dir
            while current != current.parent:
                if (current / "justfile").exists():
                    self.working_dir = current
                    return
                current = current.parent
            raise FileNotFoundError(
                f"未找到 justfile 文件。当前目录: {self.working_dir}"
            )

    def _run_command(
        self,
        args: List[str],
        capture_output: bool = True,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """
        执行 just 命令

        Args:
            args: 命令参数列表
            capture_output: 是否捕获输出
            check: 是否检查返回码

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd = ["just"] + args
        try:
            return subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                cwd=self.working_dir,
                check=check
            )
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {' '.join(cmd)}", file=sys.stderr)
            if e.stderr:
                print(f"错误: {e.stderr}", file=sys.stderr)
            raise

    def list_recipes(self) -> List[Dict[str, Any]]:
        """
        列出所有可用的 recipes

        Returns:
            Recipe 列表，每个包含名称、文档等信息
        """
        result = self._run_command(["--list"], check=False)

        recipes = []
        for line in result.stdout.strip().split('\n'):
            if line.strip() and not line.startswith('Available'):
                parts = line.split(maxsplit=1)
                if len(parts) >= 1:
                    name = parts[0].rstrip(':')
                    doc = parts[1] if len(parts) > 1 else ""
                    recipes.append({
                        "name": name,
                        "documentation": doc
                    })

        return recipes

    def run(
        self,
        recipe: str,
        args: Optional[List[str]] = None,
        variables: Optional[Dict[str, str]] = None
    ) -> subprocess.CompletedProcess:
        """
        运行指定的 recipe

        Args:
            recipe: Recipe 名称
            args: Recipe 参数列表
            variables: 变量字典

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd_args = []

        # 添加变量
        if variables:
            for key, value in variables.items():
                cmd_args.extend([f"{key}={value}"])

        # 添加 recipe 名称
        cmd_args.append(recipe)

        # 添加 recipe 参数
        if args:
            cmd_args.extend(args)

        return self._run_command(cmd_args, capture_output=False)

    def run_with_output(
        self,
        recipe: str,
        args: Optional[List[str]] = None,
        variables: Optional[Dict[str, str]] = None
    ) -> str:
        """
        运行 recipe 并返回输出

        Args:
            recipe: Recipe 名称
            args: Recipe 参数列表
            variables: 变量字典

        Returns:
            命令输出
        """
        result = self.run(recipe, args, variables)
        return result.stdout

    def show_recipe(self, recipe: str) -> str:
        """
        显示 recipe 的内容

        Args:
            recipe: Recipe 名称

        Returns:
            Recipe 内容
        """
        result = self._run_command(["--show", recipe])
        return result.stdout

    def get_variables(self) -> Dict[str, str]:
        """
        获取 justfile 中定义的所有变量

        Returns:
            变量字典
        """
        result = self._run_command(["--variables"], check=False)
        variables = {}
        for line in result.stdout.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                variables[key.strip()] = value.strip()
        return variables

    def evaluate(self, expression: str) -> str:
        """
        计算表达式

        Args:
            expression: 要计算的表达式

        Returns:
            计算结果
        """
        result = self._run_command(["--evaluate", expression])
        return result.stdout.strip()

    def init(self, directory: Optional[str] = None) -> str:
        """
        初始化一个新的 justfile

        Args:
            directory: 目标目录

        Returns:
            初始化结果
        """
        args = ["--init"]
        if directory:
            args.append(directory)

        result = self._run_command(args, capture_output=False)
        return result.stdout

    def format_justfile(self) -> str:
        """
        格式化 justfile

        Returns:
            格式化结果
        """
        result = self._run_command(["--format"], capture_output=False)
        return result.stdout

    def validate_justfile(self) -> bool:
        """
        验证 justfile 语法

        Returns:
            是否有效
        """
        result = self._run_command(["--validate"], check=False)
        return result.returncode == 0

    def get_justfile_path(self) -> Path:
        """
        获取 justfile 路径

        Returns:
            justfile 文件路径
        """
        return self.working_dir / "justfile"

    def read_justfile(self) -> str:
        """
        读取 justfile 内容

        Returns:
            justfile 内容
        """
        justfile_path = self.get_justfile_path()
        with open(justfile_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_justfile(self, content: str) -> None:
        """
        写入 justfile 内容

        Args:
            content: justfile 内容
        """
        justfile_path = self.get_justfile_path()
        with open(justfile_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def dry_run(
        self,
        recipe: str,
        args: Optional[List[str]] = None
    ) -> str:
        """
        干运行（显示将要执行的命令但不实际执行）

        Args:
            recipe: Recipe 名称
            args: Recipe 参数列表

        Returns:
            将要执行的命令
        """
        cmd_args = ["--dry-run", recipe]
        if args:
            cmd_args.extend(args)

        result = self._run_command(cmd_args)
        return result.stdout

    def get_info(self) -> Dict[str, Any]:
        """
        获取 Just 的版本信息

        Returns:
            版本信息字典
        """
        result = self._run_command(["--version"])
        version_info = {}
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                version_info['version'] = line.strip()
        return version_info


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Just 任务运行器 Python Wrapper")
    parser.add_argument("--dir", help="工作目录")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 列出 recipes
    list_parser = subparsers.add_parser("list", help="列出所有可用的 recipes")

    # 运行 recipe
    run_parser = subparsers.add_parser("run", help="运行指定的 recipe")
    run_parser.add_argument("recipe", help="Recipe 名称")
    run_parser.add_argument("args", nargs="*", help="Recipe 参数")
    run_parser.add_argument("--set", action="append", help="设置变量 (key=value)")

    # 显示 recipe
    show_parser = subparsers.add_parser("show", help="显示 recipe 内容")
    show_parser.add_argument("recipe", help="Recipe 名称")

    # 获取变量
    variables_parser = subparsers.add_parser("variables", help="获取所有变量")

    # 计算
    eval_parser = subparsers.add_parser("evaluate", help="计算表达式")
    eval_parser.add_argument("expression", help="要计算的表达式")

    # 初始化
    init_parser = subparsers.add_parser("init", help="初始化新的 justfile")
    init_parser.add_argument("--dir", help="目标目录")

    # 格式化
    format_parser = subparsers.add_parser("format", help="格式化 justfile")

    # 验证
    validate_parser = subparsers.add_parser("validate", help="验证 justfile")

    # 干运行
    dryrun_parser = subparsers.add_parser("dry-run", help="干运行")
    dryrun_parser.add_argument("recipe", help="Recipe 名称")
    dryrun_parser.add_argument("args", nargs="*", help="Recipe 参数")

    # 信息
    info_parser = subparsers.add_parser("info", help="获取版本信息")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    just = JustRunner(args.dir)

    try:
        if args.command == "list":
            recipes = just.list_recipes()
            print("可用的 Recipes:")
            for recipe in recipes:
                print(f"  {recipe['name']}: {recipe['documentation']}")

        elif args.command == "run":
            variables = {}
            if args.set:
                for item in args.set:
                    if '=' in item:
                        key, value = item.split('=', 1)
                        variables[key] = value

            just.run(args.recipe, args.args, variables)

        elif args.command == "show":
            content = just.show_recipe(args.recipe)
            print(content)

        elif args.command == "variables":
            variables = just.get_variables()
            print(json.dumps(variables, indent=2, ensure_ascii=False))

        elif args.command == "evaluate":
            result = just.evaluate(args.expression)
            print(result)

        elif args.command == "init":
            result = just.init(getattr(args, 'dir', None))
            print(result)

        elif args.command == "format":
            result = just.format_justfile()
            print(result)

        elif args.command == "validate":
            is_valid = just.validate_justfile()
            if is_valid:
                print("✓ justfile 语法正确")
            else:
                print("✗ justfile 语法错误")
                sys.exit(1)

        elif args.command == "dry-run":
            result = just.dry_run(args.recipe, args.args)
            print(result)

        elif args.command == "info":
            info = just.get_info()
            print(json.dumps(info, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
