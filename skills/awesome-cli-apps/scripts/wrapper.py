#!/usr/bin/env python3
"""
Awesome CLI Apps 列表查询工具
提供对 agarrharr/awesome-cli-apps 列表的查询和搜索功能
"""

import subprocess
import json
import sys
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.request import urlopen
from urllib.error import URLError


class AwesomeCLIApps:
    """Awesome CLI Apps 列表的 Python 封装类"""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化 Awesome CLI Apps 查询工具

        Args:
            cache_dir: 缓存目录
        """
        self.repo_url = "https://github.com/agarrharr/awesome-cli-apps"
        self.raw_url = "https://raw.githubusercontent.com/agarrharr/awesome-cli-apps/master/README.md"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".cache" / "awesome-cli-apps"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "README.md"

    def fetch_readme(self, force_refresh: bool = False) -> str:
        """
        获取 README 内容

        Args:
            force_refresh: 是否强制刷新

        Returns:
            README 内容
        """
        # 检查缓存
        if not force_refresh and self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return f.read()

        # 从网络获取
        try:
            with urlopen(self.raw_url, timeout=10) as response:
                content = response.read().decode('utf-8')

            # 保存到缓存
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                f.write(content)

            return content
        except URLError as e:
            if self.cache_file.exists():
                print(f"网络错误，使用缓存: {e}", file=sys.stderr)
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            raise RuntimeError(f"无法获取 README: {e}")

    def parse_categories(self, content: str) -> List[Dict[str, Any]]:
        """
        解析 README 中的分类

        Args:
            content: README 内容

        Returns:
            分类列表
        """
        categories = []
        current_category = None

        for line in content.split('\n'):
            # 匹配二级标题 (## Category Name)
            match = re.match(r'^##\s+(.+)$', line)
            if match:
                category_name = match.group(1).strip()
                # 跳过 Table of Contents 和 License
                if category_name not in ['Table of Contents', 'License']:
                    current_category = {
                        "name": category_name,
                        "tools": []
                    }
                    categories.append(current_category)
            elif current_category:
                # 匹配工具条目 - [tool](url) - description
                tool_match = re.match(r'^-\s+\[([^\]]+)\]\(([^)]+)\)\s+-\s+(.+)$', line)
                if tool_match:
                    tool_name = tool_match.group(1)
                    tool_url = tool_match.group(2)
                    tool_desc = tool_match.group(3)
                    current_category["tools"].append({
                        "name": tool_name,
                        "url": tool_url,
                        "description": tool_desc
                    })

        return categories

    def list_categories(self) -> List[Dict[str, Any]]:
        """
        列出所有分类

        Returns:
            分类列表
        """
        content = self.fetch_readme()
        return self.parse_categories(content)

    def search_tools(
        self,
        query: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索工具

        Args:
            query: 搜索关键词
            category: 限定分类

        Returns:
            匹配的工具列表
        """
        categories = self.list_categories()
        results = []
        query_lower = query.lower()

        for cat in categories:
            if category and cat["name"] != category:
                continue

            for tool in cat["tools"]:
                # 在名称、描述中搜索
                if (query_lower in tool["name"].lower() or
                    query_lower in tool["description"].lower()):
                    results.append({
                        **tool,
                        "category": cat["name"]
                    })

        return results

    def get_tools_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        获取指定分类的所有工具

        Args:
            category: 分类名称

        Returns:
            工具列表
        """
        categories = self.list_categories()

        for cat in categories:
            if cat["name"] == category:
                return cat["tools"]

        return []

    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        获取工具详细信息

        Args:
            tool_name: 工具名称

        Returns:
            工具信息
        """
        results = self.search_tools(tool_name)
        for result in results:
            if result["name"].lower() == tool_name.lower():
                return result
        return None

    def get_popular_tools(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取热门工具（基于 stars 数）

        Args:
            limit: 返回数量

        Returns:
            热门工具列表
        """
        # 这个列表是精选的，返回一些知名的 CLI 工具
        popular_tools = [
            {"name": "fzf", "category": "Utilities", "description": "命令行模糊查找器"},
            {"name": "rg", "category": "Utilities", "description": "ripgrep - 递归搜索工具"},
            {"name": "fd", "category": "Files and Directories", "description": "find 的简单替代"},
            {"name": "bat", "category": "Files and Directories", "description": "cat 的增强版"},
            {"name": "exa", "category": "Files and Directories", "description": "ls 的现代替代"},
            {"name": "jq", "category": "Data Manipulation", "description": "JSON 处理工具"},
            {"name": "htop", "category": "Utilities", "description": "交互式进程查看器"},
            {"name": "tldr", "category": "Development", "description": "简化的 man pages"},
            {"name": "delta", "category": "Development", "description": "git diff 的增强查看器"},
            {"name": "zoxide", "category": "Directory Navigation", "description": "更智能的 cd"},
        ]

        return popular_tools[:limit]

    def export_json(self, output_file: str) -> None:
        """
        导出数据为 JSON

        Args:
            output_file: 输出文件路径
        """
        categories = self.list_categories()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=2, ensure_ascii=False)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Awesome CLI Apps 查询工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 列出分类
    list_parser = subparsers.add_parser("list", help="列出所有分类")
    list_parser.add_argument("--format", choices=["table", "json"], default="table",
                          help="输出格式")

    # 搜索工具
    search_parser = subparsers.add_parser("search", help="搜索工具")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--category", help="限定分类")
    search_parser.add_argument("--format", choices=["table", "json"], default="table",
                             help="输出格式")

    # 获取分类工具
    category_parser = subparsers.add_parser("category", help="获取指定分类的工具")
    category_parser.add_argument("category", help="分类名称")
    category_parser.add_argument("--format", choices=["table", "json"], default="table",
                               help="输出格式")

    # 获取工具信息
    info_parser = subparsers.add_parser("info", help="获取工具详细信息")
    info_parser.add_argument("tool", help="工具名称")

    # 热门工具
    popular_parser = subparsers.add_parser("popular", help="获取热门工具")
    popular_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    # 导出
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("output", help="输出文件路径")
    export_parser.add_argument("--refresh", action="store_true", help="强制刷新")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    awesome = AwesomeCLIApps()

    try:
        if args.command == "list":
            categories = awesome.list_categories()

            if args.format == "json":
                print(json.dumps(categories, indent=2, ensure_ascii=False))
            else:
                print("Awesome CLI Apps 分类:")
                for cat in categories:
                    tool_count = len(cat.get("tools", []))
                    print(f"  {cat['name']} ({tool_count} 个工具)")

        elif args.command == "search":
            results = awesome.search_tools(args.query, args.category)

            if args.format == "json":
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                print(f"搜索 '{args.query}' 的结果:")
                for tool in results:
                    print(f"  {tool['name']} - {tool['description']}")
                    print(f"    分类: {tool['category']}")
                    print(f"    链接: {tool['url']}")

        elif args.command == "category":
            tools = awesome.get_tools_by_category(args.category)

            if args.format == "json":
                print(json.dumps(tools, indent=2, ensure_ascii=False))
            else:
                print(f"分类 '{args.category}' 的工具:")
                for tool in tools:
                    print(f"  {tool['name']} - {tool['description']}")
                    print(f"    链接: {tool['url']}")

        elif args.command == "info":
            info = awesome.get_tool_info(args.tool)
            if info:
                print(json.dumps(info, indent=2, ensure_ascii=False))
            else:
                print(f"未找到工具: {args.tool}", file=sys.stderr)
                sys.exit(1)

        elif args.command == "popular":
            tools = awesome.get_popular_tools(args.limit)
            print("热门 CLI 工具:")
            for tool in tools:
                print(f"  {tool['name']} - {tool['description']}")
                print(f"    分类: {tool['category']}")

        elif args.command == "export":
            if args.refresh:
                awesome.fetch_readme(force_refresh=True)
            awesome.export_json(args.output)
            print(f"✓ 数据已导出到: {args.output}")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
