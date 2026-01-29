---
name: just
description: Just命令运行时自动触发 - just、justfile、recipe、命令运行器、任务运行、项目命令。Just 是一个便捷的项目特定命令保存和运行工具，类似 make 的现代替代品。
github_url: https://github.com/casey/just
github_hash: 11e59c13b72f066764fa9a5f44ee908ba26ead8c
version: 0.2.0
created_at: 2026-01-25T14:21:12.210037
updated_at: 2026-01-26
entry_point: scripts/wrapper.py
dependencies: ['just']
license: CC0-1.0
---

# Just Skill

便捷的项目特定命令保存和运行工具，Make 的现代替代品。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **命令运行**: "运行 just"、"执行 recipe"、"just 命令"
- **项目命令**: "项目脚本"、"命令管理"、"任务执行"
- **Justfile**: "justfile 配置"、"recipe 定义"
- **构建工具**: "构建项目"、"编译代码"

## ✨ 核心功能

- ✅ **简单语法**: 比 Makefile 更直观易读
- ✅ **跨平台**: Windows、macOS、Linux 全支持
- ✅ **Recipe 参数**: 支持位置参数和默认值
- ✅ **依赖管理**: Recipe 可以依赖其他 Recipe
- ✅ **环境变量**: 灵活的变量和环境配置
- ✅ **条件执行**: 支持条件判断和错误处理
- ✅ **多语言支持**: 可以使用任何脚本语言

## 🚀 使用方法

### 基本 Justfile

```just
# 这是一个注释

# 默认 recipe（运行 just 时执行）
default:
    @echo "Hello, Just!"

# 构建项目
build:
    cargo build --release

# 运行测试
test:
    cargo test

# 清理构建文件
clean:
    rm -rf target/
```

### 运行 Recipe

```bash
# 运行默认 recipe
just

# 运行特定 recipe
just build

# 运行多个 recipe
just clean build test

# 列出所有 recipe
just --list

# 显示 recipe 内容
just --show build
```

### Recipe 参数

```just
# 位置参数
greet name:
    echo "Hello, {{name}}!"

# 默认参数
serve port="8080":
    python -m http.server {{port}}

# 多个参数
deploy env version:
    echo "Deploying {{version}} to {{env}}"

# 可变参数
test +args:
    cargo test {{args}}
```

使用：
```bash
just greet Alice
just serve 3000
just deploy production v1.2.3
just test --verbose --nocapture
```

### Recipe 依赖

```just
# 依赖其他 recipe
build: install lint
    cargo build

install:
    cargo fetch

lint:
    cargo clippy

# 带参数的依赖
deploy env: (build env)
    ./deploy.sh {{env}}

build env:
    cargo build --features {{env}}
```

### 变量

```just
# 定义变量
version := "1.0.0"
build_dir := "target/release"

# 使用变量
build:
    cargo build --release
    cp {{build_dir}}/app ./app-{{version}}

# 环境变量
export DATABASE_URL := "postgres://localhost/mydb"

test:
    cargo test

# 从命令获取变量
git_hash := `git rev-parse --short HEAD`

tag:
    git tag v{{version}}-{{git_hash}}
```

### 条件执行

```just
# 条件判断
deploy:
    #!/usr/bin/env bash
    if [ "{{env}}" = "production" ]; then
        echo "Deploying to production..."
    else
        echo "Deploying to staging..."
    fi

# 错误处理
build:
    cargo build || echo "Build failed!"

# 忽略错误
clean:
    -rm -rf target/
```

### 使用不同的 Shell

```just
# 使用 Python
analyze:
    #!/usr/bin/env python3
    import sys
    print(f"Python version: {sys.version}")

# 使用 Node.js
bundle:
    #!/usr/bin/env node
    console.log("Bundling assets...");

# 使用 Bash
setup:
    #!/usr/bin/env bash
    set -euxo pipefail
    echo "Setting up environment..."
```

## 📋 常用命令

| 命令 | 说明 |
|------|------|
| `just` | 运行默认 recipe |
| `just <recipe>` | 运行指定 recipe |
| `just --list` | 列出所有 recipe |
| `just --show <recipe>` | 显示 recipe 内容 |
| `just --dry-run <recipe>` | 模拟运行 |
| `just --evaluate` | 显示所有变量 |
| `just --variables` | 列出所有变量 |
| `just --choose` | 交互式选择 recipe |
| `just --working-directory <dir>` | 指定工作目录 |
| `just --justfile <file>` | 指定 justfile 路径 |

## 🔧 安装

### macOS - Homebrew

```bash
brew install just
```

### Linux - Cargo

```bash
cargo install just
```

### Linux - 包管理器

```bash
# Arch Linux
pacman -S just

# Fedora
dnf install just

# Ubuntu/Debian (需要添加仓库)
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
```

### Windows - Scoop

```bash
scoop install just
```

### Windows - Chocolatey

```bash
choco install just
```

### 从源码安装

```bash
cargo install just
```

### 验证安装

```bash
just --version
```

## 📝 实用示例

### 示例 1: Web 项目

```just
# 变量定义
node_version := "18"
port := "3000"

# 默认任务
default: dev

# 安装依赖
install:
    npm install

# 开发服务器
dev: install
    npm run dev

# 构建生产版本
build: install lint test
    npm run build

# 代码检查
lint:
    npm run lint
    npm run format:check

# 修复代码格式
fix:
    npm run lint:fix
    npm run format

# 运行测试
test:
    npm test

# 清理
clean:
    rm -rf dist node_modules

# 部署
deploy env: build
    ./scripts/deploy.sh {{env}}
```

### 示例 2: Rust 项目

```just
# 变量
target := "x86_64-unknown-linux-gnu"
release_dir := "target/release"

# 默认任务
default: check

# 检查代码
check:
    cargo check

# 构建
build:
    cargo build --release --target {{target}}

# 运行
run:
    cargo run

# 测试
test:
    cargo test

# 基准测试
bench:
    cargo bench

# 代码检查
lint:
    cargo clippy -- -D warnings

# 格式化
fmt:
    cargo fmt

# 文档
doc:
    cargo doc --open

# 清理
clean:
    cargo clean

# 发布
publish: test lint
    cargo publish
```

### 示例 3: Docker 项目

```just
# 变量
image_name := "myapp"
image_tag := "latest"
container_name := "myapp-container"

# 构建镜像
build:
    docker build -t {{image_name}}:{{image_tag}} .

# 运行容器
run: build
    docker run -d \
        --name {{container_name}} \
        -p 8080:8080 \
        {{image_name}}:{{image_tag}}

# 停止容器
stop:
    docker stop {{container_name}}
    docker rm {{container_name}}

# 查看日志
logs:
    docker logs -f {{container_name}}

# 进入容器
shell:
    docker exec -it {{container_name}} /bin/bash

# 推送镜像
push: build
    docker push {{image_name}}:{{image_tag}}

# 清理
clean:
    -docker stop {{container_name}}
    -docker rm {{container_name}}
    -docker rmi {{image_name}}:{{image_tag}}

# Docker Compose
up:
    docker-compose up -d

down:
    docker-compose down
```

### 示例 4: 多环境部署

```just
# 环境配置
dev_server := "dev.example.com"
staging_server := "staging.example.com"
prod_server := "prod.example.com"

# 构建
build env:
    @echo "Building for {{env}}..."
    npm run build:{{env}}

# 部署到开发环境
deploy-dev: (build "dev")
    rsync -avz dist/ user@{{dev_server}}:/var/www/

# 部署到预发布环境
deploy-staging: (build "staging")
    rsync -avz dist/ user@{{staging_server}}:/var/www/

# 部署到生产环境
deploy-prod: test (build "prod")
    @echo "Deploying to production..."
    rsync -avz dist/ user@{{prod_server}}:/var/www/
    @echo "Deployment complete!"

# 测试
test:
    npm test
    npm run e2e

# 回滚
rollback env:
    ssh user@{{env}}.example.com 'cd /var/www && git checkout HEAD~1'
```

## 🐛 常见问题

### 1. just 命令未找到

**症状**: `just: command not found`

**解决方案**:
```bash
# macOS
brew install just

# Linux
cargo install just

# 验证安装
just --version
```

### 2. Justfile 未找到

**症状**: `error: Justfile not found`

**解决方案**: 在项目根目录创建 `justfile` 或 `Justfile`

### 3. Recipe 执行失败

**症状**: Recipe 中的命令返回错误

**解决方案**:
```just
# 忽略错误（在命令前加 -）
clean:
    -rm -rf target/

# 或使用 || true
clean:
    rm -rf target/ || true
```

### 4. 变量未定义

**症状**: `error: Variable 'xxx' not defined`

**解决方案**:
```just
# 确保变量已定义
version := "1.0.0"

# 或使用环境变量
version := env_var_or_default("VERSION", "1.0.0")
```

### 5. 参数传递问题

**症状**: 参数没有正确传递

**解决方案**:
```just
# 使用 + 接收多个参数
test +args:
    cargo test {{args}}

# 使用 * 接收可选参数
run *args:
    ./app {{args}}
```

## 📖 高级特性

### 私有 Recipe

```just
# 私有 recipe（不在 --list 中显示）
_private:
    echo "This is private"

# 公开 recipe 可以调用私有 recipe
public: _private
    echo "This is public"
```

### 条件 Recipe

```just
# 根据操作系统执行不同命令
install:
    #!/usr/bin/env bash
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install package
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        apt-get install package
    fi
```

### Recipe 别名

```just
# 定义别名
alias b := build
alias t := test
alias r := run

build:
    cargo build

test:
    cargo test

run:
    cargo run
```

### 导入其他 Justfile

```just
# 导入其他文件
import 'tasks/docker.just'
import 'tasks/deploy.just'

# 使用导入的 recipe
all: docker-build deploy-prod
```

### 使用函数

```just
# 内置函数
timestamp := `date +%Y%m%d-%H%M%S`
git_branch := `git branch --show-current`

# 使用函数
backup:
    tar -czf backup-{{timestamp}}.tar.gz src/

tag:
    git tag {{git_branch}}-{{timestamp}}
```

## 📖 参考资料

- **官方文档**: https://just.systems/man/en/
- **GitHub 仓库**: https://github.com/casey/just
- **示例集合**: https://github.com/casey/just/tree/master/examples

## 📝 更新日志

### v0.2.0 (2026-01-26)
- ✨ 更新到最新版本 (11e59c1)
- 📝 完善文档和使用示例
- ✨ 添加常见问题解答
- ✨ 添加高级特性说明
- ✨ 添加多个实用示例

### v0.1.0 (2026-01-25)
- 🎉 初始版本
