# Myskill

🛠️ 个人 AI 助手技能库 - 为 Claude Code / Kiro 等 AI 编程助手打造的自定义技能集合。

## 📖 简介

这是一个模块化的技能（Skills）集合，旨在增强 AI 编程助手的能力。每个技能都是独立的功能模块，可以根据用户的自然语言请求自动激活。

## ✨ 特性

- 🎯 **自动触发** - 基于关键词智能识别并激活相应技能
- 📦 **模块化设计** - 每个技能独立封装，易于维护和扩展
- 🔧 **开箱即用** - 提供完整的脚本和文档
- 🌐 **多语言支持** - 支持中英文触发词

## 📁 技能列表

### 文档处理
| 技能 | 描述 |
|------|------|
| [docx](skills/docx/) | Word 文档创建、编辑、分析，支持追踪修改和批注 |
| [pptx](skills/pptx/) | PowerPoint 演示文稿处理 |
| [xlsx](skills/xlsx/) | Excel 电子表格处理 |

### 搜索与信息
| 技能 | 描述 |
|------|------|
| [local-search](skills/local-search/) | 多引擎聚合搜索（Google、百度、DuckDuckGo、GitHub） |
| [githubdaily](skills/githubdaily/) | GitHub 每日热门项目追踪 |

### 开发工具
| 技能 | 描述 |
|------|------|
| [zx](skills/zx/) | Google zx 脚本工具包装 |
| [just](skills/just/) | Just 命令运行器包装 |
| [task](skills/task/) | Task 任务运行器包装 |
| [cli](skills/cli/) | 命令行工具集成 |
| [yt-dlp](skills/yt-dlp/) | 视频下载工具包装 |

### 技能管理
| 技能 | 描述 |
|------|------|
| [skill-manager](skills/skill-manager/) | 技能生命周期管理、健康检查、依赖验证 |
| [skill-evolution-manager](skills/skill-evolution-manager/) | 技能优化和迭代管理 |
| [github-to-skills](skills/github-to-skills/) | 从 GitHub 仓库快速创建新技能 |

### 其他工具
| 技能 | 描述 |
|------|------|
| [mcp-builder](skills/mcp-builder/) | MCP 服务器构建工具 |
| [webapp-testing](skills/webapp-testing/) | Web 应用自动化测试 |
| [artifacts-builder](skills/artifacts-builder/) | 构建产物管理 |
| [amazing-python-scripts](skills/amazing-python-scripts/) | Python 脚本集合 |
| [awesome-cli-apps](skills/awesome-cli-apps/) | CLI 应用推荐 |
| [awesome-workflow-engines](skills/awesome-workflow-engines/) | 工作流引擎推荐 |

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/lsaac1208/Myskill.git

# 进入目录
cd Myskill

# 将 skills 目录链接到你的 AI 助手配置目录
# 例如 Claude Code:
ln -s $(pwd)/skills ~/.claude/skills
```

### 使用

技能会根据对话内容自动激活。例如：

- 说 "帮我搜索 xxx" → 激活 `local-search` 技能
- 说 "创建一个 Word 文档" → 激活 `docx` 技能
- 说 "检查 skill 更新" → 激活 `skill-manager` 技能

## 📋 技能结构

每个技能遵循统一的目录结构：

```
skills/
└── skill-name/
    ├── SKILL.md          # 技能文档（必需）
    ├── scripts/          # 脚本文件
    │   └── *.py / *.sh
    ├── assets/           # 资源文件（可选）
    └── references/       # 参考文档（可选）
```

### SKILL.md 格式

```yaml
---
name: skill-name
description: 触发关键词和描述
version: 1.0.0
dependencies: ["dep1", "dep2"]
---

# 技能标题

## 使用方法
...
```

## 🔧 开发指南

### 创建新技能

1. 使用模板创建：
```bash
cp -r skills/.templates/custom-skill-template.md skills/new-skill/SKILL.md
```

2. 编辑 `SKILL.md`，填写元数据和文档

3. 添加脚本到 `scripts/` 目录

4. 测试技能功能

### 技能管理

```bash
# 列出所有技能
python skills/skill-manager/scripts/list_skills.py skills/

# 健康检查
python skills/skill-manager/scripts/health_check.py skills/

# 检查依赖
python skills/skill-manager/scripts/check_dependencies.py skills/
```

## 📚 文档

- [模板使用指南](skills/.templates/README.md)
- [工具集说明](skills/.tools/README.md)
- [Wrapper 最佳实践](skills/.templates/WRAPPER_BEST_PRACTICES.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

⭐ 如果这个项目对你有帮助，请给个 Star！
