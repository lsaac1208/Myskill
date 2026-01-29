# Skills 管理工具集

本目录包含用于管理 Claude Code Skills 的实用工具。

## 📁 工具列表

### 1. `init-github-repos.py`
**用途**: 为自定义 Skills 初始化 GitHub 仓库

**功能**:
- 初始化 Git 仓库
- 创建 README.md
- 创建 .gitignore
- 创建 LICENSE（MIT）
- 生成 Git 命令提示

**使用方法**:
```bash
# 处理所有自定义 Skills
python3 init-github-repos.py

# 处理单个 Skill
python3 init-github-repos.py docx
```

### 2. `update-github-info.py`
**用途**: 批量更新 SKILL.md 的 GitHub 信息

**功能**:
- 读取 Git commit hash
- 更新 frontmatter 中的 github_url 和 github_hash
- 保持字段顺序一致

**使用方法**:
```bash
python3 update-github-info.py
# 按提示输入 GitHub 用户名
```

### 3. `quick-setup.sh`
**用途**: 一键准备所有 Skills 的 Git 仓库

**功能**:
- 批量初始化 Git 仓库
- 创建初始提交
- 添加远程仓库
- 生成推送命令

**使用方法**:
```bash
bash quick-setup.sh YOUR_GITHUB_USERNAME
```

### 4. `show-guide.py`
**用途**: 显示完整的 GitHub 设置指南

**功能**:
- 显示详细的操作步骤
- 提供常见问题解答
- 生成 GITHUB_SETUP_GUIDE.md

**使用方法**:
```bash
python3 show-guide.py
```

### 5. `GITHUB_SETUP_GUIDE.md`
**用途**: 完整的 GitHub 版本追踪设置指南

**内容**:
- 详细的步骤说明
- 多种操作方法
- 常见问题解答
- 最佳实践建议

## 🚀 快速开始

### 场景 1: 首次设置 GitHub 追踪

```bash
# 1. 查看指南
python3 show-guide.py

# 2. 初始化所有仓库
python3 init-github-repos.py

# 3. 在 GitHub 上创建仓库（手动或使用 gh CLI）

# 4. 推送代码

# 5. 更新 SKILL.md
python3 update-github-info.py
```

### 场景 2: 快速设置（推荐）

```bash
# 一键准备
bash quick-setup.sh YOUR_GITHUB_USERNAME

# 然后在 GitHub 上创建仓库并推送
```

### 场景 3: 单个 Skill 设置

```bash
# 初始化单个 Skill
python3 init-github-repos.py docx

# 创建 GitHub 仓库并推送

# 更新信息
python3 update-github-info.py
```

## 📋 工作流程

```
1. 初始化本地仓库
   ↓
2. 在 GitHub 创建远程仓库
   ↓
3. 推送代码到 GitHub
   ↓
4. 更新 SKILL.md 的 frontmatter
   ↓
5. 使用 skill-manager 验证
```

## 🔧 依赖要求

- Python 3.6+
- Git
- GitHub 账号
- gh CLI（可选，用于快速创建仓库）

## 📝 注意事项

1. **备份数据**: 在运行脚本前建议备份 Skills 目录
2. **检查权限**: 确保脚本有执行权限
3. **GitHub 用户名**: 准备好您的 GitHub 用户名
4. **网络连接**: 确保能访问 GitHub

## 🐛 故障排除

### 脚本无法执行

```bash
chmod +x *.py *.sh
```

### Git 命令失败

检查 Git 是否正确安装：
```bash
git --version
```

### 无法推送到 GitHub

检查远程仓库是否已创建：
```bash
gh repo view YOUR_USERNAME/SKILL_NAME
```

## 📖 相关文档

- [GITHUB_SETUP_GUIDE.md](GITHUB_SETUP_GUIDE.md) - 完整设置指南
- [../skill-manager/SKILL.md](../skill-manager/SKILL.md) - Skill Manager 文档
- [../.templates/README.md](../.templates/README.md) - 文档模板指南

## 🔗 相关 Skills

- **skill-manager**: 管理和更新 Skills
- **skill-evolution-manager**: 优化和迭代 Skills
- **github-to-skills**: 从 GitHub 创建新 Skills

---

**创建日期**: 2026-01-26
**版本**: 1.0.0
