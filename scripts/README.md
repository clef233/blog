# 博客文章同步和格式化工具

## 📋 功能介绍

这个工具集包含一个Python脚本和批处理文件，用于自动化处理博客文章：

1. **格式化现有文件** - 为没有Front Matter的Markdown文件添加Hugo标准格式
2. **从Obsidian同步** - 自动从Obsidian文件夹复制新的阅读笔记到博客目录
3. **智能格式化** - 自动生成合适的标题、标签和分类

## 🚀 快速开始

### 方法一：使用批处理文件（推荐）

双击运行 `scripts\sync.bat`，然后选择相应选项：

- **选项1** - 格式化现有文件
- **选项2** - 从Obsidian同步新文件
- **选项3** - 执行完整流程
- **选项4-6** - 预览模式（不实际修改文件）

### 方法二：直接运行Python脚本

```bash
# 格式化现有文件
python scripts/blog_sync.py --format

# 从Obsidian同步文件
python scripts/blog_sync.py --sync

# 执行完整流程
python scripts/blog_sync.py --all

# 预览模式（不实际修改）
python scripts/blog_sync.py --all --dry-run
```

## 📁 路径配置

脚本中的默认路径：

- **博客文章目录**: `D:\Projects\blog\content\posts\2025`
- **Obsidian源目录**: `D:\iCloud\DATA\iCloudDrive\iCloud~md~obsidian\下水道\阅读笔记\扩展阅读`

如果您的路径不同，请修改 `scripts/blog_sync.py` 中的配置：

```python
self.blog_dir = Path(r"你的博客目录")
self.posts_dir = self.blog_dir / "content" / "posts" / "2025"
self.obsidian_dir = Path(r"你的Obsidian目录")
```

## 🎯 Front Matter格式

脚本会自动生成以下格式的Front Matter：

```yaml
---
title: "文章标题"
date: 2025-10-22T12:00:00Z
draft: false
description: "文章描述"
tags: ["学术笔记", "阅读笔记", "同步", "政治学"]
categories: ["学术笔记"]
author: "clef233"
showToc: true
TocOpen: false
---
```

## 🏷️ 智能标签识别

脚本会根据文章内容自动添加标签：

- 包含"政治"、"国家"、"民主"、"权力" → 添加"政治学"
- 包含"社会"、"文化"、"结构"、"制度" → 添加"社会学"
- 包含"哲学"、"思想"、"认识"、"真理" → 添加"哲学"
- 包含"经济"、"资本"、"市场"、"发展" → 添加"经济学"

## ⚠️ 注意事项

1. **备份重要文件** - 脚本会修改文件，请确保已备份重要内容
2. **预览模式** - 首次使用建议使用 `--dry-run` 预览模式
3. **重复文件** - 如果目标文件已存在，脚本会跳过以避免覆盖
4. **编码问题** - 脚本使用UTF-8编码处理文件

## 🔧 自定义配置

您可以修改脚本中的以下设置：

```python
# 默认标签
self.default_tags = ["学术笔记", "阅读笔记", "同步"]

# 默认分类
self.default_categories = ["学术笔记"]

# 作者名
self.author = "clef233"
```

## 📝 工作流程建议

1. **第一次使用**：
   ```bash
   python scripts/blog_sync.py --format --dry-run
   ```

2. **检查预览结果**，确认无误后：
   ```bash
   python scripts/blog_sync.py --format
   ```

3. **提交更改**：
   ```bash
   git add .
   git commit -m "格式化博客文章"
   git push origin main
   ```

4. **日常同步**：
   ```bash
   python scripts/blog_sync.py --all
   git add .
   git commit -m "同步新文章"
   git push origin main
   ```

## 🐛 故障排除

### Python未找到
确保Python已安装并在PATH中，或者使用完整路径：
```bash
python3 scripts/blog_sync.py --all
```

### 路径不存在
检查路径是否正确，Obsidian目录是否存在：
```python
python scripts/blog_sync.py --all --dry-run
```

### 文件编码错误
脚本使用UTF-8编码，如果遇到编码问题，请确保源文件编码正确。

## 📊 脚本特性

- ✅ 自动检测已有Front Matter
- ✅ 智能提取标题和描述
- ✅ 基于内容自动分类
- ✅ 支持预览模式
- ✅ 避免重复处理
- ✅ 详细的操作日志
- ✅ 中文路径支持
- ✅ 批量处理能力