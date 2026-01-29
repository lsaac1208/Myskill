#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索聚合器 - 多引擎搜索聚合
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engines.base import SearchResult
from engines.google import GoogleSearchEngine
from engines.baidu import BaiduSearchEngine
from engines.duckduckgo import DuckDuckGoSearchEngine
from engines.github import GitHubSearchEngine
from typing import List, Dict, Optional
from config import SEARCH_ENGINES


class SearchAggregator:
    """搜索聚合器 - 整合多个搜索引擎的结果"""

    def __init__(self):
        # 初始化所有搜索引擎
        self.engines = {
            "google": GoogleSearchEngine(),
            "baidu": BaiduSearchEngine(),
            "duckduckgo": DuckDuckGoSearchEngine(),
            "github": GitHubSearchEngine()
        }

    def search(
        self,
        query: str,
        max_results: int = 10,
        engines: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """
        多引擎搜索聚合

        Args:
            query: 搜索关键词
            max_results: 每个引擎的最大结果数
            engines: 指定使用的搜索引擎列表，None 则使用所有可用引擎

        Returns:
            List[SearchResult]: 聚合后的搜索结果
        """
        if engines is None:
            # 使用配置中启用的所有引擎
            engines = [
                name for name, config in SEARCH_ENGINES.items()
                if config.get("enabled", True)
            ]

        all_results = []

        # 按优先级排序搜索引擎
        engines_with_priority = [
            (name, SEARCH_ENGINES.get(name, {}).get("priority", 0))
            for name in engines
        ]
        engines_sorted = [e[0] for e in sorted(engines_with_priority, key=lambda x: -x[1])]

        # 依次执行搜索
        for engine_name in engines_sorted:
            if engine_name not in self.engines:
                continue

            engine = self.engines[engine_name]
            if not engine.is_available():
                print(f"⚠️  {engine.name} 不可用，跳过")
                continue

            print(f"🔍 使用 {engine.name} 搜索...")
            results = engine.search(query, max_results)
            all_results.extend(results)

        # 去重和排序
        unique_results = self._deduplicate(all_results)
        ranked_results = self._rank_by_relevance(unique_results, query)

        return ranked_results

    def _deduplicate(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        结果去重（基于 URL）

        Args:
            results: 原始结果列表

        Returns:
            List[SearchResult]: 去重后的结果
        """
        seen_urls = set()
        unique = []

        for result in results:
            # 标准化 URL（去除协议、www、尾部斜杠等）
            normalized_url = self._normalize_url(result.url)

            if normalized_url not in seen_urls:
                seen_urls.add(normalized_url)
                unique.append(result)

        return unique

    def _normalize_url(self, url: str) -> str:
        """标准化 URL 用于去重"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            # 返回 netloc + path（忽略协议和参数）
            return f"{parsed.netloc}{parsed.path}".rstrip('/').lower()
        except Exception:
            return url.lower()

    def _rank_by_relevance(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """
        按相关性排序结果

        Args:
            results: 结果列表
            query: 原始查询

        Returns:
            List[SearchResult]: 排序后的结果
        """
        # 简单的相关性评分：标题和摘要中包含查询词的次数
        query_lower = query.lower()

        for result in results:
            score = 0
            title_lower = result.title.lower()
            snippet_lower = result.snippet.lower()

            # 标题匹配权重更高
            score += title_lower.count(query_lower) * 3
            score += snippet_lower.count(query_lower)

            # 来源引擎权重
            engine_weights = {
                "Google": 1.5,
                "百度": 1.2,
                "DuckDuckGo": 1.0,
                "GitHub": 2.0
            }
            score *= engine_weights.get(result.source, 1.0)

            result.score = score

        # 按分数降序排序
        return sorted(results, key=lambda r: r.score, reverse=True)

    def get_available_engines(self) -> Dict[str, bool]:
        """获取所有搜索引擎的可用状态"""
        return {
            name: engine.is_available()
            for name, engine in self.engines.items()
        }


# 测试代码
if __name__ == "__main__":
    aggregator = SearchAggregator()

    print("=== 可用搜索引擎 ===")
    available = aggregator.get_available_engines()
    for name, is_avail in available.items():
        status = "✅" if is_avail else "❌"
        print(f"{status} {name}")

    print("\n=== 多引擎搜索测试 ===")
    results = aggregator.search("武汉天气", max_results=5)

    print(f"\n共找到 {len(results)} 条结果（已去重、排序）\n")
    for i, r in enumerate(results[:10], 1):
        print(f"{i}. [{r.source}] {r.title}")
        print(f"   {r.url}")
        print(f"   评分: {r.score:.1f} | {r.snippet[:60]}...")
        print()
