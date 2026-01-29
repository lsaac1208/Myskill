#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索引擎基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class SearchResult:
    """搜索结果数据类"""
    title: str           # 标题
    url: str             # 链接
    snippet: str         # 摘要
    source: str          # 来源搜索引擎
    date: Optional[str] = None  # 发布日期
    score: float = 0.0   # 相关性评分

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "date": self.date,
            "score": self.score
        }


class BaseSearchEngine(ABC):
    """搜索引擎基类"""

    def __init__(self, name: str, timeout: int = 30):
        self.name = name
        self.timeout = timeout

    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        执行搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            List[SearchResult]: 搜索结果列表
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查搜索引擎是否可用"""
        pass

    def normalize_results(self, raw_results: List[Dict]) -> List[SearchResult]:
        """
        标准化搜索结果

        Args:
            raw_results: 原始搜索结果

        Returns:
            List[SearchResult]: 标准化后的结果
        """
        normalized = []
        for item in raw_results:
            result = SearchResult(
                title=self._extract_title(item),
                url=self._extract_url(item),
                snippet=self._extract_snippet(item),
                source=self.name,
                date=self._extract_date(item)
            )
            normalized.append(result)
        return normalized

    def _extract_title(self, item: Dict) -> str:
        """提取标题"""
        return item.get("title", "")

    def _extract_url(self, item: Dict) -> str:
        """提取链接"""
        return item.get("url") or item.get("link", "")

    def _extract_snippet(self, item: Dict) -> str:
        """提取摘要"""
        return item.get("snippet") or item.get("body") or item.get("description", "")

    def _extract_date(self, item: Dict) -> Optional[str]:
        """提取日期"""
        return item.get("date")
