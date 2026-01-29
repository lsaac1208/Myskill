#!/usr/bin/env python3
"""测试搜索功能"""
from ddgs import DDGS

try:
    ddgs = DDGS()
    results = list(ddgs.text("武汉天气", max_results=3))
    print(f"✅ 搜索成功，找到 {len(results)} 条结果")
    for r in results:
        print(f"  - {r.get('title', 'N/A')}")
except Exception as e:
    print(f"❌ 搜索失败: {e}")
