#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索引擎模块
"""

from .google import GoogleSearchEngine
from .baidu import BaiduSearchEngine
from .duckduckgo import DuckDuckGoSearchEngine
from .github import GitHubSearchEngine

__all__ = [
    'GoogleSearchEngine',
    'BaiduSearchEngine',
    'DuckDuckGoSearchEngine',
    'GitHubSearchEngine'
]
