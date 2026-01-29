---
name: task
description: Go Task任务运行时自动触发 - task、taskfile、go task、任务运行器、构建工具、任务编排。Task (Go Task) 是一个任务运行器和构建工具，比 make 更简单易用，支持 Taskfile.yml 配置。
github_url: https://github.com/go-task/task
github_hash: 026c899d904ebf96c182b1d6a923c6e430718bbb
version: 0.2.0
created_at: 2026-01-25T14:21:12.749740
updated_at: 2026-01-26
entry_point: scripts/wrapper.py
dependencies: ["task"]
license: MIT
---

# Task Skill

现代化的任务运行器和构建工具，比 Make 更简单易用。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **任务运行**: "运行任务"、"执行 task"、"task 命令"
- **构建工具**: "构建项目"、"编译代码"、"打包应用"
- **任务编排**: "任务管理"、"工作流"、"自动化任务"
- **Taskfile**: "taskfile 配置"、"task 脚本"

## ✨ 核心功能

- ✅ **简单易用**: YAML 配置，比 Makefile 更直观
- ✅ **跨平台**: Windows、macOS、Linux 全支持
- ✅ **依赖管理**: 自动处理任务依赖关系
- ✅ **并行执行**: 支持任务并行运行
- ✅ **变量支持**: 环境变量、任务变量、模板语法
- ✅ **增量构建**: 基于文件变化的智能执行
- ✅ **Watch 模式**: 监听文件变化自动执行

## 🚀 使用方法

### 基本 Taskfile.yml

```yaml
version: '3'

tasks:
  build:
    desc: 构建项目
    cmds:
      - go build -o bin/app main.go
    sources:
      - '**/*.go'
    generates:
      - bin/app

  test:
    desc: 运行测试
    cmds:
      - go test ./...

  clean:
    desc: 清理构建文件
    cmds:
      - rm -rf bin/
```

### 运行任务

```bash
# 列出所有任务
task --list

# 运行特定任务
task build

# 运行多个任务
task clean build test

# 查看任务详情
task --summary build
```

### 任务依赖

```yaml
version: '3'

tasks:
  build:
    desc: 构建项目
    deps: [install, lint]
    cmds:
      - go build -o bin/app

  install:
    desc: 安装依赖
    cmds:
      - go mod download

  lint:
    desc: 代码检查
    cmds:
      - golangci-lint run
```

### 使用变量

```yaml
version: '3'

vars:
  APP_NAME: myapp
  BUILD_DIR: ./bin

tasks:
  build:
    desc: 构建 {{.APP_NAME}}
    cmds:
      - go build -o {{.BUILD_DIR}}/{{.APP_NAME}}
    env:
      CGO_ENABLED: 0
      GOOS: linux
```

### 并行执行

```yaml
version: '3'

tasks:
  test-all:
    desc: 并行运行所有测试
    deps:
      - task: test-unit
      - task: test-integration
      - task: test-e2e

  test-unit:
    cmds:
      - go test ./internal/...

  test-integration:
    cmds:
      - go test ./tests/integration/...

  test-e2e:
    cmds:
      - go test ./tests/e2e/...
```

### Watch 模式

```yaml
version: '3'

tasks:
  dev:
    desc: 开发模式（自动重载）
    watch: true
    sources:
      - '**/*.go'
    cmds:
      - go run main.go
```

运行：
```bash
task --watch dev
```

## 📋 常用命令

| 命令 | 说明 |
|------|------|
| `task` | 运行默认任务 |
| `task <name>` | 运行指定任务 |
| `task --list` | 列出所有任务 |
| `task --list-all` | 列出所有任务（包括内部任务） |
| `task --summary <name>` | 显示任务详情 |
| `task --watch <name>` | Watch 模式运行 |
| `task --parallel` | 并行运行所有依赖 |
| `task --dry` | 模拟运行（不执行） |
| `task --force` | 强制运行（忽略缓存） |
| `task --verbose` | 详细输出 |

## 🔧 安装

### macOS - Homebrew

```bash
brew install go-task/tap/go-task
```

### Linux - Snap

```bash
snap install task --classic
```

### Go Install

```bash
go install github.com/go-task/task/v3/cmd/task@latest
```

### 下载二进制文件

访问 [Releases 页面](https://github.com/go-task/task/releases) 下载对应平台的二进制文件。

### 验证安装

```bash
task --version
```

## 📝 实用示例

### 示例 1: 前端项目

```yaml
version: '3'

tasks:
  install:
    desc: 安装依赖
    cmds:
      - npm install
    sources:
      - package.json
      - package-lock.json
    generates:
      - node_modules/**

  dev:
    desc: 开发服务器
    deps: [install]
    cmds:
      - npm run dev

  build:
    desc: 构建生产版本
    deps: [install, lint]
    cmds:
      - npm run build
    sources:
      - 'src/**'
    generates:
      - 'dist/**'

  lint:
    desc: 代码检查
    cmds:
      - npm run lint

  test:
    desc: 运行测试
    deps: [install]
    cmds:
      - npm test

  clean:
    desc: 清理构建文件
    cmds:
      - rm -rf dist node_modules
```

### 示例 2: Docker 项目

```yaml
version: '3'

vars:
  IMAGE_NAME: myapp
  IMAGE_TAG: latest

tasks:
  build:
    desc: 构建 Docker 镜像
    cmds:
      - docker build -t {{.IMAGE_NAME}}:{{.IMAGE_TAG}} .

  run:
    desc: 运行容器
    deps: [build]
    cmds:
      - docker run -p 8080:8080 {{.IMAGE_NAME}}:{{.IMAGE_TAG}}

  push:
    desc: 推送镜像
    deps: [build]
    cmds:
      - docker push {{.IMAGE_NAME}}:{{.IMAGE_TAG}}

  clean:
    desc: 清理容器和镜像
    cmds:
      - docker stop $(docker ps -q --filter ancestor={{.IMAGE_NAME}})
      - docker rmi {{.IMAGE_NAME}}:{{.IMAGE_TAG}}
```

### 示例 3: 多环境部署

```yaml
version: '3'

vars:
  APP_NAME: myapp

tasks:
  deploy:dev:
    desc: 部署到开发环境
    cmds:
      - task: build
        vars: {ENV: dev}
      - task: push
        vars: {ENV: dev}

  deploy:prod:
    desc: 部署到生产环境
    cmds:
      - task: test
      - task: build
        vars: {ENV: prod}
      - task: push
        vars: {ENV: prod}

  build:
    desc: 构建应用
    cmds:
      - echo "Building for {{.ENV}}"
      - go build -o bin/{{.APP_NAME}}-{{.ENV}}

  push:
    desc: 推送到服务器
    cmds:
      - scp bin/{{.APP_NAME}}-{{.ENV}} server:/opt/{{.APP_NAME}}/
```

## 🐛 常见问题

### 1. task 命令未找到

**症状**: `task: command not found`

**解决方案**:
```bash
# macOS
brew install go-task/tap/go-task

# 或使用 Go
go install github.com/go-task/task/v3/cmd/task@latest
```

### 2. Taskfile.yml 未找到

**症状**: `task: No Taskfile found`

**解决方案**: 在项目根目录创建 `Taskfile.yml` 文件

### 3. 任务不执行（已缓存）

**症状**: 任务显示 "Task is up to date"

**解决方案**:
```bash
# 强制执行
task --force build

# 或清理缓存
rm -rf .task
```

### 4. 变量未替换

**症状**: 命令中的 `{{.VAR}}` 没有被替换

**解决方案**: 确保使用正确的模板语法，变量名区分大小写

## 📖 高级特性

### 包含其他 Taskfile

```yaml
version: '3'

includes:
  docker: ./docker/Taskfile.yml
  k8s: ./k8s/Taskfile.yml

tasks:
  deploy:
    cmds:
      - task: docker:build
      - task: k8s:apply
```

### 动态变量

```yaml
version: '3'

tasks:
  build:
    vars:
      GIT_COMMIT:
        sh: git rev-parse --short HEAD
      BUILD_TIME:
        sh: date -u +"%Y-%m-%dT%H:%M:%SZ"
    cmds:
      - go build -ldflags "-X main.commit={{.GIT_COMMIT}} -X main.buildTime={{.BUILD_TIME}}"
```

### 条件执行

```yaml
version: '3'

tasks:
  build:
    cmds:
      - go build
    status:
      - test -f bin/app
      - test bin/app -nt main.go
```

## 📖 参考资料

- **官方文档**: https://taskfile.dev/
- **GitHub**: https://github.com/go-task/task
- **示例**: https://github.com/go-task/task/tree/main/docs/docs/examples

## 📝 更新日志

### v0.2.0 (2026-01-26)
- ✨ 更新到最新版本 (026c899)
- 📝 完善文档和使用示例
- ✨ 添加常见问题解答
- ✨ 添加多个实用示例
- ✨ 添加高级特性说明

### v0.1.0 (2026-01-25)
- 🎉 初始版本
