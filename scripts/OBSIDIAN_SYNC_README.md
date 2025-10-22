# Obsidian 到 Hugo 同步脚本

这个脚本可以自动将 Obsidian 仓库中的 Markdown 文件同步到 Hugo 博客系统，自动处理元数据、链接格式转换和 Frontmatter 生成。

## 功能特性

- ✅ 自动解析 Obsidian Frontmatter 元数据
- ✅ 转换 Obsidian 风格链接 `[[文件名]]` 为标准 Markdown 链接
- ✅ 自动提取文章标题、标签、分类
- ✅ 生成 Hugo 兼容的 YAML Frontmatter
- ✅ 按年份自动组织文章目录结构
- ✅ 支持排除特定文件和目录
- ✅ 详细的日志记录和错误处理
- ✅ 可配置的同步选项

## 安装依赖

```bash
pip install pyyaml
```

## 使用方法

### 基本用法

```bash
python obsidian_sync.py \
  --obsidian-vault "D:/Obsidian/MyVault" \
  --hugo-content "D:/Projects/blog/content" \
  --author "你的名字"
```

### 使用配置文件

1. 复制并修改 `sync_config.yaml` 配置文件
2. 运行脚本：

```bash
python obsidian_sync.py \
  --obsidian-vault "你的Obsidian路径" \
  --hugo-content "你的Hugo内容路径"
```

### 命令行参数

- `--obsidian-vault`: Obsidian 仓库路径（必需）
- `--hugo-content`: Hugo 内容目录路径（必需）
- `--author`: 默认作者名称（默认: clef233）
- `--log-level`: 日志级别（DEBUG/INFO/WARNING/ERROR）
- `--dry-run`: 预览模式，显示将要处理的文件但不实际同步

## 配置选项

### `sync_config.yaml` 配置说明

```yaml
# Obsidian 仓库路径
obsidian_vault_path: "D:/Obsidian/Vault"

# Hugo 内容目录路径
hugo_content_path: "D:/Projects/blog/content"

# 默认作者
default_author: "clef233"

# 默认分类
default_categories:
  - "博客文章"

# 默认标签
default_tags: []

# 时区设置
timezone: "Asia/Shanghai"

# 排除模式（正则表达式）
exclude_patterns:
  - ".*\\.excalidraw$"
  - ".*\\.canvas$"
  - ".*/_templates/.*"
  - ".*/\\.obsidian/.*"
```

## Obsidian 文件格式要求

### 推荐的 Obsidian 文件格式

```markdown
---
title: "文章标题"
created: 2025-10-22T10:00:00
tags: ["标签1", "标签2"]
categories: ["分类"]
description: "文章描述"
---

# 文章标题

这是文章内容...

## 内容格式

### 标题层级
使用 # 号表示标题层级：
# H1 标题
## H2 标题
### H3 标题

### 链接格式
- 内部链接：`[[其他文件]]` 会被自动转换为 `[其他文件](其他文件.md)`
- 图片链接：`![[图片.png]]` 会被自动转换为 `![图片](图片.png)`

### 标签格式
- 内容标签：`#标签名` 会被自动提取
- Frontmatter 标签：在 YAML 中定义 `tags: ["标签1", "标签2"]`

### 注释格式
Obsidian 风格的注释 `%%这是注释%%` 会被自动移除
```

## 输出文件结构

脚本会在 Hugo 内容目录下创建以下结构：

```
content/
├── posts/
│   ├── 2025/
│   │   ├── 文章标题1.md
│   │   ├── 文章标题2.md
│   │   └── ...
│   ├── 2024/
│   └── ...
```

### 生成的 Hugo Frontmatter 示例

```yaml
title: 文章标题
date: 2025-10-22T10:00:00+0800
draft: false
author: clef233
description: 文章描述
summary: 文章描述
categories:
  - 博客文章
tags:
  - 标签1
  - 标签2
showToc: true
TocOpen: false
```

## 工作流程

1. **扫描 Obsidian 仓库**：查找所有 Markdown 文件
2. **过滤文件**：根据排除模式跳过特定文件
3. **解析内容**：提取 Frontmatter 和正文内容
4. **转换格式**：
   - 转换 Obsidian 链接为标准 Markdown
   - 移除 Obsidian 注释
   - 提取标签和元数据
5. **生成 Frontmatter**：创建 Hugo 兼容的 YAML 元数据
6. **写入文件**：按年份组织并保存到 Hugo 内容目录

## 日志和错误处理

脚本会生成详细的日志文件 `obsidian_sync.log`，包含：

- 处理的文件列表
- 跳过的文件及原因
- 转换过程中的警告和错误
- 同步统计信息

## 常见问题

### Q: 如何处理中文文件名？
A: 脚本会自动清理文件名中的特殊字符，保持文件名系统兼容性。

### Q: 如何同步图片和附件？
A: 目前脚本主要处理 Markdown 文件，图片同步功能可以在后续版本中添加。

### Q: 如何自定义 Frontmatter 字段？
A: 可以修改脚本中的 `HugoFrontmatterGenerator` 类来自定义字段映射。

### Q: 如何处理已经存在的文件？
A: 脚本会覆盖已存在的文件，建议在同步前备份重要内容。

## 开发和扩展

### 添加新的内容处理器

```python
class CustomContentProcessor:
    def process(self, content: str) -> str:
        # 自定义内容处理逻辑
        return processed_content

# 在主脚本中注册
synchronizer.add_content_processor(CustomContentProcessor())
```

### 自定义 Frontmatter 生成

```python
class CustomFrontmatterGenerator(HugoFrontmatterGenerator):
    def generate_frontmatter(self, ...):
        frontmatter = super().generate_frontmatter(...)
        # 添加自定义字段
        frontmatter['custom_field'] = 'custom_value'
        return frontmatter
```

## 示例用法

### 从你的 Obsidian 仓库同步到博客

```bash
# 基本同步
python obsidian_sync.py \
  --obsidian-vault "D:/iCloud/DATA/iCloudDrive/iCloud~md~obsidian/下水道" \
  --hugo-content "D:/Projects/blog/content" \
  --author "clef233"

# 预览模式（不实际修改文件）
python obsidian_sync.py \
  --obsidian-vault "D:/iCloud/DATA/iCloudDrive/iCloud~md~obsidian/下水道" \
  --hugo-content "D:/Projects/blog/content" \
  --dry-run

# 详细日志
python obsidian_sync.py \
  --obsidian-vault "D:/iCloud/DATA/iCloudDrive/iCloud~md~obsidian/下水道" \
  --hugo-content "D:/Projects/blog/content" \
  --log-level DEBUG
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个脚本！