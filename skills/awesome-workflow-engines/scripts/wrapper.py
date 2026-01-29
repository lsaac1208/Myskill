#!/usr/bin/env python3
"""
Awesome Workflow Engines 列表查询工具
提供对 meirwah/awesome-workflow-engines 列表的查询和搜索功能
"""

import subprocess
import json
import sys
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.request import urlopen
from urllib.error import URLError


class AwesomeWorkflowEngines:
    """Awesome Workflow Engines 列表的 Python 封装类"""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化 Awesome Workflow Engines 查询工具

        Args:
            cache_dir: 缓存目录
        """
        self.repo_url = "https://github.com/meirwah/awesome-workflow-engines"
        self.raw_url = "https://raw.githubusercontent.com/meirwah/awesome-workflow-engines/master/README.md"
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".cache" / "awesome-workflow-engines"
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

    def parse_engines(self, content: str) -> List[Dict[str, Any]]:
        """
        解析 README 中的工作流引擎

        Args:
            content: README 内容

        Returns:
            工作流引擎列表
        """
        engines = []

        for line in content.split('\n'):
            # 匹配格式: * [EngineName](url) [![Stars](badge)] - Description
            match = re.match(
                r'^\*\s+\[([^\]]+)\]\(([^)]+)\)\s+(\[!\[Stars\]\([^\)]+\)\])?\s*-\s+(.+)$',
                line
            )
            if match:
                engine_name = match.group(1)
                engine_url = match.group(2)
                engine_desc = match.group(4)

                engines.append({
                    "name": engine_name,
                    "url": engine_url,
                    "description": engine_desc
                })

        return engines

    def list_engines(self) -> List[Dict[str, Any]]:
        """
        列出所有工作流引擎

        Returns:
            工作流引擎列表
        """
        content = self.fetch_readme()
        return self.parse_engines(content)

    def search_engines(self, query: str) -> List[Dict[str, Any]]:
        """
        搜索工作流引擎

        Args:
            query: 搜索关键词

        Returns:
            匹配的工作流引擎列表
        """
        engines = self.list_engines()
        results = []
        query_lower = query.lower()

        for engine in engines:
            if (query_lower in engine["name"].lower() or
                query_lower in engine["description"].lower()):
                results.append(engine)

        return results

    def get_engine_info(self, engine_name: str) -> Optional[Dict[str, Any]]:
        """
        获取工作流引擎详细信息

        Args:
            engine_name: 引擎名称

        Returns:
            工作流引擎信息
        """
        engines = self.list_engines()

        for engine in engines:
            if engine["name"].lower() == engine_name.lower():
                return engine

        return None

    def get_popular_engines(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取热门工作流引擎

        Args:
            limit: 返回数量

        Returns:
            热门工作流引擎列表
        """
        # 基于知名度的精选列表
        popular_engines = [
            {"name": "Airflow", "description": "Python-based 平台，运行 DAGs 任务", "language": "Python"},
            {"name": "Argo Workflows", "description": "Kubernetes 原生工作流引擎", "language": "Go"},
            {"name": "Cadence", "description": "Uber 开发的异步长流程业务逻辑编排引擎", "language": "Go"},
            {"name": "Dagster", "description": "数据编排器，用于 ML、分析和 ETL", "language": "Python"},
            {"name": "Prefect", "description": "现代工作流编排系统", "language": "Python"},
            {"name": "Temporal", "description": "Cadence 的开源版本", "language": "Go"},
            {"name": "Flyte", "description": "Kubernetes 原生的类型安全工作流平台", "language": "Go"},
            {"name": "Kubeflow Pipelines", "description": "Kubernetes 上的 ML 工作流", "language": "Go"},
            {"name": "Luigi", "description": "Python 任务批处理依赖管理工具", "language": "Python"},
            {"name": "Apache DolphinScheduler", "description": "分布式易扩展的可视化工作流任务调度系统", "language": "Java"},
        ]

        return popular_engines[:limit]

    def get_engines_by_language(self, language: str) -> List[Dict[str, Any]]:
        """
        按编程语言筛选工作流引擎

        Args:
            language: 编程语言

        Returns:
            工作流引擎列表
        """
        engines = self.list_engines()
        results = []
        language_lower = language.lower()

        for engine in engines:
            # 在名称或描述中查找语言特征
            if language_lower in engine["name"].lower() or \
               language_lower in engine["description"].lower():
                results.append(engine)

        return results

    def export_json(self, output_file: str) -> None:
        """
        导出数据为 JSON

        Args:
            output_file: 输出文件路径
        """
        engines = self.list_engines()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(engines, f, indent=2, ensure_ascii=False)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Awesome Workflow Engines 查询工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 列出引擎
    list_parser = subparsers.add_parser("list", help="列出所有工作流引擎")
    list_parser.add_argument("--format", choices=["table", "json"], default="table",
                          help="输出格式")

    # 搜索引擎
    search_parser = subparsers.add_parser("search", help="搜索工作流引擎")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--format", choices=["table", "json"], default="table",
                             help="输出格式")

    # 获取引擎信息
    info_parser = subparsers.add_parser("info", help="获取工作流引擎详细信息")
    info_parser.add_argument("engine", help="引擎名称")

    # 按语言筛选
    lang_parser = subparsers.add_parser("language", help="按编程语言筛选")
    lang_parser.add_argument("language", help="编程语言")
    lang_parser.add_argument("--format", choices=["table", "json"], default="table",
                            help="输出格式")

    # 热门引擎
    popular_parser = subparsers.add_parser("popular", help="获取热门工作流引擎")
    popular_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    # 导出
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("output", help="输出文件路径")
    export_parser.add_argument("--refresh", action="store_true", help="强制刷新")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    awesome = AwesomeWorkflowEngines()

    try:
        if args.command == "list":
            engines = awesome.list_engines()

            if args.format == "json":
                print(json.dumps(engines, indent=2, ensure_ascii=False))
            else:
                print(f"工作流引擎列表 (共 {len(engines)} 个):")
                for engine in engines:
                    print(f"  {engine['name']}")
                    print(f"    {engine['description']}")

        elif args.command == "search":
            results = awesome.search_engines(args.query)

            if args.format == "json":
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                print(f"搜索 '{args.query}' 的结果:")
                for engine in results:
                    print(f"  {engine['name']}")
                    print(f"    {engine['description']}")
                    print(f"    链接: {engine['url']}")

        elif args.command == "info":
            info = awesome.get_engine_info(args.engine)
            if info:
                print(json.dumps(info, indent=2, ensure_ascii=False))
            else:
                print(f"未找到工作流引擎: {args.engine}", file=sys.stderr)
                sys.exit(1)

        elif args.command == "language":
            engines = awesome.get_engines_by_language(args.language)

            if args.format == "json":
                print(json.dumps(engines, indent=2, ensure_ascii=False))
            else:
                print(f"{args.language} 工作流引擎:")
                for engine in engines:
                    print(f"  {engine['name']} - {engine['description']}")

        elif args.command == "popular":
            engines = awesome.get_popular_engines(args.limit)
            print("热门工作流引擎:")
            for engine in engines:
                print(f"  {engine['name']} - {engine['description']}")
                print(f"    语言: {engine.get('language', 'N/A')}")

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
