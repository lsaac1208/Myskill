#!/usr/bin/env python3
"""
GitHubDaily 资源查询工具
提供对 GitHubDaily/GitHubDaily 资源库的查询和搜索功能
"""

import subprocess
import json
import sys
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.request import urlopen
from urllib.error import URLError


class GitHubDaily:
    """GitHubDaily 资源库的 Python 封装类"""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化 GitHubDaily 查询工具

        Args:
            cache_dir: 缓存目录
        """
        self.repo_url = "https://github.com/GitHubDaily/GitHubDaily"
        self.raw_url_base = "https://raw.githubusercontent.com/GitHubDaily/GitHubDaily/master"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".cache" / "githubdaily"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_file(self, filename: str, force_refresh: bool = False) -> str:
        """
        获取文件内容

        Args:
            filename: 文件名
            force_refresh: 是否强制刷新

        Returns:
            文件内容
        """
        cache_file = self.cache_dir / filename

        # 检查缓存
        if not force_refresh and cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()

        # 从网络获取
        url = f"{self.raw_url_base}/{filename}"
        try:
            with urlopen(url, timeout=10) as response:
                content = response.read().decode('utf-8')

            # 保存到缓存
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(content)

            return content
        except URLError as e:
            if cache_file.exists():
                print(f"网络错误，使用缓存: {e}", file=sys.stderr)
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            raise RuntimeError(f"无法获取文件 {filename}: {e}")

    def parse_yearly_projects(self, year: str) -> List[Dict[str, Any]]:
        """
        解析年度项目列表

        Args:
            year: 年份

        Returns:
            项目列表
        """
        content = self.fetch_file(f"{year}.md")
        projects = []

        # 解析表格格式
        current_category = None

        for line in content.split('\n'):
            # 匹配分类标题 (### 分类名)
            category_match = re.match(r'^###\s+(.+)$', line)
            if category_match:
                current_category = category_match.group(1).strip()
                continue

            # 匹配项目条目 | 项目 | 简述 | ...
            if '|' in line and '项目' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    project_name = parts[1]
                    project_desc = parts[2] if len(parts) > 2 else ""

                    # 提取链接
                    link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', project_name)
                    if link_match:
                        name = link_match.group(1)
                        url = link_match.group(2)
                    else:
                        name = project_name
                        url = ""

                    if name:
                        projects.append({
                            "name": name,
                            "url": url,
                            "description": project_desc,
                            "category": current_category or "未分类",
                            "year": year
                        })

        return projects

    def list_categories_by_year(self, year: str) -> List[str]:
        """
        列出指定年份的分类

        Args:
            year: 年份

        Returns:
            分类列表
        """
        projects = self.parse_yearly_projects(year)
        categories = set()
        for project in projects:
            if project["category"]:
                categories.add(project["category"])
        return sorted(list(categories))

    def search_projects(
        self,
        query: str,
        year: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索项目

        Args:
            query: 搜索关键词
            year: 限定年份
            category: 限定分类

        Returns:
            匹配的项目列表
        """
        # 如果没有指定年份，搜索最近几年
        years = [year] if year else ["2025", "2024", "2023", "2022"]

        results = []
        query_lower = query.lower()

        for y in years:
            try:
                projects = self.parse_yearly_projects(y)

                for project in projects:
                    # 应用分类筛选
                    if category and project["category"] != category:
                        continue

                    # 搜索匹配
                    if (query_lower in project["name"].lower() or
                        query_lower in project["description"].lower()):
                        results.append(project)
            except Exception:
                continue

        return results

    def get_project_info(self, project_name: str) -> Optional[Dict[str, Any]]:
        """
        获取项目详细信息

        Args:
            project_name: 项目名称

        Returns:
            项目信息
        """
        results = self.search_projects(project_name)
        for result in results:
            if result["name"].lower() == project_name.lower():
                return result
        return None

    def get_trending_projects(self, year: str = "2025", limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取热门项目

        Args:
            year: 年份
            limit: 返回数量

        Returns:
            热门项目列表
        """
        try:
            projects = self.parse_yearly_projects(year)
            return projects[:limit]
        except Exception:
            return []

    def get_projects_by_category(
        self,
        category: str,
        year: str = "2025"
    ) -> List[Dict[str, Any]]:
        """
        获取指定分类的项目

        Args:
            category: 分类名称
            year: 年份

        Returns:
            项目列表
        """
        projects = self.parse_yearly_projects(year)
        return [p for p in projects if p["category"] == category]

    def export_json(self, output_file: str, year: str = "2025") -> None:
        """
        导出数据为 JSON

        Args:
            output_file: 输出文件路径
            year: 年份
        """
        projects = self.parse_yearly_projects(year)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="GitHubDaily 资源查询工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 列出分类
    list_parser = subparsers.add_parser("list", help="列出分类")
    list_parser.add_argument("--year", default="2025", help="年份")

    # 搜索项目
    search_parser = subparsers.add_parser("search", help="搜索项目")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--year", help="限定年份")
    search_parser.add_argument("--category", help="限定分类")
    search_parser.add_argument("--format", choices=["table", "json"], default="table",
                             help="输出格式")

    # 获取分类项目
    category_parser = subparsers.add_parser("category", help="获取指定分类的项目")
    category_parser.add_argument("category", help="分类名称")
    category_parser.add_argument("--year", default="2025", help="年份")
    category_parser.add_argument("--format", choices=["table", "json"], default="table",
                               help="输出格式")

    # 获取项目信息
    info_parser = subparsers.add_parser("info", help="获取项目详细信息")
    info_parser.add_argument("project", help="项目名称")

    # 热门项目
    trending_parser = subparsers.add_parser("trending", help="获取热门项目")
    trending_parser.add_argument("--year", default="2025", help="年份")
    trending_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    # 导出
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("output", help="输出文件路径")
    export_parser.add_argument("--year", default="2025", help="年份")
    export_parser.add_argument("--refresh", action="store_true", help="强制刷新")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    ghd = GitHubDaily()

    try:
        if args.command == "list":
            categories = ghd.list_categories_by_year(args.year)
            print(f"{args.year} 年分类:")
            for cat in categories:
                print(f"  {cat}")

        elif args.command == "search":
            results = ghd.search_projects(args.query, args.year, args.category)

            if args.format == "json":
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                print(f"搜索 '{args.query}' 的结果:")
                for project in results:
                    print(f"  {project['name']} - {project['description']}")
                    print(f"    分类: {project['category']}")
                    if project['url']:
                        print(f"    链接: {project['url']}")

        elif args.command == "category":
            projects = ghd.get_projects_by_category(args.category, args.year)

            if args.format == "json":
                print(json.dumps(projects, indent=2, ensure_ascii=False))
            else:
                print(f"分类 '{args.category}' 的项目:")
                for project in projects:
                    print(f"  {project['name']} - {project['description']}")
                    if project['url']:
                        print(f"    链接: {project['url']}")

        elif args.command == "info":
            info = ghd.get_project_info(args.project)
            if info:
                print(json.dumps(info, indent=2, ensure_ascii=False))
            else:
                print(f"未找到项目: {args.project}", file=sys.stderr)
                sys.exit(1)

        elif args.command == "trending":
            projects = ghd.get_trending_projects(args.year, args.limit)
            print(f"{args.year} 年热门项目:")
            for project in projects:
                print(f"  {project['name']} - {project['description']}")
                print(f"    分类: {project['category']}")

        elif args.command == "export":
            if args.refresh:
                ghd.fetch_file(f"{args.year}.md", force_refresh=True)
            ghd.export_json(args.output, args.year)
            print(f"✓ 数据已导出到: {args.output}")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
