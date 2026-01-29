#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google 搜索引擎实现
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engines.base import BaseSearchEngine, SearchResult
from typing import List
import time

try:
    from googlesearch import search as google_search
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


class GoogleSearchEngine(BaseSearchEngine):
    """Google 搜索引擎"""

    def __init__(self, timeout: int = 30):
        super().__init__("Google", timeout)
        self.available = GOOGLE_AVAILABLE

    def is_available(self) -> bool:
        """检查 Google 搜索是否可用"""
        return self.available

    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        使用 Google 搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            List[SearchResult]: 搜索结果列表
        """
        if not self.is_available():
            print(f"⚠️  Google 搜索不可用（未安装 googlesearch-python）")
            return []

        results = []
        try:
            # 执行搜索（新版本 API）
            # googlesearch-python 返回的结果对象包含标题、URL和描述
            search_results = google_search(
                term=query,
                num_results=max_results,
                lang="zh-CN",
                region="CN",
                advanced=True,  # 使用高级模式获取更多信息
                sleep_interval=2,
                timeout=self.timeout
            )

            for result in search_results:
                sr = SearchResult(
                    title=result.title if hasattr(result, 'title') else "",
                    url=result.url if hasattr(result, 'url') else "",
                    snippet=result.description if hasattr(result, 'description') else "",
                    source=self.name
                )
                results.append(sr)

            # 稍作延迟避免被封
            time.sleep(1)

        except Exception as e:
            print(f"⚠️  Google 搜索失败: {e}")

        return results


# 测试代码
if __name__ == "__main__":
    engine = GoogleSearchEngine()

    if not engine.is_available():
        print("Google 搜索引擎不可用，请安装: pip install googlesearch-python")
    else:
        print("=== Google 搜索测试 ===\n")
        results = engine.search("武汉天气", max_results=5)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.title}")
            print(f"   {r.url}")
            print(f"   {r.snippet[:80]}...")
            print()
