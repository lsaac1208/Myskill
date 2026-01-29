#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气格式化器 - 天气搜索结果格式化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from formatters.base_formatter import BaseFormatter
from engines.base import SearchResult
from typing import List, Optional
import re


class WeatherFormatter(BaseFormatter):
    """天气格式化器"""

    # 天气图标映射
    WEATHER_ICONS = {
        "晴": "☀️",
        "多云": "⛅",
        "阴": "☁️",
        "雨": "🌧️",
        "雪": "❄️",
        "雷": "⛈️",
        "雾": "🌫️",
        "霾": "😷"
    }

    def format(self, results: List[SearchResult], **kwargs) -> str:
        """
        格式化天气搜索结果

        Args:
            results: 搜索结果列表
            location: 地点名称（必需）

        Returns:
            str: 格式化后的字符串
        """
        location = kwargs.get('location', '未知')

        lines = []

        # 标题
        lines.append(f"🌤️ {location}今日天气")
        lines.append("")

        # 尝试解析天气信息
        weather_info = self._parse_weather_info(results)

        if weather_info:
            # 格式化天气信息
            weather = weather_info.get('weather', '未知')
            temp = weather_info.get('temp', '')
            wind = weather_info.get('wind', '')
            humidity = weather_info.get('humidity', '')

            # 添加天气图标
            icon = self._get_weather_icon(weather)

            lines.append(f"**天气**: {icon} {weather}")
            if temp:
                lines.append(f"**气温**: {temp}")
            if wind:
                lines.append(f"**风力**: {wind}")
            if humidity:
                lines.append(f"**湿度**: {humidity}")

        else:
            # 无法解析，显示原始结果
            lines.append("**无法获取天气详情，以下是搜索结果：**\n")
            for i, result in enumerate(results[:3], 1):
                lines.append(f"{i}. {result.title}")
                lines.append(f"   {result.url}")
                if result.snippet:
                    snippet = self._safe_truncate(result.snippet, 80)
                    lines.append(f"   {snippet}")
                lines.append("")

        return "\n".join(lines)

    def _parse_weather_info(self, results: List[SearchResult]) -> Optional[dict]:
        """
        尝试从搜索结果中解析天气信息

        Args:
            results: 搜索结果列表

        Returns:
            dict: 天气信息字典
        """
        for result in results:
            text = f"{result.title} {result.snippet}"

            # 尝试解析温度
            temp_match = re.search(r'(\-?\d+)℃?[\//~\-](\-?\d+)℃?', text)
            temp = ""
            if temp_match:
                high = temp_match.group(1)
                low = temp_match.group(2)
                temp = f"{high}℃ / {low}℃"
            else:
                # 单一温度
                temp_match = re.search(r'(\-?\d+)℃', text)
                if temp_match:
                    temp = f"{temp_match.group(1)}℃"

            # 解析天气状况
            weather = ""
            for condition in ["晴", "多云", "阴", "雨", "雪", "雷", "雾", "霾"]:
                if condition in text:
                    weather = condition
                    break

            # 解析风力
            wind_match = re.search(r'风力[：:]\s*(\d+[-~至]\d+级|\d+级|<\d+级)', text)
            wind = wind_match.group(1) if wind_match else ""

            # 如果解析到了一些信息，返回
            if temp or weather or wind:
                return {
                    'weather': weather,
                    'temp': temp,
                    'wind': wind
                }

        return None

    def _get_weather_icon(self, weather: str) -> str:
        """获取天气图标"""
        for key, icon in self.WEATHER_ICONS.items():
            if key in weather:
                return icon
        return ""


# 测试代码
if __name__ == "__main__":
    from engines.base import SearchResult

    # 创建测试数据
    test_results = [
        SearchResult(
            title="武汉天气预报 - 中国天气网",
            url="http://www.weather.com.cn/weather/101200101.shtml",
            snippet="武汉今日天气：晴转多云，气温11℃/-1℃，风力<3级。明天天气预报：阴转小雨，气温8℃/2℃。",
            source="百度"
        ),
    ]

    formatter = WeatherFormatter()
    output = formatter.format(test_results, location="武汉")
    print(output)
