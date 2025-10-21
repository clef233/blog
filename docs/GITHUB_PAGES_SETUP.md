# GitHub Pages 设置指南

## 概述

本指南详细说明如何配置 GitHub Pages 以自动部署 Hugo 博客网站。

## 前置条件

1. **GitHub 账户**: 确保你有 GitHub 账户
2. **代码仓库**: 项目已经推送到 GitHub 仓库
3. **分支保护**: 确保 main 分支受保护（可选但推荐）

## 仓库设置

### 1. 创建 GitHub 仓库

```bash
# 如果还没有创建远程仓库
git remote add origin https://github.com/username/blog.git
git branch -M main
git push -u origin main
```

### 2. 配置 GitHub Pages

1. **进入仓库设置**
   - 访问你的 GitHub 仓库
   - 点击 **Settings** 标签页
   - 在左侧菜单中找到 **Pages**

2. **配置构建源**
   - **Source**: 选择 **GitHub Actions**
   - 这样配置会让 GitHub Actions 控制部署过程

3. **自定义域名（可选）**
   - 如果你想使用自定义域名：
   - 在 **Custom domain** 中输入你的域名
   - 配置 DNS 记录指向 GitHub Pages

## GitHub Actions 配置

### 工作流文件说明

项目已包含两个主要工作流：

#### 1. 部署工作流 (`.github/workflows/deploy.yml`)

```yaml
name: Deploy Hugo to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  pages: write
  id-token: write
```

**功能**:
- 当代码推送到 main 分支时自动构建和部署
- 支持 Pull Request 触发的测试构建
- 使用最新的 Hugo 版本
- 自动压缩和优化资源

#### 2. 链接检查工作流 (`.github/workflows/link-check.yml`)

```yaml
name: Link Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # 每日检查
```

**功能**:
- 检查网站中的所有链接是否有效
- 定期检查已发布网站的链接状态
- 在 Pull Request 中报告链接问题

## 首次部署流程

### 1. 推送代码到 GitHub

```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "feat: 初始化Hugo博客项目

- 完成基础配置
- 配置PaperMod主题
- 设置GitHub Actions自动部署

🤖 Generated with Claude Code"

# 推送到远程仓库
git push origin main
```

### 2. 监控部署状态

1. **访问 GitHub Actions**
   - 在仓库中点击 **Actions** 标签页
   - 查看正在运行的工作流

2. **检查部署结果**
   - 成功的部署会显示绿色 ✓ 标记
   - 失败的部署会显示红色 ✗ 标记，点击查看错误日志

3. **验证网站访问**
   - 部署完成后访问: `https://username.github.io`
   - 确认网站内容正常显示

### 3. 常见部署问题排查

#### 构建失败

**检查 GitHub Actions 日志**:
1. 进入 **Actions** 页面
2. 点击失败的构建任务
3. 查看详细的错误信息

**常见原因**:
- Hugo 配置文件语法错误
- 主题配置问题
- 内容文件格式错误
- Git 子模块问题

#### 部署权限问题

**确认权限设置**:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

**启用 GitHub Pages**:
- 确保 **Settings > Pages** 中已启用
- 选择 **GitHub Actions** 作为构建源

#### 自定义域名问题

**DNS 配置**:
```bash
# A 记录
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153

# CNAME 记录（可选）
www.yourdomain.com -> username.github.io
```

**HTTPS 证书**:
- GitHub Pages 会自动为自定义域名配置 SSL 证书
- 证书配置可能需要几分钟到几小时

## 高级配置

### 1. 环境变量配置

在 GitHub 仓库设置中配置环境变量：

**Settings > Secrets and variables > Actions > New repository secret**

| 变量名 | 描述 | 示例值 |
|---------|------|--------|
| `HUGO_VERSION` | Hugo 版本 | `latest` |
| `GOOGLE_ANALYTICS_ID` | Google Analytics ID | `G-XXXXXXXXXX` |
| `GISCUS_REPO_ID` | Giscus 仓库ID | `R_kgDOG...` |

### 2. 构建优化

#### 缓存配置

```yaml
- name: Setup Hugo Cache
  uses: actions/cache@v3
  with:
    path: /tmp/hugo_cache
    key: ${{ runner.os }}-hugomod-${{ hashFiles('**/go.sum') }}
```

#### 并行构建

```yaml
strategy:
  matrix:
    os: [ubuntu-latest]
    hugo-version: [latest]
```

### 3. 多环境部署

#### 开发环境

```yaml
# .github/workflows/deploy-dev.yml
name: Deploy to Development

on:
  push:
    branches: [ develop ]

jobs:
  deploy-dev:
    runs-on: ubuntu-latest
    environment: development
    # ... 部署到开发环境
```

#### 生产环境

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy to Production

on:
  push:
    tags: [ 'v*' ]  # 标签触发

jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production
    # ... 部署到生产环境
```

## 性能优化

### 1. 图片优化

GitHub Pages 不自动优化图片，建议：

```yaml
# 在 Hugo 配置中启用图片处理
imaging:
  resampleFilter: CatmullRom
  quality: 75
  anchor: smart
```

### 2. 资源压缩

```yaml
# 在构建时启用压缩
minify:
  disableXML: true
  minifyOutput: true
```

### 3. CDN 配置

GitHub Pages 内置了全球 CDN，但可以配置自定义 CDN：

```yaml
# config.yaml
baseURL: 'https://cdn.yourdomain.com'
canonifyURLs: true
```

## 监控和维护

### 1. 网站监控

#### GitHub Actions 状态
- 设置邮件通知构建失败
- 使用 GitHub Status 页面监控服务状态

#### 外部监控服务
- Uptime Robot
- Pingdom
- StatusCake

### 2. 定期维护

#### 每月检查
- [ ] 检查 GitHub Actions 执行状态
- [ ] 更新 Hugo 版本
- [ ] 清理旧的工作流运行记录
- [ ] 检查域名和 SSL 证书状态

#### 每季度检查
- [ ] 分析网站性能
- [ ] 检查安全配置
- [ ] 更新依赖项
- [ ] 审查访问统计

### 3. 备份策略

#### 内容备份
```bash
# 定期备份内容
git archive HEAD --format=zip --output=blog-backup-$(date +%Y%m%d).zip

# 备份配置文件
cp hugo.yaml hugo.yaml.backup
cp -r static/ static-backup/
```

#### 仓库镜像
- 考虑设置仓库镜像到其他平台
- 使用 GitHub 的备份功能

## 故障排除

### 常见错误和解决方案

#### 1. "Page build failed"

**原因**: HTML/CSS/JS 语法错误
**解决**: 检查生成的 HTML 文件，验证模板语法

#### 2. "404 Not Found"

**原因**: 路径配置错误或文件缺失
**解决**:
- 检查 `baseURL` 配置
- 确认文件在正确位置
- 验证 `hugo.yaml` 配置

#### 3. "Permission denied"

**原因**: GitHub Actions 权限不足
**解决**: 检查工作流文件中的权限配置

#### 4. "Submodule not found"

**原因**: Git 子模块配置问题
**解决**:
```bash
git submodule update --init --recursive
git submodule update --remote --merge
```

### 调试技巧

#### 本地测试
```bash
# 使用与 GitHub Actions 相同的命令
hugo --gc --minify --buildDrafts=false --buildFuture=false

# 检查生成的文件
ls -la public/
```

#### 详细构建日志
```bash
# 启用详细日志
hugo --gc --minify --verbose
```

#### 模板调试
```bash
# 检查模板渲染
hugo server --disableFastRender
```

## 最佳实践

### 1. 安全配置

- 使用 HTTPS 强制访问
- 配置适当的 CORS 策略
- 定期更新依赖项
- 限制 GitHub Actions 权限

### 2. 性能优化

- 压缩所有静态资源
- 使用适当的图片格式和尺寸
- 启用浏览器缓存
- 使用 Content Security Policy

### 3. SEO 优化

- 配置正确的元标签
- 生成 sitemap.xml
- 使用语义化 HTML
- 配置 robots.txt

### 4. 版本管理

- 使用语义化版本标签
- 保持主分支的稳定性
- 使用功能分支进行开发
- 定期合并和发布

---

**文档版本**: v1.0
**创建日期**: 2025-10-21
**最后更新**: 2025-10-21
**维护者**: 开发团队

## 参考资源

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [Hugo 部署指南](https://gohugo.io/hosting-and-deployment/hosting-on-github/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [GitHub Pages 最佳实践](https://docs.github.com/en/pages/getting-started-with-github-pages/best-practices-for-your-github-pages-site)