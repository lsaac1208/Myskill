#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地搜索工具 - 增强版
支持智能意图识别、多引擎搜索、结果格式化
完全不消耗 GLM MCP 额度
"""

import sys
import os
import json
import argparse

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 导入模块
from intent.recognizer import IntentRecognizer
from aggregators.search_aggregator import SearchAggregator
from formatters.general_formatter import GeneralFormatter
from formatters.news_formatter import NewsFormatter
from formatters.weather_formatter import WeatherFormatter
from formatters.github_formatter import GitHubFormatter
from engines.github import GitHubSearchEngine


def github_search(query: str, max_results: int = 10, search_type: str = "repos", quiet: bool = False):
    """
    执行 GitHub 搜索

    Args:
        query: 搜索关键词
        max_results: 最大结果数量
        search_type: 搜索类型 (repos/code/issues/prs/users)
        quiet: 简洁模式（减少调试信息）
    """
    if not quiet:
        print(f"🔧 GitHub 搜索: {query}")
        print(f"📋 搜索类型: {search_type}\n")

    engine = GitHubSearchEngine()

    if not engine.is_available():
        print("❌ GitHub 搜索不可用，请安装 GitHub CLI")
        print("   安装方法: brew install gh")
        return

    results = engine.search(query, max_results=max_results, search_type=search_type)

    if not results:
        print("❌ 未找到搜索结果")
        return

    if not quiet:
        print(f"✅ 找到 {len(results)} 条结果\n")
        print("-" * 50)
        print()

    # 格式化输出
    formatter = GitHubFormatter()
    output = formatter.format(results, query=query, show_stats=True)
    print(output)


def search(
    query: str,
    max_results: int = 10,
    output_json: bool = False,
    engines: list = None,
    quiet: bool = False
):
    """
    执行智能搜索

    Args:
        query: 搜索关键词
        max_results: 最大结果数量
        output_json: 是否输出 JSON 格式
        engines: 指定使用的搜索引擎
        quiet: 简洁模式（减少调试信息）
    """
    if not quiet:
        print(f"🔍 本地搜索: {query}\n")

    # 1. 意图识别
    recognizer = IntentRecognizer()
    intent = recognizer.recognize(query)

    if not quiet:
        print(f"📌 意图识别: {intent.intent_type} (置信度: {intent.confidence:.2f})")
        print(f"📍 位置: {intent.location}")
        print(f"🕐 时间范围: {intent.time_range}")
        print(f"🔑 优化搜索词: {intent.refined_query}")
        print()

    # 2. 执行搜索
    aggregator = SearchAggregator()

    # 显示可用引擎
    if not quiet:
        available = aggregator.get_available_engines()
        status_list = []
        for n, a in available.items():
            status = "✅" if a else "❌"
            status_list.append(f"{n}({status})")
        print(f"🌐 搜索引擎状态: {', '.join(status_list)}")
        print()

    # 使用优化后的搜索词
    search_query = intent.refined_query if intent.refined_query else intent.query

    results = aggregator.search(
        search_query,
        max_results=max_results,
        engines=engines
    )

    if not results:
        print("❌ 未找到搜索结果")
        return

    if not quiet:
        print(f"✅ 找到 {len(results)} 条结果（已去重、排序）\n")
        print("-" * 50)
        print()

    # 3. 格式化输出
    if output_json:
        # JSON 格式
        output = [r.to_dict() for r in results]
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 根据意图类型选择格式化器
        if intent.intent_type == "news":
            formatter = NewsFormatter()
            output = formatter.format(
                results,
                date=intent.time_range,
                location=intent.location
            )
        elif intent.intent_type == "weather":
            formatter = WeatherFormatter()
            output = formatter.format(
                results,
                location=intent.location
            )
        elif intent.intent_type == "github":
            formatter = GitHubFormatter()
            output = formatter.format(
                results,
                query=query,
                show_stats=True
            )
        else:
            formatter = GeneralFormatter()
            output = formatter.format(
                results,
                query=query,
                show_source=True,
                show_score=True
            )

        print(output)


def main():
    parser = argparse.ArgumentParser(
        description="本地搜索工具 - 增强版，不消耗 GLM MCP 额度",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s search "武汉天气"           # 自动识别为天气查询
  %(prog)s search "今天的新闻"         # 自动识别为新闻查询
  %(prog)s search "AI 最新进展" -n 20  # 通用搜索，返回20条结果
  %(prog)s search "Python 教程" --json # JSON 格式输出
  %(prog)s search "深度学习" -e google baidu  # 指定搜索引擎
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # Search 命令
    search_parser = subparsers.add_parser("search", help="执行搜索")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("-n", "--results", type=int, default=10,
                              help="结果数量（默认: 10）")
    search_parser.add_argument("--json", action="store_true",
                              help="输出 JSON 格式")
    search_parser.add_argument("-e", "--engines", nargs='+',
                              help="指定搜索引擎 (google baidu duckduckgo github)")
    search_parser.add_argument("-q", "--quiet", action="store_true",
                              help="简洁模式（减少调试信息）")

    # GitHub 搜索命令
    github_parser = subparsers.add_parser("github", help="GitHub 专用搜索")
    github_parser.add_argument("query", help="搜索关键词")
    github_parser.add_argument("-n", "--results", type=int, default=10,
                              help="结果数量（默认: 10）")
    github_parser.add_argument("-t", "--type", default="repos",
                              choices=["repos", "code", "issues", "prs", "users"],
                              help="搜索类型（默认: repos）")
    github_parser.add_argument("-q", "--quiet", action="store_true",
                              help="简洁模式（减少调试信息）")

    # 测试命令
    test_parser = subparsers.add_parser("test", help="测试功能")
    test_parser.add_argument("--intent", action="store_true", help="测试意图识别")
    test_parser.add_argument("--engines", action="store_true", help="测试搜索引擎")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        quiet = getattr(args, 'quiet', False)
        search(args.query, args.results, args.json, args.engines, quiet)

    elif args.command == "github":
        quiet = getattr(args, 'quiet', False)
        github_search(args.query, args.results, args.type, quiet)

    elif args.command == "test":
        if args.intent:
            test_intent()
        elif args.engines:
            test_engines()
        else:
            test_all()


def test_intent():
    """测试意图识别"""
    print("=== 意图识别测试 ===\n")
    recognizer = IntentRecognizer()

    test_queries = [
        "今天的新闻",
        "武汉今天天气怎么样",
        "查一下 AI 的最新进展",
        "百度搜索 深度学习",
        "今日头条新闻",
        "有什么新闻"
    ]

    for query in test_queries:
        intent = recognizer.recognize(query)
        print(f"查询: {query}")
        print(f"  类型: {intent.intent_type} (置信度: {intent.confidence:.2f})")
        print(f"  优化词: {intent.refined_query}")
        print()


def test_engines():
    """测试搜索引擎"""
    print("=== 搜索引擎测试 ===\n")
    aggregator = SearchAggregator()

    available = aggregator.get_available_engines()
    print("可用搜索引擎:")
    for name, is_avail in available.items():
        status = "✅" if is_avail else "❌"
        print(f"  {status} {name}")
    print()

    # 测试搜索
    print("测试搜索 '武汉天气':\n")
    results = aggregator.search("武汉天气", max_results=3)

    for i, r in enumerate(results, 1):
        print(f"{i}. [{r.source}] {r.title}")
        print(f"   {r.url[:60]}...")
        print()


def test_all():
    """运行所有测试"""
    test_intent()
    print("\n" + "="*50 + "\n")
    test_engines()


if __name__ == "__main__":
    main()
