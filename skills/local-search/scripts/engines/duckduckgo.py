#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DuckDuckGo 搜索引擎实现
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engines.base import BaseSearchEngine, SearchResult
from typing import List
import time

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


class DuckDuckGoSearchEngine(BaseSearchEngine):
    """DuckDuckGo 搜索引擎"""

    def __init__(self, timeout: int = 30):
        super().__init__("DuckDuckGo", timeout)
        self.available = DDGS_AVAILABLE

    def is_available(self) -> bool:
        """检查 DuckDuckGo 搜索是否可用"""
        return self.available

    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        使用 DuckDuckGo 搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            List[SearchResult]: 搜索结果列表
        """
        if not self.is_available():
            print(f"⚠️  DuckDuckGo 搜索不可用（未安装 ddgs）")
            return []

        results = []
        try:
            ddgs = DDGS()

            # 执行搜索
            raw_results = ddgs.text(
                query,
                max_results=max_results
            )

            # 转换为标准格式
            for item in raw_results:
                result = SearchResult(
                    title=item.get('title', ''),
                    url=item.get('href', ''),
                    snippet=item.get('body', ''),
                    source=self.name
                )
                results.append(result)

            # 稍作延迟
            time.sleep(0.5)

        except Exception as e:
            print(f"⚠️  DuckDuckGo 搜索失败: {e}")

        return results


# 测试代码
if __name__ == "__main__":
    engine = DuckDuckGoSearchEngine()

    if not engine.is_available():
        print("DuckDuckGo 搜索引擎不可用，请安装: pip install ddgs")
    else:
        print("=== DuckDuckGo 搜索测试 ===\n")
        results = engine.search("武汉天气", max_results=5)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.title}")
            print(f"   {r.url}")
            print(f"   {r.snippet[:80]}...")
            print()
