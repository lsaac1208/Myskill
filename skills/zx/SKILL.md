---
name: zx
description: Zx脚本编写时自动触发 - zx、javascript脚本、js脚本、bash脚本、shell脚本、脚本编写。Zx 是 Google 开发的更好脚本编写工具，用 JavaScript 替代复杂 Bash 脚本。
github_url: https://github.com/google/zx
github_hash: f19b651df0b8a0265883c28c208ed2c4da8b9081
version: 0.2.0
created_at: 2026-01-25T14:21:12.460813
updated_at: 2026-01-26
entry_point: scripts/wrapper.py
dependencies: ["zx", "node"]
license: Apache-2.0
---

# zx Skill

用 JavaScript 编写更好的 Shell 脚本。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **脚本编写**: "写一个脚本"、"创建脚本"、"shell 脚本"
- **JavaScript 脚本**: "用 js 写脚本"、"javascript 脚本"
- **zx 工具**: "使用 zx"、"zx 脚本"
- **自动化任务**: "自动化执行"、"批处理任务"

## ✨ 核心功能

- ✅ **JavaScript 语法**: 使用熟悉的 JavaScript 编写 Shell 脚本
- ✅ **异步支持**: 原生支持 async/await
- ✅ **便捷函数**: 内置 `$`、`cd`、`fetch` 等实用函数
- ✅ **彩色输出**: 自动美化命令输出
- ✅ **错误处理**: 智能的错误处理和退出码管理
- ✅ **TypeScript**: 支持 TypeScript 类型检查

## 🚀 使用方法

### 基本脚本

```javascript
#!/usr/bin/env zx

// 执行命令
await $`ls -la`

// 获取命令输出
const branch = await $`git branch --show-current`
console.log(`Current branch: ${branch}`)

// 条件执行
if (branch.stdout.includes('main')) {
  await $`git pull origin main`
}
```

### 切换目录

```javascript
#!/usr/bin/env zx

cd('/tmp')
await $`pwd` // 输出: /tmp

cd('src')
await $`pwd` // 输出: /tmp/src
```

### 使用 fetch

```javascript
#!/usr/bin/env zx

const response = await fetch('https://api.github.com/repos/google/zx')
const data = await response.json()
console.log(`Stars: ${data.stargazers_count}`)
```

### 管道和重定向

```javascript
#!/usr/bin/env zx

// 管道
await $`cat package.json | grep version`

// 重定向
await $`echo "Hello" > output.txt`
await $`cat output.txt`
```

### 并行执行

```javascript
#!/usr/bin/env zx

// 并行执行多个命令
await Promise.all([
  $`npm test`,
  $`npm run lint`,
  $`npm run build`
])
```

## 📋 常用 API

| API | 说明 | 示例 |
|-----|------|------|
| `$` | 执行 Shell 命令 | `await $\`ls\`` |
| `cd()` | 切换目录 | `cd('/tmp')` |
| `fetch()` | HTTP 请求 | `await fetch(url)` |
| `question()` | 用户输入 | `await question('Name?')` |
| `sleep()` | 延迟执行 | `await sleep(1000)` |
| `echo()` | 彩色输出 | `echo\`Hello\`` |
| `chalk` | 文本着色 | `chalk.blue('text')` |
| `fs` | 文件系统 | `await fs.readFile()` |
| `os` | 系统信息 | `os.platform()` |
| `path` | 路径处理 | `path.join()` |

## 🔧 安装

### 方法 1: npm 全局安装（推荐）

```bash
npm install -g zx
```

### 方法 2: npx 直接运行

```bash
npx zx script.mjs
```

### 方法 3: 作为项目依赖

```bash
npm install zx
```

### 验证安装

```bash
zx --version
```

## 📝 脚本示例

### 示例 1: Git 自动化

```javascript
#!/usr/bin/env zx

// 检查工作区状态
const status = await $`git status --porcelain`
if (status.stdout) {
  console.log('有未提交的更改')

  // 提交更改
  await $`git add .`
  const message = await question('提交信息: ')
  await $`git commit -m ${message}`
  await $`git push`
} else {
  console.log('工作区干净')
}
```

### 示例 2: 批量文件处理

```javascript
#!/usr/bin/env zx

const files = await glob('src/**/*.js')

for (const file of files) {
  console.log(`处理: ${file}`)
  await $`prettier --write ${file}`
  await $`eslint --fix ${file}`
}

console.log(`处理完成: ${files.length} 个文件`)
```

### 示例 3: 部署脚本

```javascript
#!/usr/bin/env zx

console.log('开始部署...')

// 运行测试
await $`npm test`

// 构建项目
await $`npm run build`

// 部署到服务器
await $`rsync -avz dist/ user@server:/var/www/`

console.log('部署完成!')
```

## 🐛 常见问题

### 1. zx 命令未找到

**症状**: `zx: command not found`

**解决方案**:
```bash
npm install -g zx
```

### 2. 权限错误

**症状**: `Permission denied`

**解决方案**:
```bash
chmod +x script.mjs
```

### 3. 模块导入错误

**症状**: `Cannot use import statement`

**解决方案**: 使用 `.mjs` 扩展名或在 package.json 中设置 `"type": "module"`

### 4. 命令执行失败

**症状**: 命令返回非零退出码

**解决方案**:
```javascript
// 忽略错误
await $`command`.nothrow()

// 自定义错误处理
try {
  await $`command`
} catch (error) {
  console.log('命令失败:', error.message)
}
```

## 📖 参考资料

- **官方文档**: https://github.com/google/zx
- **API 文档**: https://google.github.io/zx/
- **示例脚本**: https://github.com/google/zx/tree/main/examples

## 📝 更新日志

### v0.2.0 (2026-01-26)
- ✨ 更新到最新版本 (f19b651)
- 📝 完善文档和使用示例
- ✨ 添加常见问题解答
- ✨ 添加更多实用示例

### v0.1.0 (2026-01-25)
- 🎉 初始版本
