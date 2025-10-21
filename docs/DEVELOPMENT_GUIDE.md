# Hugo 博客开发指南

## 快速开始

### 环境要求
- Hugo 0.120+
- Git
- Node.js 18+ (可选，用于额外功能)
- Obsidian (推荐)

### 安装 Hugo

#### Windows (推荐使用 Chocolatey)
```bash
choco install hugo-extended
```

#### macOS (推荐使用 Homebrew)
```bash
brew install hugo
```

#### Linux
```bash
sudo apt install hugo  # Ubuntu/Debian
sudo dnf install hugo  # Fedora
```

### 验证安装
```bash
hugo version
```

## 开发工作流

### 1. 本地开发
```bash
# 启动开发服务器
hugo server -D --buildDrafts --buildFuture

# 访问 http://localhost:1313
```

### 2. 创建新文章
```bash
# 使用模板创建新文章
hugo new posts/2025/my-new-post.md

# 创建草稿
hugo new posts/2025/draft-post.md --kind draft
```

### 3. 构建和部署
```bash
# 构建生产版本
hugo --minify

# 预览构建结果
hugo server --buildDrafts=false --buildFuture=false
```

## Obsidian 集成指南

### 设置工作区
1. 打开 Obsidian
2. 选择"打开文件夹作为仓库"
3. 选择项目的 `content/` 目录
4. 配置附件设置：
   - 设置 → 文件与链接 → 默认附件存储位置：`当前文件夹下指定子文件夹`
   - 新附件的默认位置：`images`

### 文章模板
在 Obsidian 中创建模板文件 `Templates/博客文章.md`：
```markdown
---
title: "{{title}}"
date: {{date}}
draft: false
tags: []
categories: []
author: "作者名"
description: ""
keywords: []
---

# 文章摘要

<!--more-->

# 正文内容
```

### Obsidian 插件推荐
1. **Templater** - 自动化模板
2. **Image auto upload** - 图片自动上传
3. **Tag Wrangler** - 标签管理
4. **Linter** - 格式化 Markdown

## Git 工作流

### 分支策略
```
main          # 生产环境分支
develop       # 开发环境分支
feature/*     # 功能开发分支
hotfix/*      # 紧急修复分支
```

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

### 提交示例
```bash
git commit -m "feat(posts): 添加文章阅读时间估算功能

- 实现阅读时间自动计算
- 添加配置选项
- 更新文章元数据模板

🤖 Generated with Claude Code"
```

## 测试策略

### 本地测试检查清单
- [ ] Hugo 服务器正常启动
- [ ] 所有页面正常加载
- [ ] 主题切换功能正常
- [ ] 搜索功能正常
- [ ] 移动端显示正常
- [ ] 图片加载正确
- [ ] 代码高亮正常
- [ ] 数学公式渲染正确

### 性能测试
```bash
# 本地性能测试
npx lighthouse http://localhost:1313 --output html --output-path ./lighthouse-report.html

# 在线性能测试
# 1. Google PageSpeed Insights
# 2. GTmetrix
# 3. WebPageTest
```

### 部署前检查
```bash
# 构建检查
hugo --minify --buildDrafts=false --buildFuture=false

# 检查输出目录
ls -la public/

# 检查文件大小
du -sh public/
```

## 常见问题解决

### Hugo 构建问题
1. **版本不兼容**
   ```bash
   # 更新 Hugo
   brew upgrade hugo  # macOS
   choco upgrade hugo  # Windows
   ```

2. **主题问题**
   ```bash
   # 更新主题子模块
   git submodule update --remote themes/PaperMod
   ```

3. **配置错误**
   ```bash
   # 验证配置文件
   hugo config
   ```

### GitHub Actions 问题
1. **构建失败**
   - 检查 YAML 语法
   - 查看 Actions 日志
   - 验证 Hugo 版本

2. **部署失败**
   - 检查 GitHub Pages 设置
   - 验证仓库权限
   - 检查自定义域名配置

### 内容问题
1. **图片不显示**
   - 检查图片路径
   - 验证文件大小
   - 检查文件格式

2. **Markdown 渲染问题**
   - 检查语法错误
   - 验证特殊字符转义
   - 检查 Front Matter 格式

## 性能优化建议

### 图片优化
```bash
# 使用 WebP 格式
# 添加到 config.yaml
markup:
  goldmark:
    renderer:
      unsafe: true
```

### 缓存策略
```yaml
# config.yaml
params:
    assets:
      disableHLJS: true
      favicon: "/favicon.ico"
      favicon16x16: "/favicon-16x16.png"
      favicon32x32: "/favicon-32x32.png"
      apple_touch_icon: "/apple-touch-icon.png"
      safari_pinned_tab: "/safari-pinned-tab.svg"
```

### CDN 配置
```yaml
# 使用 Cloudflare 或其他 CDN
baseURL: 'https://username.github.io'
canonifyURLs: true
```

## 安全配置

### CSP 头部
```yaml
# config.yaml
params:
    csp:
      child-src: 'none'
      font-src: 'self'
      form-src: 'self'
      frame-src: 'none'
      img-src: 'self data:'
      object-src: 'none'
      style-src: 'self 'unsafe-inline''
      script-src: 'self'
      worker-src: 'none'
```

### HTTPS 强制
```yaml
# config.yaml
params:
    forceHTTPS: true
    enableRobotsTXT: true
```

## 维护和更新

### 定期维护任务
1. **每月更新**
   ```bash
   # 更新 Hugo
   hugo version

   # 更新主题
   git submodule update --remote --merge

   # 更新依赖
   npm update  # 如果使用 npm
   ```

2. **季度检查**
   - 性能测试
   - 安全扫描
   - 备份检查

3. **年度审查**
   - 技术栈评估
   - 架构优化
   - 内容归档

### 备份策略
```bash
# 完整备份
git archive HEAD --format=zip --output=blog-backup-$(date +%Y%m%d).zip

# 配置备份
cp config.yaml config.yaml.backup
cp -r static/ static-backup/
```

## 扩展功能

### 评论系统配置
```yaml
# Giscus 配置
params:
    comments:
      enable: true
      type: giscus
      giscus:
        repo: "username/blog"
        repoId: "R_kgDOG..."
        category: "Announcements"
        categoryId: "DIC_kwDOG..."
        mapping: "pathname"
        strict: 0
        reactionsEnabled: 1
        emitMetadata: 0
        inputPosition: "bottom"
        lang: "zh-CN"
```

### 分析工具集成
```yaml
# Google Analytics
params:
    analytics:
      google:
        SiteVerificationTag: "your-verification-code"

# Cloudflare Analytics
params:
    analytics:
      cloudflare:
        token: "your-cloudflare-token"
```

### 社交媒体集成
```yaml
params:
    social:
      twitter: "username"
      github: "username"
      instagram: "username"
      linkedin: "username"
```

## 参考资源

### 官方文档
- [Hugo 官方文档](https://gohugo.io/documentation/)
- [PaperMod 主题文档](https://adityatelange.github.io/hugo-PaperMod/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)

### 社区资源
- [Hugo 论坛](https://discourse.gohugo.io/)
- [Hugo GitHub](https://github.com/gohugoio/hugo)
- [PaperMod GitHub](https://github.com/adityatelange/hugo-PaperMod)

### 工具和插件
- [Hugo 安装器](https://github.com/schnerring/hugo-installer)
- [Obsidian 插件市场](https://obsidian.md/plugins)
- [Markdown 编辑器](https://www.markdownguide.org/basic-syntax/)

---

**文档版本**: v1.0
**创建日期**: 2025-10-21
**最后更新**: 2025-10-21
**维护者**: 开发团队