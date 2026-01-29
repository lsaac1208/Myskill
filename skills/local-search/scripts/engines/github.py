#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 搜索引擎实现 - 使用 GitHub CLI
"""

import sys
import os
import subprocess
import json
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from engines.base import BaseSearchEngine, SearchResult


class GitHubSearchEngine(BaseSearchEngine):
    """GitHub 搜索引擎（使用 GitHub CLI）"""

    def __init__(self, timeout: int = 30):
        super().__init__("GitHub", timeout)
        self.available = self._check_gh_available()

    def _check_gh_available(self) -> bool:
        """检查 GitHub CLI 是否可用"""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def is_available(self) -> bool:
        """检查 GitHub 搜索是否可用"""
        return self.available

    def search(
        self,
        query: str,
        max_results: int = 10,
        search_type: str = "repos"
    ) -> List[SearchResult]:
        """
        使用 GitHub 搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数
            search_type: 搜索类型 (repos/code/issues/prs/users/topics)

        Returns:
            List[SearchResult]: 搜索结果列表
        """
        if not self.is_available():
            print(f"⚠️  GitHub 搜索不可用（需要安装 GitHub CLI）")
            return []

        results = []

        try:
            # 根据搜索类型调用不同的搜索方法
            if search_type == "repos":
                results = self._search_repos(query, max_results)
            elif search_type == "code":
                results = self._search_code(query, max_results)
            elif search_type == "issues":
                results = self._search_issues(query, max_results)
            elif search_type == "prs":
                results = self._search_prs(query, max_results)
            elif search_type == "users":
                results = self._search_users(query, max_results)
            else:
                print(f"⚠️  不支持的搜索类型: {search_type}")
                return []

        except Exception as e:
            print(f"⚠️  GitHub 搜索失败: {e}")

        return results

    def _search_repos(self, query: str, max_results: int) -> List[SearchResult]:
        """搜索 GitHub 仓库"""
        results = []
        try:
            # 使用 gh search 命令
            cmd = [
                "gh", "search", "repos",
                query,
                "--limit", str(max_results),
                "--json", "name,description,url,language,updatedAt"
            ]

            output = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if output.returncode != 0:
                return []

            data = json.loads(output.stdout)

            for item in data:
                result = SearchResult(
                    title=item.get("name", ""),
                    url=item.get("url", ""),
                    snippet=self._format_repo_snippet(item),
                    source=self.name,
                    date=item.get("updatedAt", "")[:10] if item.get("updatedAt") else None
                )
                results.append(result)

        except json.JSONDecodeError:
            print("⚠️  GitHub 返回数据解析失败")
        except Exception as e:
            print(f"⚠️  仓库搜索失败: {e}")

        return results

    def _search_code(self, query: str, max_results: int) -> List[SearchResult]:
        """搜索 GitHub 代码"""
        results = []
        try:
            cmd = [
                "gh", "search", "code",
                query,
                "--limit", str(max_results),
                "--json", "path,url,repository"
            ]

            output = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if output.returncode != 0:
                return []

            data = json.loads(output.stdout)

            for item in data:
                repo = item.get("repository", {})
                repo_name = repo.get("fullName", "") if repo else ""
                path = item.get("path", "")

                # 从路径提取文件名
                file_name = path.split("/")[-1] if path else "code"

                result = SearchResult(
                    title=file_name,
                    url=item.get("url", ""),
                    snippet=f"仓库: {repo_name} | 路径: {path}",
                    source=f"{self.name}/Code"
                )
                results.append(result)

        except Exception as e:
            print(f"⚠️  代码搜索失败: {e}")

        return results

    def _search_issues(self, query: str, max_results: int) -> List[SearchResult]:
        """搜索 GitHub Issues"""
        results = []
        try:
            cmd = [
                "gh", "search", "issues",
                query,
                "--limit", str(max_results),
                "--json", "title,url,body,state,updatedAt"
            ]

            output = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if output.returncode != 0:
                return []

            data = json.loads(output.stdout)

            for item in data:
                body = item.get("body", "")
                snippet = (body[:100] + "...") if body else ""

                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=f"{snippet} | 状态: {item.get('state', '')}",
                    source=f"{self.name}/Issue",
                    date=item.get("updatedAt", "")[:10] if item.get("updatedAt") else None
                )
                results.append(result)

        except Exception as e:
            print(f"⚠️  Issue 搜索失败: {e}")

        return results

    def _search_prs(self, query: str, max_results: int) -> List[SearchResult]:
        """搜索 GitHub Pull Requests"""
        results = []
        try:
            cmd = [
                "gh", "search", "prs",
                query,
                "--limit", str(max_results),
                "--json", "title,url,state,updatedAt"
            ]

            output = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if output.returncode != 0:
                return []

            data = json.loads(output.stdout)

            for item in data:
                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=f"状态: {item.get('state', '')}",
                    source=f"{self.name}/PR",
                    date=item.get("updatedAt", "")[:10] if item.get("updatedAt") else None
                )
                results.append(result)

        except Exception as e:
            print(f"⚠️  PR 搜索失败: {e}")

        return results

    def _search_users(self, query: str, max_results: int) -> List[SearchResult]:
        """搜索 GitHub 用户"""
        results = []
        try:
            cmd = [
                "gh", "search", "users",
                query,
                "--limit", str(max_results),
                "--json", "login,name,url,bio"
            ]

            output = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if output.returncode != 0:
                return []

            data = json.loads(output.stdout)

            for item in data:
                bio = item.get("bio", "")
                snippet = bio if bio else "用户"

                result = SearchResult(
                    title=item.get("login", ""),
                    url=item.get("url", ""),
                    snippet=snippet,
                    source=f"{self.name}/User"
                )
                results.append(result)

        except Exception as e:
            print(f"⚠️  用户搜索失败: {e}")

        return results

    def _format_repo_snippet(self, item: dict) -> str:
        """格式化仓库信息"""
        parts = []
        if item.get("description"):
            parts.append(item["description"])
        if item.get("language"):
            parts.append(f"语言: {item['language']}")
        if item.get("stargazersCount"):
            parts.append(f"⭐ {item['stargazersCount']}")
        return " | ".join(parts)

    def smart_search(
        self,
        query: str,
        max_results: int = 10
    ) -> List[SearchResult]:
        """
        智能搜索 - 自动识别搜索类型

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            List[SearchResult]: 搜索结果列表
        """
        # 检测搜索类型
        search_type = self._detect_search_type(query)
        return self.search(query, max_results, search_type)

    def _detect_search_type(self, query: str) -> str:
        """检测搜索类型"""
        query_lower = query.lower()

        # 代码搜索关键词
        if any(kw in query_lower for kw in ["code:", "language:", "extension:", "filename:"]):
            return "code"

        # Issue/PR 搜索关键词
        if any(kw in query_lower for kw in ["issue:", "is:issue", "is:pr", "author:", "mentions:"]):
            return "issues"

        # 用户搜索
        if any(kw in query_lower for kw in ["user:", "org:"]):
            return "users"

        # 默认搜索仓库
        return "repos"


# 测试代码
if __name__ == "__main__":
    engine = GitHubSearchEngine()

    if not engine.is_available():
        print("GitHub 搜索引擎不可用，请安装 GitHub CLI: https://cli.github.com/")
    else:
        print("=== GitHub 搜索测试 ===\n")

        # 测试仓库搜索
        print("测试搜索仓库 'python':")
        results = engine.search("python", max_results=3, search_type="repos")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.title}")
            print(f"   {r.url}")
            print(f"   {r.snippet[:80]}...")
            print()

        # 测试智能搜索
        print("\n测试智能搜索 'lang:python search':")
        results = engine.smart_search("lang:python search", max_results=3)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.title}")
            print(f"   {r.url}")
            print()
