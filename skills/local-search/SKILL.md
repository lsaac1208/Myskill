---
name: local-search
description: 搜索时自动触发 - 搜索、搜一下、查一下、查找、找、帮找、帮搜、google、百度、今天的新闻、今日新闻、有什么新闻、新闻、今天天气、天气、气温、github、GitHub搜索、github上、在github、找仓库、搜代码、开源项目。完全不消耗GLM MCP额度，使用多引擎聚合搜索。
version: 2.2.0
created_at: 2025-01-24
updated_at: 2026-01-26
entry_point: scripts/search.sh
dependencies: ["ddgs>=9.0.0", "googlesearch-python", "jieba", "feedparser", "beautifulsoup4", "requests"]
---

# 本地搜索 Skill (增强版 + GitHub)

当用户有**网络搜索需求**或 **GitHub 搜索需求**时自动激活此 Skill，使用本地多引擎搜索代替 GLM MCP 搜索功能。

## 🎯 适用场景

当用户请求以下内容时，Claude 应自动使用此 Skill：

- **搜索信息**: "搜索 xxx"、"查一下 xxx"、"找 xxx"
- **查询资讯**: "xxx 的最新消息"、"今天 xxx 新闻"
- **实时数据**: "今天天气"、"xxx 汇率"、"股票行情"
- **资料查找**: "xxx 教程"、"xxx 怎么做"
- **GitHub 搜索**: "github 搜索 xxx"、"找 xxx 仓库"、"xxx 开源项目"
- **网络内容**: 任何需要联网获取的信息

## 🚀 使用方法

### 通用搜索
当识别到搜索需求时，Claude 应该：

1. **激活此 Skill**
2. **调用搜索脚本**:
   ```bash
   python3 ~/.claude/skills/local-search/scripts/local_search.py search "关键词"
   ```
3. **将搜索结果返回给用户**

### GitHub 搜索
当识别到 GitHub 搜索需求时，Claude 应该：

1. **激活此 Skill**
2. **调用 GitHub 搜索脚本**:
   ```bash
   python3 ~/.claude/skills/local-search/scripts/local_search.py github "关键词" -t repos
   ```
3. **将搜索结果返回给用户**

## 📋 工作流程

```
用户请求搜索
    ↓
Claude 识别为网络搜索需求 或 GitHub 搜索需求
    ↓
激活 local-search Skill
    ↓
智能意图识别（类型、位置、时间、GitHub 识别）
    ↓
多引擎聚合搜索（Google、百度、DuckDuckGo、GitHub）
    ↓
结果去重、排序
    ↓
格式化输出（新闻/天气/通用/GitHub）
    ↓
返回搜索结果
```

## ✨ 增强特性

### 智能意图识别
- **类型识别**: 自动识别搜索类型（新闻/天气/通用/GitHub）
- **位置识别**: 从查询中提取地理位置
- **时间识别**: 理解"今天"、"本周"等时间词
- **查询优化**: 自动优化搜索关键词
- **GitHub 识别**: 识别 `github:`、`repo:`、`lang:` 等 GitHub 搜索模式

### 多引擎聚合
- **Google**: 主力引擎，结果质量高（⭐⭐⭐⭐⭐）
- **百度**: 中文内容丰富（⭐⭐⭐⭐）
- **DuckDuckGo**: 隐私保护，备选（⭐⭐⭐）
- **GitHub**: 代码/仓库搜索（⭐⭐⭐⭐⭐）
- **结果去重**: 基于 URL 智能去重
- **相关性排序**: 综合评分排序

### 智能格式化
- **新闻格式**: 结构化新闻输出，按来源分组
- **天气格式**: 提取温度、天气状况、风力
- **通用格式**: 清晰的搜索结果列表
- **GitHub 格式**: 仓库/代码/Issue 专用格式

## 🏆 优势对比

| 特性 | GLM MCP | 本地搜索 Skill |
|------|---------|----------------|
| **额度消耗** | ❌ 每月 100 次 | ✅ 无限使用 |
| **搜索引擎** | 单一 | 多引擎聚合 |
| **意图识别** | ❌ 无 | ✅ 智能识别 |
| **GitHub 搜索** | ❌ 消耗额度 | ✅ 本地 CLI |
| **结果质量** | 一般 | 高质量去重排序 |
| **格式化** | ❌ 无 | ✅ 智能格式化 |
| **隐私保护** | ⚠️ 云端记录 | ✅ 完全本地 |

## 📝 使用示例

### 新闻搜索
**用户**: "今天的新闻" 或 "有什么新闻"

**Claude 应该**:
1. 识别为新闻搜索需求
2. 调用: `python3 ~/.claude/skills/local-search/scripts/local_search.py search "今天的新闻"`
3. 返回格式化的新闻列表

### 天气搜索
**用户**: "武汉今天天气怎么样？"

**Claude 应该**:
1. 识别为天气查询需求
2. 调用: `python3 ~/.claude/skills/local-search/scripts/local_search.py search "武汉今天天气怎么样"`
3. 返回解析后的天气信息

### GitHub 仓库搜索
**用户**: "在 GitHub 上搜索 rust 搜索库"

**Claude 应该**:
1. 识别为 GitHub 搜索需求
2. 调用: `python3 ~/.claude/skills/local-search/scripts/local_search.py github "rust search" -t repos`
3. 返回格式化的仓库列表

### GitHub 代码搜索
**用户**: "搜索 Python 搜索相关代码"

**Claude 应该**:
1. 识别为 GitHub 代码搜索需求
2. 调用: `python3 ~/.claude/skills/local-search/scripts/local_search.py github "language:python search" -t code`
3. 返回匹配的代码文件列表

### 通用搜索
**用户**: "查一下 AI 的最新进展"

**Claude 应该**:
1. 识别为通用搜索需求
2. 调用: `python3 ~/.claude/skills/local-search/scripts/local_search.py search "AI 最新进展" -n 20`
3. 返回排序后的搜索结果

## ⚙️ 高级参数

### 通用搜索参数
- `query` - 搜索关键词（必需）
- `-n, --results` - 结果数量（可选，默认 10）
- `--json` - 输出 JSON 格式（可选）
- `-e, --engines` - 指定搜索引擎（可选：google baidu duckduckgo github）

### GitHub 搜索参数
- `query` - 搜索关键词（必需）
- `-n, --results` - 结果数量（可选，默认 10）
- `-t, --type` - 搜索类型（可选：repos/code/issues/prs/users，默认：repos）

### 指定搜索引擎示例
```bash
# 仅使用 Google 搜索
python3 ~/.claude/skills/local-search/scripts/local_search.py search "深度学习" -e google

# 使用 Google 和百度
python3 ~/.claude/skills/local-search/scripts/local_search.py search "武汉天气" -e google baidu
```

### GitHub 搜索类型示例
```bash
# 搜索仓库（默认）
python3 ~/.claude/skills/local-search/scripts/local_search.py github "rust" -t repos

# 搜索代码
python3 ~/.claude/skills/local-search/scripts/local_search.py github "search" -t code

# 搜索 Issues
python3 ~/.claude/skills/local-search/scripts/local_search.py github "bug" -t issues

# 搜索 Pull Requests
python3 ~/.claude/skills/local-search/scripts/local_search.py github "feature" -t prs

# 搜索用户
python3 ~/.claude/skills/local-search/scripts/local_search.py github "torvalds" -t users
```

## 📁 目录结构

```
~/.claude/skills/local-search/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── local_search.py         # 主搜索脚本
│   ├── search.sh              # Bash 包装器
│   ├── config.py              # 配置文件
│   ├── intent/                # 意图识别模块
│   │   ├── __init__.py
│   │   └── recognizer.py      # 意图识别器
│   ├── engines/               # 搜索引擎模块
│   │   ├── __init__.py
│   │   ├── base.py           # 基类
│   │   ├── google.py         # Google 搜索
│   │   ├── baidu.py          # 百度搜索
│   │   ├── duckduckgo.py     # DuckDuckGo 搜索
│   │   └── github.py         # GitHub 搜索
│   ├── aggregators/           # 聚合器模块
│   │   ├── __init__.py
│   │   └── search_aggregator.py  # 搜索聚合
│   └── formatters/            # 格式化器模块
│       ├── __init__.py
│       ├── base_formatter.py
│       ├── news_formatter.py  # 新闻格式化
│       ├── weather_formatter.py  # 天气格式化
│       ├── general_formatter.py  # 通用格式化
│       └── github_formatter.py  # GitHub 格式化
└── mcp-server/
    └── index.js              # MCP 服务器（可选）
```

## 🧪 测试命令

```bash
# 测试意图识别
python3 ~/.claude/skills/local-search/scripts/local_search.py test --intent

# 测试搜索引擎
python3 ~/.claude/skills/local-search/scripts/local_search.py test --engines

# 测试所有功能
python3 ~/.claude/skills/local-search/scripts/local_search.py test
```

## ⚠️ 注意事项

### GitHub 搜索要求
- 需要 [GitHub CLI](https://cli.github.com/) (gh 命令)
- 需要使用 `gh auth login` 进行认证
- 代码搜索可能对公开仓库有限制

### 网络要求
- 需要能够访问 Google 和百度搜索
- DuckDuckGo 中文搜索结果可能不理想，建议使用 `-e google baidu`

## 📊 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2025-01-24 | 初始版本，仅支持 DuckDuckGo |
| 2.0.0 | 2025-01-24 | 增强版：智能意图识别、多引擎聚合、结果格式化 |
| 2.1.0 | 2025-01-24 | 添加 GitHub 搜索能力（仓库/代码/Issue/PR/用户） |
