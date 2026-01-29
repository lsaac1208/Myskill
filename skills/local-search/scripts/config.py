#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地搜索配置文件
"""

import os
from typing import Dict, List, Optional

# 默认配置
DEFAULT_LOCATION = "武汉"  # 默认地理位置
DEFAULT_MAX_RESULTS = 10   # 默认搜索结果数
SEARCH_TIMEOUT = 30        # 搜索超时时间(秒)

# 搜索引擎配置
SEARCH_ENGINES = {
    "google": {
        "name": "Google",
        "enabled": True,
        "priority": 5,
        "lang": "zh-CN",
        "country": "CN"
    },
    "baidu": {
        "name": "百度",
        "enabled": True,
        "priority": 4,
    },
    "duckduckgo": {
        "name": "DuckDuckGo",
        "enabled": True,
        "priority": 3,
    },
    "github": {
        "name": "GitHub",
        "enabled": True,
        "priority": 6,
        "category": "code"
    }
}

# 新闻 RSS 源配置
NEWS_SOURCES = {
    "general": [
        {"name": "央视网", "url": "http://news.cctv.com/rss/news.xml"},
        {"name": "新浪新闻", "url": "http://news.sina.com.cn/society/all/roll/index.d.html"},
        {"name": "腾讯新闻", "url": "https://news.qq.com/rss/newsgn.xml"},
    ],
    "tech": [
        {"name": "36Kr", "url": "https://36kr.com/feed"},
        {"name": "虎嗅网", "url": "https://www.huxiu.com/rss/0.xml"},
    ],
    "finance": [
        {"name": "新浪财经", "url": "http://finance.sina.com.cn/roll/index.d.html"},
    ]
}

# 意图识别关键词模板
INTENT_PATTERNS = {
    "news": {
        "keywords": ["新闻", "资讯", "消息", "头条", "最新"],
        "prefixes": ["今天的新闻", "最新新闻", "今日新闻", "有什么新闻"]
    },
    "weather": {
        "keywords": ["天气", "气温", "温度", "下雨", "晴天", "阴天"],
        "prefixes": ["天气怎么样", "天气如何", "今天天气"]
    },
    "search": {
        "keywords": ["搜索", "查一下", "查找", "找", "百度", "谷歌"],
        "prefixes": ["搜索", "查一下", "帮我找"]
    },
    "github": {
        "keywords": ["github", "仓库", "repo", "开源项目", "代码", "issue", "pr"],
        "prefixes": ["github搜索", "在github上", "github仓库"],
        "patterns": ["github.com", "gh:", "repo:", "code:", "lang:"]
    }
}

# 时间相关关键词
TIME_PATTERNS = {
    "today": ["今天", "今日", "现在"],
    "yesterday": ["昨天", "昨日"],
    "this_week": ["本周", "这周"],
    "this_month": ["本月", "这个月"],
    "this_year": ["今年", "本年"]
}

# 城市列表（用于位置识别）
MAJOR_CITIES = [
    "北京", "上海", "广州", "深圳", "武汉", "杭州", "南京",
    "成都", "重庆", "西安", "苏州", "天津", "青岛", "大连",
    "厦门", "长沙", "郑州", "沈阳", "哈尔滨", "济南", "昆明"
]

# 输出格式配置
OUTPUT_FORMATS = {
    "markdown": {
        "enabled": True,
        "emoji": True
    },
    "json": {
        "enabled": True,
        "indent": 2
    }
}
