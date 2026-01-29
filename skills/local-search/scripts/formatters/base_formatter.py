#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化器基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from engines.base import SearchResult


class BaseFormatter(ABC):
    """格式化器基类"""

    def __init__(self, use_emoji: bool = True):
        self.use_emoji = use_emoji

    @abstractmethod
    def format(self, results: List[SearchResult], **kwargs) -> str:
        """
        格式化搜索结果

        Args:
            results: 搜索结果列表
            **kwargs: 额外参数

        Returns:
            str: 格式化后的字符串
        """
        pass

    def format_json(self, results: List[SearchResult]) -> str:
        """
        格式化为 JSON

        Args:
            results: 搜索结果列表

        Returns:
            str: JSON 字符串
        """
        import json
        data = [r.to_dict() for r in results]
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _safe_truncate(self, text: str, max_length: int = 100) -> str:
        """安全截断文本"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
