#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度搜索引擎实现（自定义爬虫）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engines.base import BaseSearchEngine, SearchResult
from typing import List
import time
import urllib.parse
import re

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class BaiduSearchEngine(BaseSearchEngine):
    """百度搜索引擎"""

    BAIDU_SEARCH_URL = "https://www.baidu.com/s"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    def __init__(self, timeout: int = 30):
        super().__init__("百度", timeout)
        self.available = REQUESTS_AVAILABLE

    def is_available(self) -> bool:
        """检查百度搜索是否可用"""
        return self.available

    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        使用百度搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            List[SearchResult]: 搜索结果列表
        """
        if not self.is_available():
            print(f"⚠️  百度搜索不可用（需要 requests 和 beautifulsoup4）")
            return []

        results = []
        try:
            # 构建搜索参数
            params = {
                "wd": query,
                "rn": max_results,
                "ie": "utf-8"
            }

            # 发送请求
            response = requests.get(
                self.BAIDU_SEARCH_URL,
                params=params,
                headers=self.HEADERS,
                timeout=self.timeout
            )
            response.raise_for_status()
            response.encoding = 'utf-8'

            # 解析结果
            soup = BeautifulSoup(response.text, 'html.parser')

            # 百度搜索结果通常在 .result 容器中
            result_divs = soup.find_all('div', class_='result')

            for div in result_divs[:max_results]:
                result = self._parse_baidu_result(div)
                if result:
                    results.append(result)

            # 避免频繁请求
            time.sleep(1)

        except requests.exceptions.Timeout:
            print(f"⚠️  百度搜索超时")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  百度搜索请求失败: {e}")
        except Exception as e:
            print(f"⚠️  百度搜索解析失败: {e}")

        return results

    def _parse_baidu_result(self, div) -> SearchResult:
        """解析单个百度搜索结果"""
        try:
            # 获取标题和链接
            h3 = div.find('h3')
            if not h3:
                return None

            a_tag = h3.find('a')
            if not a_tag:
                return None

            title = a_tag.get_text(strip=True)
            url = a_tag.get('href', '')

            # 清理百度链接（去除跳转链接）
            url = self._clean_baidu_url(url)

            # 获取摘要
            summary_div = div.find('div', class_='c-abstract')
            if not summary_div:
                summary_div = div.find('div', class_='c-span-last')

            snippet = ""
            if summary_div:
                snippet = summary_div.get_text(strip=True)

            return SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=self.name
            )

        except Exception:
            return None

    def _clean_baidu_url(self, url: str) -> str:
        """清理百度跳转链接"""
        try:
            # 百度链接格式: http://www.baidu.com/link?url=xxxxx
            if 'baidu.com/link?url=' in url:
                # 尝试提取真实 URL（这里简化处理，实际需要解析跳转）
                # 更好的方式是请求该链接并跟踪重定向
                return url
            return url
        except Exception:
            return url


# 测试代码
if __name__ == "__main__":
    engine = BaiduSearchEngine()

    if not engine.is_available():
        print("百度搜索引擎不可用，请安装: pip install requests beautifulsoup4")
    else:
        print("=== 百度搜索测试 ===\n")
        results = engine.search("武汉天气", max_results=5)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.title}")
            print(f"   {r.url}")
            print(f"   {r.snippet[:80]}...")
            print()
