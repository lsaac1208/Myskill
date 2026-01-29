#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
意图识别器 - 识别用户搜索意图
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

# 导入配置
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import (
    INTENT_PATTERNS, TIME_PATTERNS, MAJOR_CITIES, DEFAULT_LOCATION
)


@dataclass
class SearchIntent:
    """搜索意图数据类"""
    query: str                      # 原始查询
    intent_type: str                # 意图类型: news, weather, search
    location: str = DEFAULT_LOCATION # 地理位置
    time_range: str = "today"       # 时间范围
    keywords: List[str] = field(default_factory=list)  # 关键词列表
    count: int = 10                 # 结果数量
    refined_query: str = ""         # 优化后的搜索词
    confidence: float = 0.0         # 置信度

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "query": self.query,
            "intent_type": self.intent_type,
            "location": self.location,
            "time_range": self.time_range,
            "keywords": self.keywords,
            "count": self.count,
            "refined_query": self.refined_query,
            "confidence": self.confidence
        }


class IntentRecognizer:
    """意图识别器"""

    def __init__(self):
        self.location = DEFAULT_LOCATION

        # 如果 jieba 可用，添加自定义词典
        if JIEBA_AVAILABLE:
            # 添加城市名到词典
            for city in MAJOR_CITIES:
                jieba.add_word(city)
            # 添加常用搜索词
            for intent_keywords in INTENT_PATTERNS.values():
                for keyword in intent_keywords.get("keywords", []):
                    jieba.add_word(keyword)

    def recognize(self, query: str) -> SearchIntent:
        """
        识别搜索意图

        Args:
            query: 用户查询字符串

        Returns:
            SearchIntent: 解析后的搜索意图
        """
        # 分词
        if JIEBA_AVAILABLE:
            words = list(jieba.cut(query))
        else:
            # 简单按空格分词
            words = query.split()

        # 识别意图类型
        intent_type, confidence = self._detect_intent_type(query, words)

        # 识别位置
        location = self._detect_location(words)

        # 识别时间范围
        time_range = self._detect_time_range(query)

        # 提取关键词
        keywords = self._extract_keywords(words)

        # 生成优化后的搜索词
        refined_query = self._refine_query(intent_type, location, time_range, keywords)

        return SearchIntent(
            query=query,
            intent_type=intent_type,
            location=location,
            time_range=time_range,
            keywords=keywords,
            refined_query=refined_query,
            confidence=confidence
        )

    def _detect_intent_type(self, query: str, words: List[str]) -> Tuple[str, float]:
        """检测意图类型"""
        scores = {}

        # 检查前缀匹配（高分）
        for intent_type, patterns in INTENT_PATTERNS.items():
            score = 0.0
            for prefix in patterns.get("prefixes", []):
                if query.startswith(prefix):
                    score += 0.8
                elif prefix in query:
                    score += 0.5
            scores[intent_type] = score

        # 检查关键词匹配（中分）
        query_lower = query.lower()
        for intent_type, patterns in INTENT_PATTERNS.items():
            additional_score = 0.0
            for keyword in patterns.get("keywords", []):
                if keyword in query_lower:
                    additional_score += 0.3
            scores[intent_type] = scores.get(intent_type, 0) + additional_score

        # 检查特殊模式匹配（高分）
        for intent_type, patterns in INTENT_PATTERNS.items():
            pattern_score = 0.0
            for pattern in patterns.get("patterns", []):
                if pattern in query_lower:
                    pattern_score += 0.7
            scores[intent_type] = scores.get(intent_type, 0) + pattern_score

        # 找出最高分的意图类型
        if not scores:
            return "search", 0.5

        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        # 如果分数太低，默认为通用搜索
        if best_score < 0.3:
            return "search", 0.5

        # 归一化置信度
        confidence = min(best_score, 1.0)
        return best_intent, confidence

    def _detect_location(self, words: List[str]) -> str:
        """检测地理位置"""
        # 检查是否包含主要城市名
        for word in words:
            if word in MAJOR_CITIES:
                return word

        return self.location

    def _detect_time_range(self, query: str) -> str:
        """检测时间范围"""
        for time_type, keywords in TIME_PATTERNS.items():
            for keyword in keywords:
                if keyword in query:
                    return time_type
        return "today"

    def _extract_keywords(self, words: List[str]) -> List[str]:
        """提取关键词（过滤停用词）"""
        # 简单停用词列表
        stopwords = {"的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"}

        keywords = [w for w in words if w not in stopwords and len(w) > 1]
        return keywords

    def _refine_query(self, intent_type: str, location: str, time_range: str, keywords: List[str]) -> str:
        """生成优化后的搜索词"""
        if intent_type == "news":
            # 新闻搜索优化
            time_map = {"today": "今天", "yesterday": "昨天", "this_week": "本周"}
            time_str = time_map.get(time_range, "")
            base_query = " ".join(keywords) if keywords else ""
            if time_str and location:
                return f"{location} {time_str} {base_query} 新闻".strip()
            elif time_str:
                return f"{time_str} {base_query} 新闻".strip()
            else:
                return f"{base_query} 新闻".strip()

        elif intent_type == "weather":
            # 天气搜索优化
            return f"{location} 天气"

        else:
            # 通用搜索
            return " ".join(keywords) if keywords else ""


# 测试代码
if __name__ == "__main__":
    recognizer = IntentRecognizer()

    test_queries = [
        "今天的新闻",
        "武汉今天天气怎么样",
        "查一下 AI 的最新进展",
        "百度搜索 深度学习",
        "今日头条新闻",
        "有什么新闻"
    ]

    print("=== 意图识别测试 ===\n")
    for query in test_queries:
        intent = recognizer.recognize(query)
        print(f"查询: {query}")
        print(f"  类型: {intent.intent_type} (置信度: {intent.confidence:.2f})")
        print(f"  位置: {intent.location}")
        print(f"  时间: {intent.time_range}")
        print(f"  关键词: {intent.keywords}")
        print(f"  优化词: {intent.refined_query}")
        print()
