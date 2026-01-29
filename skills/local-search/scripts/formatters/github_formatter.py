#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 格式化器 - GitHub 搜索结果格式化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from formatters.base_formatter import BaseFormatter
from engines.base import SearchResult
from typing import List


class GitHubFormatter(BaseFormatter):
    """GitHub 搜索结果格式化器"""

    def format(self, results: List[SearchResult], **kwargs) -> str:
        """
        格式化 GitHub 搜索结果

        Args:
            results: 搜索结果列表
            query: 搜索关键词（可选）

        Returns:
            str: 格式化后的字符串
        """
        query = kwargs.get('query', '')
        show_stats = kwargs.get('show_stats', True)

        lines = []

        # 标题
        lines.append(f"🔧 GitHub 搜索")
        if query:
            lines.append(f"关键词: {query}")
        lines.append(f"共找到 {len(results)} 条结果\n")

        # 按来源分组（仓库/代码/Issue等）
        grouped = self._group_by_source(results)

        for source, items in grouped.items():
            # 显示来源分组
            if source != "GitHub":
                lines.append(f"### {source}")
            else:
                lines.append("### 仓库")
            lines.append("")

            # 显示结果
            for item in items:
                lines.append(f"**{item.title}**")
                lines.append(f"🔗 {item.url}")

                # 显示统计信息
                if show_stats and item.snippet:
                    lines.append(f"📊 {item.snippet}")

                # 显示日期
                if item.date:
                    lines.append(f"📅 更新: {item.date}")

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
            title="python-search",
            url="https://github.com/user/python-search",
            snippet="⭐ 1234 | 语言: Python | 一个强大的搜索库",
            source="GitHub",
            date="2025-01-20"
        ),
        SearchResult(
            title="Fix search bug",
            url="https://github.com/user/repo/issues/42",
            snippet="搜索功能在某些情况下会崩溃...",
            source="GitHub/Issue",
            date="2025-01-22"
        ),
    ]

    formatter = GitHubFormatter()
    output = formatter.format(test_results, query="python search", show_stats=True)
    print(output)
