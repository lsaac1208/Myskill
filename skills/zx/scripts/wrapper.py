#!/usr/bin/env python3
"""
Zx JavaScript 脚本工具 Wrapper
提供 zx 命令的 Python 封装接口
"""

import subprocess
import json
import sys
import os
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any


class ZxRunner:
    """Zx JavaScript 脚本工具的 Python 封装类"""

    def __init__(self, working_dir: Optional[str] = None):
        """
        初始化 Zx runner

        Args:
            working_dir: 工作目录，默认为当前目录
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()
        self._check_installed()

    def _check_installed(self) -> None:
        """检查 zx 是否已安装"""
        try:
            # 检查 npx 可以访问 zx
            result = subprocess.run(
                ["npx", "zx", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # zx 不返回错误码即为成功
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(
                "Zx 未安装。请运行: npm install -g zx\n"
                "或者在项目中: npm install zx"
            )

    def _run_command(
        self,
        args: List[str],
        capture_output: bool = True,
        check: bool = True,
        input_text: Optional[str] = None
    ) -> subprocess.CompletedProcess:
        """
        执行 zx 命令

        Args:
            args: 命令参数列表
            capture_output: 是否捕获输出
            check: 是否检查返回码
            input_text: 标准输入内容

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd = ["npx", "zx"] + args
        try:
            return subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                cwd=self.working_dir,
                check=check,
                input=input_text
            )
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {' '.join(cmd)}", file=sys.stderr)
            if e.stderr:
                print(f"错误: {e.stderr}", file=sys.stderr)
            raise

    def run_script(
        self,
        script_path: str,
        args: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """
        运行 zx 脚本文件

        Args:
            script_path: 脚本文件路径
            args: 脚本参数列表

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd_args = [script_path]
        if args:
            cmd_args.extend(args)

        return self._run_command(cmd_args, capture_output=False)

    def run_code(
        self,
        code: str,
        args: Optional[List[str]] = None
    ) -> subprocess.CompletedProcess:
        """
        直接运行 JavaScript 代码

        Args:
            code: JavaScript 代码
            args: 脚本参数列表

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd_args = ["-"]
        if args:
            cmd_args.extend(args)

        return self._run_command(cmd_args, input_text=code, capture_output=False)

    def run_code_with_output(
        self,
        code: str,
        args: Optional[List[str]] = None
    ) -> str:
        """
        运行 JavaScript 代码并返回输出

        Args:
            code: JavaScript 代码
            args: 脚本参数列表

        Returns:
            命令输出
        """
        cmd_args = ["-"]
        if args:
            cmd_args.extend(args)

        result = self._run_command(cmd_args, input_text=code)
        return result.stdout

    def execute_shell_command(
        self,
        command: str,
        use_zx: bool = True
    ) -> subprocess.CompletedProcess:
        """
        使用 zx 执行 shell 命令

        Args:
            command: Shell 命令
            use_zx: 是否使用 zx 的 $ 函数

        Returns:
            subprocess.CompletedProcess 对象
        """
        if use_zx:
            code = f"await $`{command}`\n"
        else:
            code = f"await exec(`{command}`)\n"

        return self.run_code(code)

    def create_script(
        self,
        filename: str,
        content: str,
        directory: Optional[str] = None
    ) -> Path:
        """
        创建一个新的 zx 脚本

        Args:
            filename: 文件名
            content: 脚本内容
            directory: 目标目录

        Returns:
            创建的文件路径
        """
        target_dir = Path(directory) if directory else self.working_dir
        file_path = target_dir / filename

        # 添加 shebang 如果不存在
        if not content.startswith('#!'):
            content = "#!/usr/bin/env zx\n" + content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # 添加执行权限
        file_path.chmod(0o755)

        return file_path

    def make_executable(self, script_path: str) -> None:
        """
        为脚本添加执行权限

        Args:
            script_path: 脚本路径
        """
        path = Path(script_path)
        path.chmod(0o755)

    def validate_script(self, script_path: str) -> bool:
        """
        验证脚本语法

        Args:
            script_path: 脚本路径

        Returns:
            是否有效
        """
        try:
            # 使用 node 检查语法
            result = subprocess.run(
                ["node", "--check", script_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_script_template(self, template_type: str = "basic") -> str:
        """
        获取脚本模板

        Args:
            template_type: 模板类型 (basic, async, with-args)

        Returns:
            模板内容
        """
        templates = {
            "basic": """#!/usr/bin/env zx

// 基本的 zx 脚本模板

console.log('Hello from zx!');

// 执行 shell 命令
await $`echo "Running shell command..."`

// 读取文件
const content = await fs.readFile('./package.json', 'utf-8')
console.log(content)
""",
            "async": """#!/usr/bin/env zx

// 异步操作的脚本模板

// 并发执行多个命令
await Promise.all([
  $`echo "Command 1"`,
  $`echo "Command 2"`,
  $`echo "Command 3"`
])

// 顺序执行
await $`sleep 1`
await $`echo "After sleep"`

// 处理输出
const output = await $`ls -la`
console.log(output.stdout)
""",
            "with-args": """#!/usr/bin/env zx

// 带参数的脚本模板

// 获取命令行参数
const args = process.argv.slice(2)
const name = args[0] || 'World'

console.log(`Hello, ${name}!`)

// 使用环境变量
const envVar = process.env.MY_VAR || 'default'
console.log(`MY_VAR: ${envVar}`)
"""
        }

        return templates.get(template_type, templates["basic"])

    def run_with_env(
        self,
        code: str,
        env_vars: Dict[str, str]
    ) -> subprocess.CompletedProcess:
        """
        运行代码并设置环境变量

        Args:
            code: JavaScript 代码
            env_vars: 环境变量字典

        Returns:
            subprocess.CompletedProcess 对象
        """
        # 构建带环境变量的代码
        env_code = "\n".join([
            f"process.env.{k} = '{v}'"
            for k, v in env_vars.items()
        ]) + "\n\n" + code

        return self.run_code(env_code)

    def interactive_shell(self) -> None:
        """
        启动交互式 zx shell
        """
        print("进入 zx 交互式 shell...")
        print("提示: 输入 .exit 退出")

        # 使用 zx 的 REPL
        subprocess.run(
            ["npx", "zx", "-i"],
            cwd=self.working_dir
        )

    def get_package_info(self) -> Dict[str, Any]:
        """
        获取 zx 包信息

        Returns:
            包信息字典
        """
        try:
            result = subprocess.run(
                ["npm", "info", "zx", "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                info = json.loads(result.stdout)
                return {
                    "version": info.get("version", "unknown"),
                    "description": info.get("description", ""),
                    "homepage": info.get("homepage", "")
                }
        except Exception:
            pass

        return {"version": "unknown", "description": "", "homepage": ""}


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Zx JavaScript 脚本工具 Python Wrapper")
    parser.add_argument("--dir", help="工作目录")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 运行脚本
    run_parser = subparsers.add_parser("run", help="运行脚本文件")
    run_parser.add_argument("script", help="脚本文件路径")
    run_parser.add_argument("args", nargs="*", help="脚本参数")

    # 运行代码
    eval_parser = subparsers.add_parser("eval", help="运行 JavaScript 代码")
    eval_parser.add_argument("code", help="JavaScript 代码")

    # 创建脚本
    create_parser = subparsers.add_parser("create", help="创建新脚本")
    create_parser.add_argument("filename", help="文件名")
    create_parser.add_argument("--template", default="basic",
                              help="模板类型 (basic, async, with-args)")
    create_parser.add_argument("--dir", help="目标目录")

    # 验证脚本
    validate_parser = subparsers.add_parser("validate", help="验证脚本语法")
    validate_parser.add_argument("script", help="脚本文件路径")

    # 获取模板
    template_parser = subparsers.add_parser("template", help="获取脚本模板")
    template_parser.add_argument("--type", default="basic", help="模板类型")

    # 执行命令
    exec_parser = subparsers.add_parser("exec", help="执行 shell 命令")
    exec_parser.add_argument("command", help="Shell 命令")

    # 信息
    info_parser = subparsers.add_parser("info", help="获取包信息")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    zx = ZxRunner(args.dir)

    try:
        if args.command == "run":
            zx.run_script(args.script, args.args)

        elif args.command == "eval":
            zx.run_code(args.code)

        elif args.command == "create":
            template = zx.get_script_template(args.template)
            file_path = zx.create_script(args.filename, template, getattr(args, 'dir', None))
            print(f"✓ 创建脚本: {file_path}")

        elif args.command == "validate":
            is_valid = zx.validate_script(args.script)
            if is_valid:
                print("✓ 脚本语法正确")
            else:
                print("✗ 脚本语法错误")
                sys.exit(1)

        elif args.command == "template":
            template = zx.get_script_template(args.type)
            print(template)

        elif args.command == "exec":
            zx.execute_shell_command(args.command)

        elif args.command == "info":
            info = zx.get_package_info()
            print(json.dumps(info, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
