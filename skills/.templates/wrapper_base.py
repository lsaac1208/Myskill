#!/usr/bin/env python3
"""
GitHub Skills Wrapper 基类模板

为 GitHub 包装型 Skills 提供通用的基类和工具函数
"""

import subprocess
import sys
import shutil
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod


class SkillWrapperBase(ABC):
    """
    Skill Wrapper 基类

    提供通用的功能：
    - 依赖检查
    - 命令执行
    - 错误处理
    - 输出格式化
    """

    def __init__(self, tool_name: str, install_url: Optional[str] = None):
        """
        初始化 Wrapper

        Args:
            tool_name: 工具命令名称
            install_url: 安装指南 URL
        """
        self.tool_name = tool_name
        self.install_url = install_url or f"https://github.com/{tool_name}"
        self._check_installed()

    def _check_installed(self) -> None:
        """检查工具是否已安装"""
        if not shutil.which(self.tool_name):
            error_msg = f"{self.tool_name} 未安装。"
            if self.install_url:
                error_msg += f"\n请访问 {self.install_url} 安装。"
            raise RuntimeError(error_msg)

    def _run_command(
        self,
        args: List[str],
        capture_output: bool = True,
        check: bool = True,
        **kwargs
    ) -> subprocess.CompletedProcess:
        """
        执行命令

        Args:
            args: 命令参数列表
            capture_output: 是否捕获输出
            check: 是否检查返回码
            **kwargs: 传递给 subprocess.run 的其他参数

        Returns:
            subprocess.CompletedProcess 对象

        Raises:
            subprocess.CalledProcessError: 命令执行失败
        """
        cmd = [self.tool_name] + args

        try:
            return subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=check,
                **kwargs
            )
        except subprocess.CalledProcessError as e:
            self._handle_error(cmd, e)
            raise

    def _handle_error(
        self,
        cmd: List[str],
        error: subprocess.CalledProcessError
    ) -> None:
        """
        处理命令执行错误

        Args:
            cmd: 执行的命令
            error: 捕获的错误
        """
        print(f"❌ 命令执行失败: {' '.join(cmd)}", file=sys.stderr)
        if error.stderr:
            print(f"错误信息: {error.stderr}", file=sys.stderr)
        if error.returncode:
            print(f"退出码: {error.returncode}", file=sys.stderr)

    def get_version(self) -> str:
        """
        获取工具版本

        Returns:
            版本字符串
        """
        try:
            result = self._run_command(["--version"])
            return result.stdout.strip()
        except:
            return "未知版本"

    @abstractmethod
    def get_help(self) -> str:
        """
        获取帮助信息

        Returns:
            帮助文本
        """
        pass


class CLIToolWrapper(SkillWrapperBase):
    """
    命令行工具 Wrapper 基类

    适用于大多数命令行工具的通用封装
    """

    def get_help(self) -> str:
        """获取帮助信息"""
        try:
            result = self._run_command(["--help"], check=False)
            return result.stdout
        except:
            return f"无法获取 {self.tool_name} 的帮助信息"

    def run(self, *args, **kwargs) -> subprocess.CompletedProcess:
        """
        运行命令

        Args:
            *args: 命令参数
            **kwargs: 传递给 _run_command 的参数

        Returns:
            subprocess.CompletedProcess 对象
        """
        return self._run_command(list(args), **kwargs)


# 使用示例

class GitHubCLIWrapper(SkillWrapperBase):
    """GitHub CLI (gh) Wrapper 示例"""

    def __init__(self):
        super().__init__("gh", "https://cli.github.com/")

    def get_help(self) -> str:
        """获取帮助信息"""
        result = self._run_command(["--help"])
        return result.stdout

    def repo_view(self, repo: Optional[str] = None) -> Dict[str, Any]:
        """查看仓库信息"""
        import json

        args = ["repo", "view"]
        if repo:
            args.extend(["--repo", repo])
        args.append("--json=name,description,url")

        result = self._run_command(args)
        return json.loads(result.stdout)


class TaskWrapper(SkillWrapperBase):
    """Task (Go Task) Wrapper 示例"""

    def __init__(self):
        super().__init__("task", "https://taskfile.dev/")

    def get_help(self) -> str:
        """获取帮助信息"""
        result = self._run_command(["--help"])
        return result.stdout

    def list_tasks(self) -> str:
        """列出所有任务"""
        result = self._run_command(["--list"])
        return result.stdout

    def run_task(self, task_name: str) -> None:
        """运行指定任务"""
        self._run_command([task_name], capture_output=False)


class JustWrapper(SkillWrapperBase):
    """Just Wrapper 示例"""

    def __init__(self):
        super().__init__("just", "https://github.com/casey/just")

    def get_help(self) -> str:
        """获取帮助信息"""
        result = self._run_command(["--help"])
        return result.stdout

    def list_recipes(self) -> str:
        """列出所有 recipes"""
        result = self._run_command(["--list"])
        return result.stdout

    def run_recipe(self, recipe_name: str, *args) -> None:
        """运行指定 recipe"""
        self._run_command([recipe_name] + list(args), capture_output=False)


# 工具函数

def check_multiple_tools(tools: List[str]) -> Dict[str, bool]:
    """
    检查多个工具的安装状态

    Args:
        tools: 工具名称列表

    Returns:
        工具名称到安装状态的映射
    """
    return {tool: shutil.which(tool) is not None for tool in tools}


def suggest_install(tool_name: str) -> str:
    """
    提供安装建议

    Args:
        tool_name: 工具名称

    Returns:
        安装建议文本
    """
    install_commands = {
        "gh": "brew install gh",
        "task": "brew install go-task/tap/go-task",
        "just": "brew install just",
        "zx": "npm install -g zx",
    }

    if tool_name in install_commands:
        return f"安装命令: {install_commands[tool_name]}"
    else:
        return f"请访问 https://github.com/{tool_name} 查看安装指南"


if __name__ == "__main__":
    # 测试示例
    print("Skill Wrapper 基类模板")
    print("="*60)

    # 检查工具安装状态
    tools = ["gh", "task", "just", "zx"]
    status = check_multiple_tools(tools)

    print("\n工具安装状态:")
    for tool, installed in status.items():
        icon = "✅" if installed else "❌"
        print(f"  {icon} {tool}")
        if not installed:
            print(f"     {suggest_install(tool)}")
