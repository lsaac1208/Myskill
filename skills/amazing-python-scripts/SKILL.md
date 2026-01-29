---
name: amazing-python-scripts
description: Python脚本查询时自动触发 - python脚本、python示例、python代码、python工具、amazing python、找python脚本。精选 Python 脚本集合，从基础到高级的自动化任务脚本查询和搜索功能。
github_url: https://github.com/avinashkranjan/Amazing-Python-Scripts
github_hash: 905b1e6b0042c435c07f34c618f2f02f164232c5
version: 0.2.0
created_at: 2026-01-25T14:21:14.131458
updated_at: 2026-01-26
entry_point: scripts/wrapper.py
dependencies: ['python3']
license: MIT
---

# Amazing Python Scripts Skill

精选的 Python 脚本集合，涵盖从基础到高级的各类自动化任务。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **Python 脚本**: "python 脚本"、"python 示例"、"python 代码"
- **自动化任务**: "自动化脚本"、"批处理脚本"、"任务脚本"
- **工具查找**: "找 python 工具"、"python 实用工具"
- **学习资源**: "python 学习"、"python 例子"

## ✨ 核心功能

- ✅ **丰富的脚本库**: 涵盖 100+ 实用 Python 脚本
- ✅ **分类清晰**: 按功能分类，易于查找
- ✅ **即用即走**: 大部分脚本可直接运行
- ✅ **学习资源**: 适合初学者学习 Python
- ✅ **自动化工具**: 提供各类自动化解决方案
- ✅ **持续更新**: 社区活跃，定期添加新脚本

## 🚀 脚本分类

### 📁 文件操作

```python
# 批量重命名文件
# 位置: File-Renamer/
import os

def batch_rename(directory, old_ext, new_ext):
    for filename in os.listdir(directory):
        if filename.endswith(old_ext):
            new_name = filename.replace(old_ext, new_ext)
            os.rename(
                os.path.join(directory, filename),
                os.path.join(directory, new_name)
            )

# 使用示例
batch_rename('./images', '.jpeg', '.jpg')
```

```python
# 文件组织器
# 位置: File-Organizer/
import shutil
from pathlib import Path

def organize_files(directory):
    extensions = {
        'images': ['.jpg', '.png', '.gif'],
        'documents': ['.pdf', '.doc', '.txt'],
        'videos': ['.mp4', '.avi', '.mkv']
    }

    for file in Path(directory).iterdir():
        if file.is_file():
            for folder, exts in extensions.items():
                if file.suffix in exts:
                    dest = Path(directory) / folder
                    dest.mkdir(exist_ok=True)
                    shutil.move(str(file), str(dest / file.name))
```

### 🌐 网络工具

```python
# 网站状态检查器
# 位置: Website-Status-Checker/
import requests

def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {url} is UP")
        else:
            print(f"⚠️ {url} returned {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ {url} is DOWN: {e}")

# 批量检查
websites = [
    'https://google.com',
    'https://github.com',
    'https://example.com'
]

for site in websites:
    check_website(site)
```

```python
# 网页截图工具
# 位置: Website-Screenshot/
from selenium import webdriver

def take_screenshot(url, output_file):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.save_screenshot(output_file)
    driver.quit()
    print(f"Screenshot saved to {output_file}")

take_screenshot('https://example.com', 'screenshot.png')
```

### 📊 数据处理

```python
# CSV 数据分析
# 位置: CSV-Analyzer/
import pandas as pd

def analyze_csv(file_path):
    df = pd.read_csv(file_path)

    print("数据概览:")
    print(df.head())

    print("\n数据统计:")
    print(df.describe())

    print("\n缺失值:")
    print(df.isnull().sum())

    return df

df = analyze_csv('data.csv')
```

```python
# Excel 数据处理
# 位置: Excel-Processor/
import openpyxl

def process_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    # 读取数据
    for row in ws.iter_rows(values_only=True):
        print(row)

    # 写入数据
    ws['A1'] = '新数据'
    wb.save('output.xlsx')
```

### 🖼️ 图像处理

```python
# 图像压缩
# 位置: Image-Compressor/
from PIL import Image

def compress_image(input_path, output_path, quality=85):
    img = Image.open(input_path)
    img.save(output_path, optimize=True, quality=quality)
    print(f"Compressed: {input_path} -> {output_path}")

compress_image('large.jpg', 'compressed.jpg', quality=70)
```

```python
# 批量添加水印
# 位置: Watermark-Adder/
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image_path, watermark_text):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # 设置字体和位置
    font = ImageFont.truetype('arial.ttf', 36)
    width, height = img.size

    # 添加水印
    draw.text((width-200, height-50), watermark_text,
              font=font, fill=(255, 255, 255, 128))

    img.save('watermarked_' + image_path)
```

### 📧 邮件自动化

```python
# 批量发送邮件
# 位置: Email-Sender/
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    from_email = "your_email@gmail.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

    print(f"Email sent to {to_email}")

# 批量发送
recipients = ['user1@example.com', 'user2@example.com']
for recipient in recipients:
    send_email(recipient, '主题', '邮件内容')
```

### 🤖 自动化工具

```python
# 自动化表单填写
# 位置: Form-Filler/
from selenium import webdriver
from selenium.webdriver.common.by import By

def fill_form(url, data):
    driver = webdriver.Chrome()
    driver.get(url)

    # 填写表单
    driver.find_element(By.NAME, 'name').send_keys(data['name'])
    driver.find_element(By.NAME, 'email').send_keys(data['email'])
    driver.find_element(By.NAME, 'submit').click()

    driver.quit()

data = {'name': 'John Doe', 'email': 'john@example.com'}
fill_form('https://example.com/form', data)
```

### 📱 社交媒体

```python
# Twitter 自动发推
# 位置: Twitter-Bot/
import tweepy

def post_tweet(message):
    # 配置 API 密钥
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # 发推
    api.update_status(message)
    print(f"Tweet posted: {message}")

post_tweet("Hello from Python!")
```

### 🎵 多媒体处理

```python
# 音频格式转换
# 位置: Audio-Converter/
from pydub import AudioSegment

def convert_audio(input_file, output_file, output_format):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format=output_format)
    print(f"Converted: {input_file} -> {output_file}")

convert_audio('song.mp3', 'song.wav', 'wav')
```

```python
# 视频下载器
# 位置: Video-Downloader/
from pytube import YouTube

def download_video(url, output_path='.'):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path)
    print(f"Downloaded: {yt.title}")

download_video('https://youtube.com/watch?v=xxxxx')
```

## 📋 脚本目录

| 分类 | 脚本数量 | 主要功能 |
|------|---------|---------|
| 文件操作 | 15+ | 重命名、组织、压缩、加密 |
| 网络工具 | 20+ | 爬虫、下载、API 调用 |
| 数据处理 | 18+ | CSV、Excel、JSON 处理 |
| 图像处理 | 12+ | 压缩、转换、水印、滤镜 |
| 邮件自动化 | 8+ | 发送、接收、解析邮件 |
| 自动化工具 | 25+ | 表单填写、任务调度 |
| 社交媒体 | 10+ | Twitter、Instagram 自动化 |
| 多媒体 | 15+ | 音视频处理、格式转换 |
| 系统工具 | 12+ | 监控、备份、清理 |
| 安全工具 | 8+ | 密码生成、加密解密 |

## 🔧 安装

### 克隆仓库

```bash
git clone https://github.com/avinashkranjan/Amazing-Python-Scripts.git
cd Amazing-Python-Scripts
```

### 安装 Python

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3 python3-pip

# Windows
# 从 python.org 下载安装
```

### 安装依赖

```bash
# 安装常用依赖
pip install requests beautifulsoup4 pandas pillow selenium

# 或安装特定脚本的依赖
cd Script-Name
pip install -r requirements.txt
```

### 验证安装

```bash
python3 --version
pip --version
```

## 📝 使用方法

### 方法 1: 直接运行

```bash
# 进入脚本目录
cd File-Organizer

# 运行脚本
python3 file_organizer.py
```

### 方法 2: 导入使用

```python
# 将脚本作为模块导入
import sys
sys.path.append('./Amazing-Python-Scripts')

from File_Organizer import organize_files
organize_files('./downloads')
```

### 方法 3: 修改后使用

```bash
# 复制脚本到你的项目
cp Amazing-Python-Scripts/Script-Name/script.py ./my_project/

# 根据需求修改
vim my_project/script.py

# 运行
python3 my_project/script.py
```

## 📝 实用示例

### 示例 1: 自动化文件整理

```python
#!/usr/bin/env python3
"""
每天自动整理下载文件夹
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_downloads():
    downloads = Path.home() / 'Downloads'

    # 按文件类型分类
    categories = {
        'Images': ['.jpg', '.png', '.gif', '.svg'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
        'Archives': ['.zip', '.rar', '.7z', '.tar'],
        'Code': ['.py', '.js', '.html', '.css']
    }

    for file in downloads.iterdir():
        if file.is_file():
            # 跳过隐藏文件
            if file.name.startswith('.'):
                continue

            # 按类型移动
            for category, extensions in categories.items():
                if file.suffix.lower() in extensions:
                    dest_dir = downloads / category
                    dest_dir.mkdir(exist_ok=True)

                    # 如果文件已存在，添加时间戳
                    dest_file = dest_dir / file.name
                    if dest_file.exists():
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        name = file.stem + f'_{timestamp}' + file.suffix
                        dest_file = dest_dir / name

                    shutil.move(str(file), str(dest_file))
                    print(f"Moved: {file.name} -> {category}/")
                    break

if __name__ == '__main__':
    organize_downloads()
```

### 示例 2: 批量图像处理

```python
#!/usr/bin/env python3
"""
批量压缩和调整图像大小
"""
from PIL import Image
from pathlib import Path

def process_images(input_dir, output_dir, max_size=(1920, 1080), quality=85):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    for img_file in input_path.iterdir():
        if img_file.suffix.lower() in image_extensions:
            try:
                img = Image.open(img_file)

                # 调整大小（保持宽高比）
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # 保存压缩后的图像
                output_file = output_path / img_file.name
                img.save(output_file, optimize=True, quality=quality)

                # 显示文件大小变化
                original_size = img_file.stat().st_size / 1024
                new_size = output_file.stat().st_size / 1024
                reduction = (1 - new_size/original_size) * 100

                print(f"✅ {img_file.name}")
                print(f"   {original_size:.1f}KB -> {new_size:.1f}KB ({reduction:.1f}% 减少)")

            except Exception as e:
                print(f"❌ Error processing {img_file.name}: {e}")

if __name__ == '__main__':
    process_images('./images', './compressed', quality=80)
```

### 示例 3: 网站监控

```python
#!/usr/bin/env python3
"""
监控网站状态并发送通知
"""
import requests
import time
from datetime import datetime

def monitor_websites(urls, interval=300):
    """
    监控网站列表
    urls: 要监控的网站列表
    interval: 检查间隔（秒）
    """
    print(f"开始监控 {len(urls)} 个网站...")

    while True:
        for url in urls:
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                response_time = time.time() - start_time

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if response.status_code == 200:
                    print(f"[{timestamp}] ✅ {url} - {response_time:.2f}s")
                else:
                    print(f"[{timestamp}] ⚠️ {url} - Status: {response.status_code}")
                    # 这里可以添加发送通知的代码

            except requests.exceptions.RequestException as e:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}] ❌ {url} - Error: {e}")
                # 这里可以添加发送告警的代码

        print(f"\n等待 {interval} 秒后继续检查...\n")
        time.sleep(interval)

if __name__ == '__main__':
    websites = [
        'https://google.com',
        'https://github.com',
        'https://stackoverflow.com'
    ]
    monitor_websites(websites, interval=60)
```

## 🐛 常见问题

### 1. 模块未找到

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
```bash
# 安装缺失的模块
pip install module-name

# 或安装脚本的所有依赖
pip install -r requirements.txt
```

### 2. 权限错误

**症状**: `PermissionError: [Errno 13] Permission denied`

**解决方案**:
```bash
# 给脚本添加执行权限
chmod +x script.py

# 或使用 sudo 运行（谨慎使用）
sudo python3 script.py
```

### 3. 编码错误

**症状**: `UnicodeDecodeError` 或 `UnicodeEncodeError`

**解决方案**:
```python
# 指定编码
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 或在文件开头添加
# -*- coding: utf-8 -*-
```

### 4. Selenium 驱动问题

**症状**: `WebDriverException: 'chromedriver' executable needs to be in PATH`

**解决方案**:
```bash
# macOS
brew install chromedriver

# 或下载并添加到 PATH
# https://chromedriver.chromium.org/
```

### 5. PIL/Pillow 问题

**症状**: `ImportError: No module named PIL`

**解决方案**:
```bash
# 安装 Pillow（PIL 的替代品）
pip install Pillow
```

## 📖 推荐脚本

### 初学者推荐

1. **File Organizer** - 学习文件操作
2. **Simple Calculator** - 学习基础语法
3. **Password Generator** - 学习字符串处理
4. **To-Do List** - 学习数据结构
5. **Weather App** - 学习 API 调用

### 进阶推荐

1. **Web Scraper** - 学习网络爬虫
2. **Email Automation** - 学习邮件处理
3. **Image Processor** - 学习图像处理
4. **Data Analyzer** - 学习数据分析
5. **Automation Bot** - 学习自动化

### 实用工具推荐

1. **Bulk File Renamer** - 批量重命名
2. **PDF Merger** - PDF 合并
3. **Video Downloader** - 视频下载
4. **System Monitor** - 系统监控
5. **Backup Tool** - 自动备份

## 📖 参考资料

- **GitHub 仓库**: https://github.com/avinashkranjan/Amazing-Python-Scripts
- **Python 官方文档**: https://docs.python.org/3/
- **常用库文档**:
  - Requests: https://requests.readthedocs.io/
  - Pandas: https://pandas.pydata.org/docs/
  - Pillow: https://pillow.readthedocs.io/
  - Selenium: https://selenium-python.readthedocs.io/

## 📝 更新日志

### v0.2.0 (2026-01-26)
- ✨ 更新到最新版本 (905b1e6)
- 📝 完善文档和使用示例
- ✨ 添加脚本分类说明
- ✨ 添加常见问题解答
- ✨ 添加实用示例代码
- ✨ 添加推荐脚本列表

### v0.1.0 (2026-01-25)
- 🎉 初始版本
