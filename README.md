# Hugo 博客系统

一个基于 Hugo + PaperMod 的现代化博客系统，支持 Obsidian 本地编辑和 GitHub Pages 自动部署。

## 🚀 特性

- ⚡ **极速构建** - Hugo 极快的构建速度
- 🎨 **现代设计** - PaperMod 主题，支持深色/浅色模式
- 📝 **Obsidian 集成** - 本地 Markdown 编辑器支持
- 🔄 **自动部署** - Git 推送自动部署到 GitHub Pages
- 🔍 **全文搜索** - 快速搜索博客内容
- 💬 **评论系统** - 集成 Giscus 评论功能
- 📱 **响应式设计** - 完美适配移动端和桌面端
- ⚡ **性能优化** - 图片优化、懒加载、CDN 支持
- 🌐 **SEO 友好** - 自动生成 sitemap、RSS、meta 标签

## 📋 技术栈

- **静态网站生成器**: Hugo 0.120+
- **主题**: PaperMod
- **内容管理**: Obsidian
- **版本控制**: Git
- **部署平台**: GitHub Pages
- **CI/CD**: GitHub Actions
- **评论系统**: Giscus

## 🛠️ 快速开始

### 环境要求

- Hugo 0.120+
- Git
- Obsidian (推荐)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/username/blog.git
   cd blog
   ```

2. **初始化子模块**
   ```bash
   git submodule update --init --recursive
   ```

3. **启动开发服务器**
   ```bash
   hugo server -D
   ```

4. **访问本地网站**
   ```
   http://localhost:1313
   ```

## 📖 使用指南

### 创建新文章

```bash
# 创建新文章
hugo new posts/2025/my-new-post.md

# 创建草稿
hugo new posts/2025/draft-post.md --kind draft
```

### 文章结构

每篇文章应包含以下 Front Matter：

```yaml
---
title: "文章标题"
date: 2025-10-21T10:00:00Z
draft: false
tags: ["标签1", "标签2"]
categories: ["分类"]
author: "作者名"
description: "文章描述"
keywords: ["关键词1", "关键词2"]
---
```

### Obsidian 集成

1. 在 Obsidian 中打开 `content/` 目录
2. 使用提供的模板创建新文章
3. 图片自动保存在文章同级目录的 `images/` 文件夹
4. Git 提交后自动部署到线上

## 🚀 部署

### 自动部署 (推荐)

1. 将代码推送到 GitHub
   ```bash
   git add .
   git commit -m "feat: 添加新文章"
   git push origin main
   ```

2. GitHub Actions 自动构建并部署到 GitHub Pages

### 手动部署

```bash
# 构建生产版本
hugo --minify

# 部署 public/ 目录到 GitHub Pages
```

## 📁 项目结构

```
blog/
├── content/              # 博客内容
│   ├── posts/           # 文章目录
│   ├── about/           # 关于页面
│   └── _index.md        # 首页
├── static/              # 静态资源
├── themes/              # 主题文件
├── config.yaml          # Hugo 配置
├── docs/                # 项目文档
│   ├── PRD.md          # 产品需求文档
│   ├── FSD.md          # 功能规格文档
│   └── DEVELOPMENT_GUIDE.md  # 开发指南
├── .github/             # GitHub Actions
└── README.md           # 项目说明
```

## ⚙️ 配置说明

### 主要配置项 (config.yaml)

```yaml
# 基础设置
baseURL: 'https://username.github.io'
languageCode: 'zh-cn'
title: '我的博客'
theme: 'PaperMod'

# 参数设置
params:
  defaultTheme: auto
  disableThemeToggle: false
  env: production

  # SEO 设置
  description: "个人技术博客"
  keywords: ["博客", "技术", "分享"]
  author: "作者名"

  # 社交媒体
  socialIcons:
    - name: "github"
      url: "https://github.com/username"
    - name: "twitter"
      url: "https://twitter.com/username"
```

### 评论系统配置

```yaml
params:
  comments:
    enable: true
    type: giscus
    giscus:
      repo: "username/blog"
      repoId: "your-repo-id"
      category: "Announcements"
      categoryId: "your-category-id"
      mapping: "pathname"
      lang: "zh-CN"
```

## 🧪 测试

### 运行测试

```bash
# 运行完整测试套件
./scripts/test_all.sh

# 运行特定测试
./scripts/test_config_validation.sh
```

### 性能测试

```bash
# 本地性能测试
npx lighthouse http://localhost:1313 --output html
```

## 📝 开发规范

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```bash
feat: 新功能
fix: 修复问题
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建工具或辅助工具的变动
```

### 分支策略

```
main          # 生产环境
develop       # 开发环境
feature/*     # 功能开发
hotfix/*      # 紧急修复
```

## 🛡️ 安全和性能

### 安全特性
- HTTPS 强制访问
- CSP 内容安全策略
- XSS 防护
- 敏感信息保护

### 性能优化
- 图片懒加载和压缩
- CSS/JS 压缩和合并
- CDN 缓存策略
- Google PageSpeed 优化

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Hugo](https://gohugo.io/) - 静态网站生成器
- [PaperMod](https://github.com/adityatelange/hugo-PaperMod) - 现代化主题
- [Obsidian](https://obsidian.md/) - 强大的 Markdown 编辑器
- [GitHub Pages](https://pages.github.com/) - 免费静态网站托管

## 📞 联系方式

- 博客: https://username.github.io
- GitHub: https://github.com/username
- Email: your.email@example.com

---

⭐ 如果这个项目对你有帮助，请给它一个星标！

**注意**: 使用前请修改 `config.yaml` 中的 `baseURL` 和其他个人信息配置。