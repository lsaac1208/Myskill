#!/usr/bin/env python3
"""
Task (Go Task) 任务运行器 Wrapper
提供 Task 命令的 Python 封装接口
"""

import subprocess
import json
import sys
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any


class TaskRunner:
    """Task (Go Task) 任务运行器的 Python 封装类"""

    def __init__(self, working_dir: Optional[str] = None):
        """
        初始化 Task runner

        Args:
            working_dir: 工作目录，默认为当前目录
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()
        self._check_installed()
        self._find_taskfile()

    def _check_installed(self) -> None:
        """检查 task 是否已安装"""
        try:
            subprocess.run(
                ["task", "--version"],
                capture_output=True,
                check=True,
                text=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "Task 未安装。请访问 https://taskfile.dev 安装。\n"
                "安装方法: go install github.com/go-task/task/v3/cmd/task@latest"
            )

    def _find_taskfile(self) -> None:
        """查找 Taskfile 文件"""
        taskfile_names = ['Taskfile.yml', 'Taskfile.yaml', 'Taskfile.dist.yml']
        taskfile_path = None

        for name in taskfile_names:
            path = self.working_dir / name
            if path.exists():
                taskfile_path = path
                break

        if not taskfile_path:
            # 尝试在上级目录查找
            current = self.working_dir
            while current != current.parent:
                for name in taskfile_names:
                    if (current / name).exists():
                        self.working_dir = current
                        self.taskfile_path = current / name
                        return
                current = current.parent
            raise FileNotFoundError(
                f"未找到 Taskfile 文件。当前目录: {self.working_dir}"
            )

        self.taskfile_path = taskfile_path

    def _run_command(
        self,
        args: List[str],
        capture_output: bool = True,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """
        执行 task 命令

        Args:
            args: 命令参数列表
            capture_output: 是否捕获输出
            check: 是否检查返回码

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd = ["task"] + args
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

    def list_tasks(self) -> List[Dict[str, Any]]:
        """
        列出所有可用的任务

        Returns:
            任务列表
        """
        result = self._run_command(["--list", "--json"])
        try:
            tasks_data = json.loads(result.stdout)
            tasks = []
            for task in tasks_data.get("tasks", []):
                tasks.append({
                    "name": task.get("name", ""),
                    "description": task.get("desc", ""),
                    "source": task.get("file", "")
                })
            return tasks
        except json.JSONDecodeError:
            # 如果 JSON 解析失败，回退到文本解析
            return self._parse_task_list_text(result.stdout)

    def _parse_task_list_text(self, output: str) -> List[Dict[str, Any]]:
        """解析文本格式的任务列表"""
        tasks = []
        for line in output.strip().split('\n'):
            if line.strip() and '*' in line:
                parts = line.split('*', 1)
                if len(parts) >= 1:
                    name = parts[0].strip()
                    desc = parts[1].strip() if len(parts) > 1 else ""
                    tasks.append({
                        "name": name,
                        "description": desc
                    })
        return tasks

    def run_task(
        self,
        task_name: str,
        args: Optional[List[str]] = None,
        global_args: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """
        运行指定的任务

        Args:
            task_name: 任务名称
            args: 任务参数列表
            global_args: 全局参数

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd_args = []

        # 添加全局参数
        if global_args:
            cmd_args.extend(global_args)

        # 添加任务名称
        cmd_args.append(task_name)

        # 添加任务参数
        if args:
            cmd_args.extend(args)

        return self._run_command(cmd_args, capture_output=False)

    def get_task_info(self, task_name: str) -> Dict[str, Any]:
        """
        获取任务详细信息

        Args:
            task_name: 任务名称

        Returns:
            任务信息字典
        """
        # 读取 Taskfile
        try:
            with open(self.taskfile_path, 'r', encoding='utf-8') as f:
                taskfile = yaml.safe_load(f)

            tasks = taskfile.get('tasks', {})
            if task_name in tasks:
                task_info = tasks[task_name]
                return {
                    "name": task_name,
                    "description": task_info.get('desc', ''),
                    "summary": task_info.get('summary', ''),
                    "dependencies": task_info.get('deps', []),
                    "commands": task_info.get('cmds', []),
                    "variables": task_info.get('vars', {})
                }
        except Exception:
            pass

        return {"name": task_name, "description": "未找到任务信息"}

    def get_taskfile_content(self) -> Dict[str, Any]:
        """
        获取 Taskfile 内容

        Returns:
            Taskfile 字典
        """
        try:
            with open(self.taskfile_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"读取 Taskfile 失败: {e}")

    def get_variables(self) -> Dict[str, str]:
        """
        获取 Taskfile 中定义的变量

        Returns:
            变量字典
        """
        taskfile = self.get_taskfile_content()
        return taskfile.get('vars', {})

    def set_variable(
        self,
        name: str,
        value: str,
        task_name: Optional[str] = None
    ) -> None:
        """
        设置变量（运行时）

        Args:
            name: 变量名
            value: 变量值
            task_name: 任务名称（可选，用于特定任务的变量）
        """
        # 运行时变量通过命令行参数传递
        pass

    def dry_run(
        self,
        task_name: str,
        args: Optional[List[str]] = None
    ) -> str:
        """
        干运行（显示将要执行的命令）

        Args:
            task_name: 任务名称
            args: 任务参数列表

        Returns:
            将要执行的命令
        """
        cmd_args = ["--dry", task_name]
        if args:
            cmd_args.extend(args)

        result = self._run_command(cmd_args)
        return result.stdout

    def watch_task(
        self,
        task_name: str,
        args: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """
        监视模式运行任务

        Args:
            task_name: 任务名称
            args: 任务参数列表

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd_args = ["--watch", task_name]
        if args:
            cmd_args.extend(args)

        return self._run_command(cmd_args, capture_output=False)

    def force_task(
        self,
        task_name: str,
        args: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """
        强制执行任务（即使已是最新的）

        Args:
            task_name: 任务名称
            args: 任务参数列表

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd_args = ["--force", task_name]
        if args:
            cmd_args.extend(args)

        return self._run_command(cmd_args, capture_output=False)

    def get_version(self) -> str:
        """
        获取 Task 版本

        Returns:
            版本信息
        """
        result = self._run_command(["--version"])
        return result.stdout.strip()

    def init_taskfile(
        self,
        directory: Optional[str] = None
    ) -> str:
        """
        初始化新的 Taskfile

        Args:
            directory: 目标目录

        Returns:
            初始化结果
        """
        target_dir = Path(directory) if directory else self.working_dir
        taskfile_path = target_dir / "Taskfile.yml"

        # 默认 Taskfile 模板
        default_taskfile = """# https://taskfile.dev

version: '3'

vars:
  GREETING: Hello, Taskfile!

tasks:
  default:
    cmds:
      - echo "{{.GREETING}}"
    silent: true

  build:
    desc: Build the project
    cmds:
      - echo "Building..."

  test:
    desc: Run tests
    cmds:
      - echo "Testing..."
"""

        with open(taskfile_path, 'w', encoding='utf-8') as f:
            f.write(default_taskfile)

        return f"✓ 创建 Taskfile: {taskfile_path}"

    def validate_taskfile(self) -> bool:
        """
        验证 Taskfile 语法

        Returns:
            是否有效
        """
        try:
            self.get_taskfile_content()
            return True
        except Exception:
            return False

    def get_task_status(self, task_name: str) -> Dict[str, Any]:
        """
        获取任务状态（是否需要运行）

        Args:
            task_name: 任务名称

        Returns:
            任务状态字典
        """
        # Task 没有内置的状态命令，这里提供基本实现
        task_info = self.get_task_info(task_name)
        return {
            "name": task_name,
            "exists": bool(task_info.get("description")),
            "up_to_date": False  # 默认需要运行
        }


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Task (Go Task) Python Wrapper")
    parser.add_argument("--dir", help="工作目录")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 列出任务
    list_parser = subparsers.add_parser("list", help="列出所有可用的任务")

    # 运行任务
    run_parser = subparsers.add_parser("run", help="运行指定的任务")
    run_parser.add_argument("task", help="任务名称")
    run_parser.add_argument("args", nargs="*", help="任务参数")
    run_parser.add_argument("--watch", action="store_true", help="监视模式")
    run_parser.add_argument("--force", action="store_true", help="强制执行")
    run_parser.add_argument("--dry", action="store_true", help="干运行")

    # 获取任务信息
    info_parser = subparsers.add_parser("info", help="获取任务详细信息")
    info_parser.add_argument("task", help="任务名称")

    # 获取变量
    variables_parser = subparsers.add_parser("variables", help="获取所有变量")

    # 初始化
    init_parser = subparsers.add_parser("init", help="初始化新的 Taskfile")
    init_parser.add_argument("--dir", help="目标目录")

    # 验证
    validate_parser = subparsers.add_parser("validate", help="验证 Taskfile")

    # 版本
    version_parser = subparsers.add_parser("version", help="获取版本信息")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    task = TaskRunner(args.dir)

    try:
        if args.command == "list":
            tasks = task.list_tasks()
            print("可用的任务:")
            for t in tasks:
                desc = t.get('description', t.get('desc', ''))
                print(f"  {t['name']}: {desc}")

        elif args.command == "run":
            global_args = []
            if args.watch:
                global_args.append("--watch")
            if args.force:
                global_args.append("--force")
            if args.dry:
                global_args.append("--dry")

            if args.dry:
                result = task.dry_run(args.task, args.args)
                print(result)
            else:
                task.run_task(args.task, args.args, global_args)

        elif args.command == "info":
            info = task.get_task_info(args.task)
            print(json.dumps(info, indent=2, ensure_ascii=False))

        elif args.command == "variables":
            variables = task.get_variables()
            print(json.dumps(variables, indent=2, ensure_ascii=False))

        elif args.command == "init":
            result = task.init_taskfile(getattr(args, 'dir', None))
            print(result)

        elif args.command == "validate":
            is_valid = task.validate_taskfile()
            if is_valid:
                print("✓ Taskfile 语法正确")
            else:
                print("✗ Taskfile 语法错误")
                sys.exit(1)

        elif args.command == "version":
            version = task.get_version()
            print(version)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
