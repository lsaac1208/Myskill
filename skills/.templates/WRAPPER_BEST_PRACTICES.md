# Wrapper 开发最佳实践

本文档提供创建高质量 Skill Wrapper 的指南和最佳实践。

## 📋 目录

1. [设计原则](#设计原则)
2. [代码结构](#代码结构)
3. [通用模式](#通用模式)
4. [错误处理](#错误处理)
5. [测试建议](#测试建议)
6. [示例代码](#示例代码)

## 🎯 设计原则

### 1. 单一职责
每个 Wrapper 类应该只封装一个工具，保持职责单一。

### 2. 简单优先
优先使用简单的实现，避免过度设计。

### 3. 用户友好
提供清晰的错误信息和安装指南。

### 4. 可测试性
设计时考虑测试，使用依赖注入等模式。

## 🏗️ 代码结构

### 推荐的文件结构

```
skill-name/
├── SKILL.md              # 文档
├── scripts/
│   ├── wrapper.py        # 主 Wrapper 类
│   ├── __init__.py       # 包初始化
│   └── utils.py          # 工具函数（可选）
└── tests/                # 测试（可选）
    └── test_wrapper.py
```

### Wrapper 类结构

```python
class ToolWrapper:
    """工具封装类"""

    def __init__(self):
        """初始化"""
        self._check_installed()

    def _check_installed(self):
        """检查工具是否已安装"""
        pass

    def _run_command(self, args):
        """执行命令"""
        pass

    def _handle_error(self, error):
        """处理错误"""
        pass

    # 公共 API 方法
    def method1(self):
        """功能1"""
        pass

    def method2(self):
        """功能2"""
        pass
```

## 🔄 通用模式

### 1. 依赖检查

**模式 A: 使用 shutil.which**

```python
import shutil

def _check_installed(self):
    """检查工具是否已安装"""
    if not shutil.which(self.tool_name):
        raise RuntimeError(
            f"{self.tool_name} 未安装。\n"
            f"安装指南: {self.install_url}"
        )
```

**模式 B: 尝试运行版本命令**

```python
import subprocess

def _check_installed(self):
    """检查工具是否已安装"""
    try:
        subprocess.run(
            [self.tool_name, "--version"],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(f"{self.tool_name} 未安装")
```

### 2. 命令执行

**标准模式**

```python
def _run_command(self, args, **kwargs):
    """执行命令"""
    cmd = [self.tool_name] + args

    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            **kwargs
        )
    except subprocess.CalledProcessError as e:
        self._handle_error(cmd, e)
        raise
```

**流式输出模式**

```python
def _run_command_stream(self, args):
    """执行命令并实时输出"""
    cmd = [self.tool_name] + args

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        print(line, end='')

    process.wait()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode,
            cmd,
            stderr=process.stderr.read()
        )
```

### 3. 参数构建

**链式构建**

```python
class CommandBuilder:
    """命令构建器"""

    def __init__(self, tool_name):
        self.tool_name = tool_name
        self.args = []

    def add(self, *args):
        """添加参数"""
        self.args.extend(args)
        return self

    def add_flag(self, flag, value=None):
        """添加标志"""
        self.args.append(flag)
        if value is not None:
            self.args.append(str(value))
        return self

    def build(self):
        """构建命令"""
        return [self.tool_name] + self.args

# 使用示例
cmd = (CommandBuilder("gh")
       .add("repo", "create")
       .add_flag("--description", "My repo")
       .add_flag("--public")
       .build())
```

### 4. JSON 输出处理

```python
import json

def _parse_json_output(self, result):
    """解析 JSON 输出"""
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise ValueError(f"无法解析 JSON 输出: {e}")
```

## ⚠️ 错误处理

### 1. 分层错误处理

```python
class ToolNotFoundError(Exception):
    """工具未找到错误"""
    pass

class CommandExecutionError(Exception):
    """命令执行错误"""
    pass

def _handle_error(self, cmd, error):
    """处理错误"""
    # 记录错误
    print(f"❌ 命令失败: {' '.join(cmd)}", file=sys.stderr)

    # 提供上下文
    if error.stderr:
        print(f"错误信息: {error.stderr}", file=sys.stderr)

    # 提供解决建议
    if "permission denied" in error.stderr.lower():
        print("💡 提示: 可能需要管理员权限", file=sys.stderr)
    elif "not found" in error.stderr.lower():
        print(f"💡 提示: 请检查 {self.tool_name} 是否正确安装", file=sys.stderr)
```

### 2. 友好的错误消息

```python
def _format_error_message(self, error):
    """格式化错误消息"""
    message = f"执行失败: {error}\n\n"
    message += "可能的原因:\n"
    message += "  1. 工具未正确安装\n"
    message += "  2. 参数格式错误\n"
    message += "  3. 权限不足\n\n"
    message += "解决方案:\n"
    message += f"  - 运行 '{self.tool_name} --version' 检查安装\n"
    message += f"  - 查看文档: {self.install_url}\n"
    return message
```

## 🧪 测试建议

### 1. 单元测试

```python
import unittest
from unittest.mock import patch, MagicMock

class TestToolWrapper(unittest.TestCase):
    """Wrapper 测试"""

    @patch('shutil.which')
    def test_check_installed_success(self, mock_which):
        """测试工具已安装"""
        mock_which.return_value = '/usr/bin/tool'
        wrapper = ToolWrapper()
        # 不应抛出异常

    @patch('shutil.which')
    def test_check_installed_failure(self, mock_which):
        """测试工具未安装"""
        mock_which.return_value = None
        with self.assertRaises(RuntimeError):
            ToolWrapper()

    @patch('subprocess.run')
    def test_run_command(self, mock_run):
        """测试命令执行"""
        mock_run.return_value = MagicMock(
            stdout='output',
            stderr='',
            returncode=0
        )
        wrapper = ToolWrapper()
        result = wrapper._run_command(['--version'])
        self.assertEqual(result.stdout, 'output')
```

### 2. 集成测试

```python
def test_integration():
    """集成测试"""
    # 跳过如果工具未安装
    if not shutil.which('tool'):
        return

    wrapper = ToolWrapper()

    # 测试基本功能
    version = wrapper.get_version()
    assert version

    # 测试命令执行
    result = wrapper.run_command(['--help'])
    assert result.returncode == 0
```

## 📝 示例代码

### 完整示例：GitHub CLI Wrapper

```python
#!/usr/bin/env python3
"""GitHub CLI Wrapper"""

import subprocess
import json
import sys
import shutil
from typing import Optional, List, Dict, Any


class GitHubCLI:
    """GitHub CLI (gh) 封装类"""

    def __init__(self):
        """初始化"""
        self.tool_name = "gh"
        self.install_url = "https://cli.github.com/"
        self._check_installed()

    def _check_installed(self) -> None:
        """检查 gh 是否已安装"""
        if not shutil.which(self.tool_name):
            raise RuntimeError(
                f"{self.tool_name} 未安装。\n"
                f"请访问 {self.install_url} 安装。"
            )

    def _run_command(
        self,
        args: List[str],
        **kwargs
    ) -> subprocess.CompletedProcess:
        """执行 gh 命令"""
        cmd = [self.tool_name] + args

        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
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
        """处理错误"""
        print(f"❌ 命令失败: {' '.join(cmd)}", file=sys.stderr)
        if error.stderr:
            print(f"错误: {error.stderr}", file=sys.stderr)

    def repo_view(self, repo: Optional[str] = None) -> Dict[str, Any]:
        """查看仓库信息"""
        args = ["repo", "view"]
        if repo:
            args.extend(["--repo", repo])
        args.append("--json=name,description,url")

        result = self._run_command(args)
        return json.loads(result.stdout)

    def get_version(self) -> str:
        """获取版本"""
        result = self._run_command(["--version"])
        return result.stdout.strip()


# 使用示例
if __name__ == "__main__":
    try:
        gh = GitHubCLI()
        print(f"版本: {gh.get_version()}")

        # 查看仓库
        repo_info = gh.repo_view("cli/cli")
        print(f"仓库: {repo_info['name']}")
        print(f"描述: {repo_info['description']}")

    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
```

## 💡 最佳实践总结

### DO ✅

1. **使用类型提示**: 提高代码可读性
2. **提供文档字符串**: 说明每个方法的用途
3. **检查依赖**: 在初始化时检查工具是否已安装
4. **友好的错误消息**: 提供清晰的错误信息和解决建议
5. **使用 subprocess.run**: 而不是 os.system
6. **捕获输出**: 使用 capture_output=True
7. **使用 text=True**: 自动处理编码
8. **提供安装指南**: 在错误消息中包含安装链接

### DON'T ❌

1. **不要忽略错误**: 总是处理可能的异常
2. **不要硬编码路径**: 使用 shutil.which 查找工具
3. **不要使用 shell=True**: 除非绝对必要
4. **不要阻塞**: 对于长时间运行的命令，考虑异步或流式输出
5. **不要假设环境**: 总是检查依赖和权限
6. **不要过度封装**: 保持简单，只封装必要的功能
7. **不要忽略返回码**: 使用 check=True 或手动检查
8. **不要混合关注点**: 保持 Wrapper 专注于工具封装

## 🔗 相关资源

- **基类模板**: `wrapper_base.py`
- **Python subprocess 文档**: https://docs.python.org/3/library/subprocess.html
- **类型提示**: https://docs.python.org/3/library/typing.html

---

**版本**: 1.0.0
**更新日期**: 2026-01-26
