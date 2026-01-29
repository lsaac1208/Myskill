---
name: cli
description: GitHub CLI时自动触发 - github cli、gh、github命令行、pr管理、issue管理、github操作、repo操作。GitHub CLI (gh) 是 GitHub 的命令行工具,提供 PR、Issue、仓库管理等功能的终端接口。
github_url: https://github.com/cli/cli
github_hash: cf53b76d71a8e26dd3f1e0106d6287e57592eaac
version: 0.2.0
created_at: 2026-01-25T14:21:11.930891
updated_at: 2026-01-26
entry_point: scripts/wrapper.py
dependencies: ['gh']
license: MIT
---

# GitHub CLI Skill

GitHub 官方命令行工具，将 Pull Request、Issue 和其他 GitHub 功能带到终端。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **PR 管理**: "创建 PR"、"查看 PR"、"合并 PR"、"PR 列表"
- **Issue 管理**: "创建 issue"、"查看 issue"、"关闭 issue"
- **仓库操作**: "克隆仓库"、"查看仓库"、"fork 仓库"
- **GitHub 操作**: "gh 命令"、"github cli"、"github 命令行"

## ✨ 核心功能

- ✅ **PR 管理**: 创建、查看、合并、审查 Pull Request
- ✅ **Issue 管理**: 创建、查看、编辑、关闭 Issue
- ✅ **仓库操作**: 克隆、查看、fork、创建仓库
- ✅ **工作流管理**: 查看和触发 GitHub Actions
- ✅ **Release 管理**: 创建和查看 Release
- ✅ **Gist 管理**: 创建和管理 Gist
- ✅ **认证集成**: 无缝集成 GitHub 认证

## 🚀 使用方法

### PR 管理

```bash
# 创建 PR
gh pr create --title "新功能" --body "功能描述"

# 交互式创建 PR
gh pr create

# 查看 PR 列表
gh pr list

# 查看特定 PR
gh pr view 123

# 在浏览器中打开 PR
gh pr view 123 --web

# 合并 PR
gh pr merge 123

# 审查 PR
gh pr review 123 --approve
gh pr review 123 --comment --body "看起来不错"
gh pr review 123 --request-changes --body "需要修改"

# 检出 PR 到本地
gh pr checkout 123
```

### Issue 管理

```bash
# 创建 Issue
gh issue create --title "Bug 报告" --body "问题描述"

# 交互式创建 Issue
gh issue create

# 查看 Issue 列表
gh issue list

# 查看特定 Issue
gh issue view 456

# 关闭 Issue
gh issue close 456

# 重新打开 Issue
gh issue reopen 456

# 添加标签
gh issue edit 456 --add-label "bug,priority"
```

### 仓库操作

```bash
# 克隆仓库
gh repo clone owner/repo

# 查看仓库信息
gh repo view owner/repo

# 在浏览器中打开仓库
gh repo view owner/repo --web

# Fork 仓库
gh repo fork owner/repo

# 创建新仓库
gh repo create my-project --public

# 列出仓库
gh repo list owner
```

### GitHub Actions

```bash
# 查看工作流列表
gh workflow list

# 查看工作流运行
gh run list

# 查看特定运行详情
gh run view 123456

# 查看运行日志
gh run view 123456 --log

# 重新运行工作流
gh run rerun 123456

# 触发工作流
gh workflow run deploy.yml
```

### Release 管理

```bash
# 创建 Release
gh release create v1.0.0 --title "版本 1.0.0" --notes "发布说明"

# 查看 Release 列表
gh release list

# 查看特定 Release
gh release view v1.0.0

# 下载 Release 资源
gh release download v1.0.0

# 上传文件到 Release
gh release upload v1.0.0 dist/*.zip
```

## 📋 常用命令

| 命令 | 说明 |
|------|------|
| `gh auth login` | 登录 GitHub |
| `gh auth status` | 查看认证状态 |
| `gh pr create` | 创建 Pull Request |
| `gh pr list` | 列出 PR |
| `gh pr merge` | 合并 PR |
| `gh issue create` | 创建 Issue |
| `gh issue list` | 列出 Issue |
| `gh repo clone` | 克隆仓库 |
| `gh repo view` | 查看仓库 |
| `gh workflow list` | 列出工作流 |
| `gh run view` | 查看工作流运行 |
| `gh release create` | 创建 Release |

## 🔧 安装

### macOS - Homebrew

```bash
brew install gh
```

### Linux - apt

```bash
# Debian/Ubuntu
sudo apt install gh
```

### Linux - dnf

```bash
# Fedora/RHEL
sudo dnf install gh
```

### Windows - Scoop

```bash
scoop install gh
```

### Windows - Chocolatey

```bash
choco install gh
```

### 从源码安装

```bash
go install github.com/cli/cli/v2/cmd/gh@latest
```

### 验证安装

```bash
gh --version
```

### 首次使用 - 认证

```bash
# 登录 GitHub
gh auth login

# 选择认证方式
# 1. GitHub.com
# 2. GitHub Enterprise Server
# 选择协议: HTTPS 或 SSH
# 选择认证方式: 浏览器或 Token
```

## 📝 实用示例

### 示例 1: 完整的 PR 工作流

```bash
# 1. 创建新分支
git checkout -b feature/new-feature

# 2. 进行开发和提交
git add .
git commit -m "添加新功能"
git push origin feature/new-feature

# 3. 创建 PR
gh pr create --title "添加新功能" --body "这个 PR 添加了..." --base main

# 4. 查看 PR 状态
gh pr status

# 5. 查看 CI 检查
gh pr checks

# 6. 请求审查
gh pr edit --add-reviewer @teammate

# 7. 合并 PR
gh pr merge --squash --delete-branch
```

### 示例 2: Issue 跟踪

```bash
# 创建 Bug Issue
gh issue create \
  --title "登录页面崩溃" \
  --body "在 Chrome 浏览器中..." \
  --label "bug,priority-high" \
  --assignee @me

# 查看我的 Issue
gh issue list --assignee @me

# 查看特定 Issue 的评论
gh issue view 123 --comments

# 添加评论
gh issue comment 123 --body "已修复，请测试"

# 关闭 Issue
gh issue close 123
```

### 示例 3: 仓库管理

```bash
# Fork 并克隆仓库
gh repo fork owner/repo --clone

# 查看仓库统计
gh repo view owner/repo

# 创建新仓库
gh repo create my-awesome-project \
  --public \
  --description "一个很棒的项目" \
  --gitignore Node \
  --license MIT

# 归档仓库
gh repo archive owner/old-repo
```

### 示例 4: 批量操作

```bash
# 批量关闭 Issue
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {}

# 批量审查 PR
for pr in $(gh pr list --json number --jq '.[].number'); do
  gh pr review $pr --approve
done

# 下载所有 Release 资源
gh release list --json tagName --jq '.[].tagName' | \
  xargs -I {} gh release download {}
```

## 🐛 常见问题

### 1. gh 命令未找到

**症状**: `gh: command not found`

**解决方案**:
```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# 验证安装
gh --version
```

### 2. 认证失败

**症状**: `authentication failed`

**解决方案**:
```bash
# 重新登录
gh auth login

# 检查认证状态
gh auth status

# 刷新认证
gh auth refresh
```

### 3. 权限不足

**症状**: `permission denied` 或 `403 Forbidden`

**解决方案**:
```bash
# 检查当前权限
gh auth status

# 重新登录并授予更多权限
gh auth login --scopes repo,workflow,admin:org
```

### 4. 找不到仓库

**症状**: `repository not found`

**解决方案**:
```bash
# 确保使用正确的格式
gh repo view owner/repo

# 检查是否有访问权限
gh auth status

# 对于私有仓库，确保已认证
gh auth login
```

### 5. PR 创建失败

**症状**: `no commits between base and head`

**解决方案**:
```bash
# 确保有提交
git log origin/main..HEAD

# 推送提交到远程
git push origin feature-branch

# 然后创建 PR
gh pr create
```

## 📖 高级特性

### 使用别名

```bash
# 创建别名
gh alias set pv 'pr view'
gh alias set il 'issue list --assignee @me'

# 使用别名
gh pv 123
gh il
```

### 自定义输出格式

```bash
# JSON 输出
gh pr list --json number,title,author

# 使用 jq 处理
gh pr list --json number,title | jq '.[] | select(.title | contains("bug"))'

# 自定义模板
gh pr list --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'
```

### 扩展功能

```bash
# 安装扩展
gh extension install owner/gh-extension

# 列出已安装扩展
gh extension list

# 升级扩展
gh extension upgrade --all

# 常用扩展推荐
gh extension install dlvhdr/gh-dash  # 仪表板
gh extension install mislav/gh-branch  # 分支管理
```

### 配置文件

```yaml
# ~/.config/gh/config.yml
git_protocol: ssh
editor: vim
prompt: enabled
pager: less

aliases:
    co: pr checkout
    pv: pr view
```

## 📖 参考资料

- **官方文档**: https://cli.github.com/manual/
- **GitHub 仓库**: https://github.com/cli/cli
- **扩展市场**: https://github.com/topics/gh-extension

## 📝 更新日志

### v0.2.0 (2026-01-26)
- ✨ 更新到最新版本 (cf53b76)
- 📝 完善文档和使用示例
- ✨ 添加常见问题解答
- ✨ 添加高级特性说明
- ✨ 添加批量操作示例

### v0.1.0 (2026-01-25)
- 🎉 初始版本
