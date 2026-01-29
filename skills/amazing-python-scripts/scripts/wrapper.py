#!/usr/bin/env python3
"""
Amazing Python Scripts 脚本查询工具
提供对 avinashkranjan/Amazing-Python-Scripts 脚本库的查询和搜索功能
"""

import subprocess
import json
import sys
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.request import urlopen
from urllib.error import URLError


class AmazingPythonScripts:
    """Amazing Python Scripts 脚本库的 Python 封装类"""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化 Amazing Python Scripts 查询工具

        Args:
            cache_dir: 缓存目录
        """
        self.repo_url = "https://github.com/avinashkranjan/Amazing-Python-Scripts"
        self.raw_url_base = "https://raw.githubusercontent.com/avinashkranjan/Amazing-Python-Scripts/master"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".cache" / "amazing-python-scripts"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "SCRIPTS.md"

    def fetch_scripts_md(self, force_refresh: bool = False) -> str:
        """
        获取 SCRIPTS.md 内容

        Args:
            force_refresh: 是否强制刷新

        Returns:
            SCRIPTS.md 内容
        """
        # 检查缓存
        if not force_refresh and self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return f.read()

        # 从网络获取
        url = f"{self.raw_url_base}/SCRIPTS.md"
        try:
            with urlopen(url, timeout=10) as response:
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
            raise RuntimeError(f"无法获取 SCRIPTS.md: {e}")

    def parse_scripts(self, content: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        解析脚本列表

        Args:
            content: SCRIPTS.md 内容

        Returns:
            脚本列表
        """
        if content is None:
            content = self.fetch_scripts_md()

        scripts = []
        current_category = None

        for line in content.split('\n'):
            # 匹配分类标题 (## Category Name)
            category_match = re.match(r'^##\s+(.+)$', line)
            if category_match:
                current_category = category_match.group(1).strip()
                continue

            # 匹配脚本条目 | 脚本名 | 描述 | 路径 |
            if '|' in line and '脚本' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    script_name = parts[1]
                    script_desc = parts[2] if len(parts) > 2 else ""
                    script_path = parts[3] if len(parts) > 3 else ""

                    # 提取链接
                    link_match = re.search(r'\[([^\]]+)\]', script_name)
                    if link_match:
                        name = link_match.group(1)
                    else:
                        name = script_name

                    if name:
                        scripts.append({
                            "name": name,
                            "description": script_desc,
                            "path": script_path,
                            "category": current_category or "未分类"
                        })

        return scripts

    def list_categories(self) -> List[str]:
        """
        列出所有分类

        Returns:
            分类列表
        """
        scripts = self.parse_scripts()
        categories = set()
        for script in scripts:
            if script["category"]:
                categories.add(script["category"])
        return sorted(list(categories))

    def search_scripts(
        self,
        query: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索脚本

        Args:
            query: 搜索关键词
            category: 限定分类

        Returns:
            匹配的脚本列表
        """
        scripts = self.parse_scripts()
        results = []
        query_lower = query.lower()

        for script in scripts:
            # 应用分类筛选
            if category and script["category"] != category:
                continue

            # 搜索匹配
            if (query_lower in script["name"].lower() or
                query_lower in script["description"].lower()):
                results.append(script)

        return results

    def get_script_info(self, script_name: str) -> Optional[Dict[str, Any]]:
        """
        获取脚本详细信息

        Args:
            script_name: 脚本名称

        Returns:
            脚本信息
        """
        scripts = self.parse_scripts()

        for script in scripts:
            if script["name"].lower() == script_name.lower():
                return script

        return None

    def get_scripts_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        获取指定分类的脚本

        Args:
            category: 分类名称

        Returns:
            脚本列表
        """
        scripts = self.parse_scripts()
        return [s for s in scripts if s["category"] == category]

    def get_script_source(self, script_path: str) -> Optional[str]:
        """
        获取脚本源代码

        Args:
            script_path: 脚本路径

        Returns:
            脚本源代码
        """
        url = f"{self.raw_url_base}/{script_path}"
        try:
            with urlopen(url, timeout=10) as response:
                return response.read().decode('utf-8')
        except URLError:
            return None

    def get_popular_scripts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取热门脚本

        Args:
            limit: 返回数量

        Returns:
            热门脚本列表
        """
        scripts = self.parse_scripts()

        # 精选一些实用且流行的脚本类别
        popular_categories = [
            "自动化",
            "网络",
            "文件处理",
            "图像处理",
            "实用工具"
        ]

        results = []
        for script in scripts:
            if any(cat in script["category"] for cat in popular_categories):
                results.append(script)
                if len(results) >= limit:
                    break

        return results[:limit]

    def export_json(self, output_file: str) -> None:
        """
        导出数据为 JSON

        Args:
            output_file: 输出文件路径
        """
        scripts = self.parse_scripts()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scripts, f, indent=2, ensure_ascii=False)

    def list_script_files(self) -> List[str]:
        """
        列出所有脚本文件路径

        Returns:
            脚本文件路径列表
        """
        scripts = self.parse_scripts()
        return [s["path"] for s in scripts if s["path"]]


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Amazing Python Scripts 查询工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 列出分类
    list_parser = subparsers.add_parser("list", help="列出所有分类")

    # 搜索脚本
    search_parser = subparsers.add_parser("search", help="搜索脚本")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--category", help="限定分类")
    search_parser.add_argument("--format", choices=["table", "json"], default="table",
                             help="输出格式")

    # 获取分类脚本
    category_parser = subparsers.add_parser("category", help="获取指定分类的脚本")
    category_parser.add_argument("category", help="分类名称")
    category_parser.add_argument("--format", choices=["table", "json"], default="table",
                               help="输出格式")

    # 获取脚本信息
    info_parser = subparsers.add_parser("info", help="获取脚本详细信息")
    info_parser.add_argument("script", help="脚本名称")

    # 获取脚本源代码
    source_parser = subparsers.add_parser("source", help="获取脚本源代码")
    source_parser.add_argument("path", help="脚本路径")

    # 热门脚本
    popular_parser = subparsers.add_parser("popular", help="获取热门脚本")
    popular_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    # 导出
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("output", help="输出文件路径")
    export_parser.add_argument("--refresh", action="store_true", help="强制刷新")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    aps = AmazingPythonScripts()

    try:
        if args.command == "list":
            categories = aps.list_categories()
            print("脚本分类:")
            for cat in categories:
                print(f"  {cat}")

        elif args.command == "search":
            results = aps.search_scripts(args.query, args.category)

            if args.format == "json":
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                print(f"搜索 '{args.query}' 的结果:")
                for script in results:
                    print(f"  {script['name']} - {script['description']}")
                    print(f"    分类: {script['category']}")
                    if script['path']:
                        print(f"    路径: {script['path']}")

        elif args.command == "category":
            scripts = aps.get_scripts_by_category(args.category)

            if args.format == "json":
                print(json.dumps(scripts, indent=2, ensure_ascii=False))
            else:
                print(f"分类 '{args.category}' 的脚本:")
                for script in scripts:
                    print(f"  {script['name']} - {script['description']}")

        elif args.command == "info":
            info = aps.get_script_info(args.script)
            if info:
                print(json.dumps(info, indent=2, ensure_ascii=False))
            else:
                print(f"未找到脚本: {args.script}", file=sys.stderr)
                sys.exit(1)

        elif args.command == "source":
            source = aps.get_script_source(args.path)
            if source:
                print(source)
            else:
                print(f"无法获取脚本源代码: {args.path}", file=sys.stderr)
                sys.exit(1)

        elif args.command == "popular":
            scripts = aps.get_popular_scripts(args.limit)
            print("热门 Python 脚本:")
            for script in scripts:
                print(f"  {script['name']} - {script['description']}")
                print(f"    分类: {script['category']}")

        elif args.command == "export":
            if args.refresh:
                aps.fetch_scripts_md(force_refresh=True)
            aps.export_json(args.output)
            print(f"✓ 数据已导出到: {args.output}")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
