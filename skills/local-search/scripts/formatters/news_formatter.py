#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻格式化器 - 新闻搜索结果格式化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from formatters.base_formatter import BaseFormatter
from engines.base import SearchResult
from typing import List
from datetime import datetime


class NewsFormatter(BaseFormatter):
    """新闻格式化器"""

    def format(self, results: List[SearchResult], **kwargs) -> str:
        """
        格式化新闻搜索结果

        Args:
            results: 搜索结果列表
            date: 日期（可选）
            location: 地点（可选）

        Returns:
            str: 格式化后的字符串
        """
        date = kwargs.get('date', datetime.now().strftime('%Y-%m-%d'))
        location = kwargs.get('location', '')

        lines = []

        # 标题
        lines.append(f"📰 今日新闻（{date}）")
        if location:
            lines.append(f"📍 地区: {location}")
        lines.append("")

        # 按来源分组
        grouped = self._group_by_source(results)

        # 输出新闻
        for source, items in grouped.items():
            lines.append(f"### 来自 {source}")
            lines.append("")
            for item in items:
                lines.append(f"- [{item.title}]({item.url})")
                if item.snippet:
                    snippet = self._safe_truncate(item.snippet, 100)
                    lines.append(f"  {snippet}")
            lines.append("")

        return "\n".join(lines)

    def _group_by_source(self, results: List[SearchResult]) -> dict:
        """按来源分组"""
        grouped = {}
        for result in results:
            source = result.source
            if source not in grouped:
                grouped[source] = []
            grouped[source].append(result)
        return grouped


# 测试代码
if __name__ == "__main__":
    from engines.base import SearchResult

    # 创建测试数据
    test_results = [
        SearchResult(
            title="习近平主席会见美国总统拜登",
            url="http://news.cctv.com/2025/01/24/xxx",
            snippet="国家主席习近平在人民大会堂会见美国总统拜登，双方就中美关系等问题深入交换意见。",
            source="央视网"
        ),
        SearchResult(
            title="2025年科技行业展望：AI将成为主流",
            url="http://36kr.com/p/xxxx",
            snippet="随着ChatGPT等大模型的普及，AI将在2025年全面进入各行各业...",
            source="36Kr"
        ),
    ]

    formatter = NewsFormatter()
    output = formatter.format(test_results, date="2025-01-24", location="全国")
    print(output)
