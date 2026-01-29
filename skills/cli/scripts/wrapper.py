#!/usr/bin/env python3
"""
GitHub CLI (gh) Wrapper
提供 GitHub CLI 工具的 Python 封装接口
"""

import subprocess
import json
import sys
from typing import Optional, List, Dict, Any


class GitHubCLI:
    """GitHub CLI (gh) 的 Python 封装类"""

    def __init__(self):
        """初始化 GitHub CLI wrapper"""
        self._check_installed()

    def _check_installed(self) -> None:
        """检查 gh 是否已安装"""
        try:
            subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                check=True,
                text=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "GitHub CLI (gh) 未安装。请访问 https://cli.github.com/ 安装。"
            )

    def _run_command(
        self,
        args: List[str],
        capture_output: bool = True
    ) -> subprocess.CompletedProcess:
        """
        执行 gh 命令

        Args:
            args: 命令参数列表
            capture_output: 是否捕获输出

        Returns:
            subprocess.CompletedProcess 对象
        """
        cmd = ["gh"] + args
        try:
            return subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {' '.join(cmd)}", file=sys.stderr)
            print(f"错误: {e.stderr}", file=sys.stderr)
            raise

    # 仓库操作
    def repo_view(self, repo: Optional[str] = None) -> Dict[str, Any]:
        """
        查看仓库信息

        Args:
            repo: 仓库格式 (owner/repo)，默认为当前仓库

        Returns:
            仓库信息字典
        """
        args = ["repo", "view"]
        if repo:
            args.extend(["--repo", repo])
        args.append("--json=name,description,primaryLanguage,owner,url,stargazerCount")

        result = self._run_command(args)
        return json.loads(result.stdout)

    def repo_create(
        self,
        name: str,
        description: str = "",
        public: bool = False,
        source: Optional[str] = None
    ) -> str:
        """
        创建新仓库

        Args:
            name: 仓库名称
            description: 仓库描述
            public: 是否公开
            source: 源仓库路径

        Returns:
            创建的仓库 URL
        """
        args = ["repo", "create", name, "--description", description]
        if public:
            args.append("--public")
        else:
            args.append("--private")
        if source:
            args.extend(["--source", source])

        result = self._run_command(args, capture_output=False)
        return result.stdout.strip()

    def repo_clone(self, repo: str, dir: Optional[str] = None) -> str:
        """
        克隆仓库

        Args:
            repo: 仓库格式 (owner/repo)
            dir: 目标目录

        Returns:
            克隆结果
        """
        args = ["repo", "clone", repo]
        if dir:
            args.append(dir)

        result = self._run_command(args, capture_output=False)
        return result.stdout.strip()

    # Issue 操作
    def issue_list(
        self,
        repo: Optional[str] = None,
        state: str = "open",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        列出 Issues

        Args:
            repo: 仓库格式
            state: 状态 (open, closed, all)
            limit: 返回数量限制

        Returns:
            Issue 列表
        """
        args = ["issue", "list", "--limit", str(limit), "--state", state]
        if repo:
            args.extend(["--repo", repo])
        args.append("--json=title,number,state,author,url")

        result = self._run_command(args)
        return json.loads(result.stdout)

    def issue_create(
        self,
        title: str,
        body: str = "",
        repo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建 Issue

        Args:
            title: Issue 标题
            body: Issue 内容
            repo: 仓库格式

        Returns:
            创建的 Issue 信息
        """
        args = ["issue", "create", "--title", title]
        if body:
            args.extend(["--body", body])
        if repo:
            args.extend(["--repo", repo])

        result = self._run_command(args)
        # 解析输出获取 Issue URL
        output = result.stdout.strip()
        return {"url": output}

    # PR 操作
    def pr_list(
        self,
        repo: Optional[str] = None,
        state: str = "open",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        列出 Pull Requests

        Args:
            repo: 仓库格式
            state: 状态 (open, closed, merged, all)
            limit: 返回数量限制

        Returns:
            PR 列表
        """
        args = ["pr", "list", "--limit", str(limit), "--state", state]
        if repo:
            args.extend(["--repo", repo])
        args.append("--json=title,number,state,author,url,headRefName")

        result = self._run_command(args)
        return json.loads(result.stdout)

    def pr_create(
        self,
        title: str,
        body: str,
        base: str,
        head: str,
        repo: Optional[str] = None
    ) -> str:
        """
        创建 Pull Request

        Args:
            title: PR 标题
            body: PR 描述
            base: 目标分支
            head: 源分支
            repo: 仓库格式

        Returns:
            创建的 PR URL
        """
        args = [
            "pr", "create", "--title", title,
            "--body", body, "--base", base, "--head", head
        ]
        if repo:
            args.extend(["--repo", repo])

        result = self._run_command(args)
        return result.stdout.strip()

    def pr_merge(
        self,
        pr_number: int,
        repo: Optional[str] = None,
        merge_method: str = "merge"
    ) -> str:
        """
        合并 Pull Request

        Args:
            pr_number: PR 编号
            repo: 仓库格式
            merge_method: 合并方式 (merge, squash, rebase)

        Returns:
            合并结果
        """
        args = ["pr", "merge", str(pr_number), "--" + merge_method]
        if repo:
            args.extend(["--repo", repo])

        result = self._run_command(args)
        return result.stdout.strip()

    # Actions 操作
    def workflow_list(
        self,
        repo: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        列出工作流

        Args:
            repo: 仓库格式

        Returns:
            工作流列表
        """
        args = ["workflow", "list"]
        if repo:
            args.extend(["--repo", repo])

        result = self._run_command(args)
        # 解析输出
        workflows = []
        for line in result.stdout.strip().split('\n')[1:]:  # 跳过标题行
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    workflows.append({
                        "name": ' '.join(parts[:-2]),
                        "state": parts[-2],
                        "id": parts[-1]
                    })
        return workflows

    def workflow_run(
        self,
        workflow: str,
        repo: Optional[str] = None
    ) -> str:
        """
        手动触发工作流

        Args:
            workflow: 工作流文件名或 ID
            repo: 仓库格式

        Returns:
            运行结果
        """
        args = ["workflow", "run", workflow]
        if repo:
            args.extend(["--repo", repo])

        result = self._run_command(args)
        return result.stdout.strip()

    # 认证操作
    def auth_status(self) -> Dict[str, Any]:
        """
        查看认证状态

        Returns:
            认证状态信息
        """
        args = ["auth", "status"]
        result = self._run_command(args)

        # 解析输出
        status = {}
        for line in result.stdout.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                status[key.strip()] = value.strip()
        return status

    def auth_login(self) -> str:
        """
        登录 GitHub

        Returns:
            登录结果
        """
        args = ["auth", "login"]
        result = self._run_command(args, capture_output=False)
        return result.stdout.strip()

    # 搜索操作
    def search_repos(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        搜索仓库

        Args:
            query: 搜索关键词
            limit: 返回数量限制

        Returns:
            搜索结果列表
        """
        args = [
            "search", "repos", query,
            "--limit", str(limit),
            "--json=name,description,owner,stargazerCount,url"
        ]

        result = self._run_command(args)
        return json.loads(result.stdout)

    def search_issues(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        搜索 Issues

        Args:
            query: 搜索关键词
            limit: 返回数量限制

        Returns:
            搜索结果列表
        """
        args = [
            "search", "issues", query,
            "--limit", str(limit),
            "--json=title,number,state,author,url,repository"
        ]

        result = self._run_command(args)
        return json.loads(result.stdout)

    # 扩展操作
    def extension_list(self) -> List[Dict[str, Any]]:
        """
        列出已安装的扩展

        Returns:
            扩展列表
        """
        args = ["extension", "list"]
        result = self._run_command(args)

        extensions = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    extensions.append({
                        "name": parts[0],
                        "version": parts[1] if len(parts) > 1 else "unknown"
                    })
        return extensions

    def api_request(
        self,
        endpoint: str,
        method: str = "GET",
        fields: Optional[List[str]] = None
    ) -> Any:
        """
        发送 API 请求

        Args:
            endpoint: API 端点
            method: HTTP 方法
            fields: 要返回的 JSON 字段

        Returns:
            API 响应数据
        """
        args = ["api", endpoint, "--method", method]
        if fields:
            args.extend(["-f", ",".join(fields)])

        result = self._run_command(args)
        return json.loads(result.stdout)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub CLI (gh) Python Wrapper")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 仓库命令
    repo_parser = subparsers.add_parser("repo", help="仓库操作")
    repo_subparsers = repo_parser.add_subparsers(dest="repo_command")

    repo_view_parser = repo_subparsers.add_parser("view", help="查看仓库")
    repo_view_parser.add_argument("--repo", help="仓库 (owner/repo)")

    repo_create_parser = repo_subparsers.add_parser("create", help="创建仓库")
    repo_create_parser.add_argument("name", help="仓库名称")
    repo_create_parser.add_argument("--description", default="", help="仓库描述")
    repo_create_parser.add_argument("--public", action="store_true", help="公开仓库")

    # Issue 命令
    issue_parser = subparsers.add_parser("issue", help="Issue 操作")
    issue_subparsers = issue_parser.add_subparsers(dest="issue_command")

    issue_list_parser = issue_subparsers.add_parser("list", help="列出 Issues")
    issue_list_parser.add_argument("--repo", help="仓库 (owner/repo)")
    issue_list_parser.add_argument("--state", default="open", help="状态 (open, closed, all)")
    issue_list_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    issue_create_parser = issue_subparsers.add_parser("create", help="创建 Issue")
    issue_create_parser.add_argument("title", help="Issue 标题")
    issue_create_parser.add_argument("--body", default="", help="Issue 内容")
    issue_create_parser.add_argument("--repo", help="仓库 (owner/repo)")

    # PR 命令
    pr_parser = subparsers.add_parser("pr", help="Pull Request 操作")
    pr_subparsers = pr_parser.add_subparsers(dest="pr_command")

    pr_list_parser = pr_subparsers.add_parser("list", help="列出 PRs")
    pr_list_parser.add_argument("--repo", help="仓库 (owner/repo)")
    pr_list_parser.add_argument("--state", default="open", help="状态 (open, closed, merged, all)")
    pr_list_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    # 搜索命令
    search_parser = subparsers.add_parser("search", help="搜索操作")
    search_subparsers = search_parser.add_subparsers(dest="search_command")

    search_repos_parser = search_subparsers.add_parser("repos", help="搜索仓库")
    search_repos_parser.add_argument("query", help="搜索关键词")
    search_repos_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    search_issues_parser = search_subparsers.add_parser("issues", help="搜索 Issues")
    search_issues_parser.add_argument("query", help="搜索关键词")
    search_issues_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    # 认证命令
    auth_parser = subparsers.add_parser("auth", help="认证操作")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command")

    auth_status_parser = auth_subparsers.add_parser("status", help="认证状态")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    gh = GitHubCLI()

    try:
        # 仓库操作
        if args.command == "repo":
            if args.repo_command == "view":
                result = gh.repo_view(args.repo)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif args.repo_command == "create":
                result = gh.repo_create(args.name, args.description, args.public)
                print(result)

        # Issue 操作
        elif args.command == "issue":
            if args.issue_command == "list":
                result = gh.issue_list(args.repo, args.state, args.limit)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif args.issue_command == "create":
                result = gh.issue_create(args.title, args.body, args.repo)
                print(json.dumps(result, indent=2, ensure_ascii=False))

        # PR 操作
        elif args.command == "pr":
            if args.pr_command == "list":
                result = gh.pr_list(args.repo, args.state, args.limit)
                print(json.dumps(result, indent=2, ensure_ascii=False))

        # 搜索操作
        elif args.command == "search":
            if args.search_command == "repos":
                result = gh.search_repos(args.query, args.limit)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif args.search_command == "issues":
                result = gh.search_issues(args.query, args.limit)
                print(json.dumps(result, indent=2, ensure_ascii=False))

        # 认证操作
        elif args.command == "auth":
            if args.auth_command == "status":
                result = gh.auth_status()
                print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
