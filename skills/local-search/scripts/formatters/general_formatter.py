#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用格式化器 - 默认搜索结果格式化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from formatters.base_formatter import BaseFormatter
from engines.base import SearchResult
from typing import List


class GeneralFormatter(BaseFormatter):
    """通用搜索结果格式化器"""

    def format(self, results: List[SearchResult], **kwargs) -> str:
        """
        格式化通用搜索结果

        Args:
            results: 搜索结果列表
            query: 搜索关键词（可选）
            show_source: 是否显示来源（默认True）
            show_score: 是否显示评分（默认False）

        Returns:
            str: 格式化后的字符串
        """
        query = kwargs.get('query', '')
        show_source = kwargs.get('show_source', True)
        show_score = kwargs.get('show_score', False)

        lines = []

        # 标题
        if query:
            lines.append(f"🔍 搜索: {query}")

        lines.append(f"📊 找到 {len(results)} 条结果\n")

        # 结果列表
        for i, result in enumerate(results, 1):
            lines.append(f"**{i}. {result.title}**")
            lines.append(f"   {result.url}")

            # 来源信息
            if show_source:
                source_tag = f"[{result.source}]"
                if show_score:
                    source_tag += f" 评分:{result.score:.1f}"
                lines.append(f"   来源: {source_tag}")

            # 摘要
            snippet = self._safe_truncate(result.snippet, 120)
            if snippet:
                lines.append(f"   {snippet}")

            lines.append("")

        return "\n".join(lines)


# 测试代码
if __name__ == "__main__":
    from engines.base import SearchResult

    # 创建测试数据
    test_results = [
        SearchResult(
            title="武汉天气预报 - 中国天气网",
            url="http://www.weather.com.cn/weather/101200101.shtml",
            snippet="武汉今日天气：晴转多云，气温11℃/-1℃，风力<3级。明天天气预报...",
            source="百度",
            score=3.5
        ),
        SearchResult(
            title="Wuhan Weather Forecast",
            url="https://weather.com/weather/today/l/Wuhan+China",
            snippet="Today's weather in Wuhan. High 11°C, Low -1°C. Sunny to cloudy...",
            source="Google",
            score=3.0
        ),
    ]

    formatter = GeneralFormatter()
    output = formatter.format(test_results, query="武汉天气", show_score=True)
    print(output)
