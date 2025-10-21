# Hugo 博客系统 UI 设计指导

## 项目概述

### 设计目标
创建一个现代化、简洁、易读的个人博客界面，强调内容可读性和用户体验。

### 目标用户
- **主要用户**: 技术博客读者、开发者、学生
- **使用场景**: 桌面端深度阅读、移动端碎片化阅读
- **用户需求**: 快速找到信息、舒适阅读体验、便捷的交互操作

### 设计原则
1. **内容为王**: 突出文章内容，减少视觉干扰
2. **简洁优雅**: 采用简约设计风格，避免过度装饰
3. **响应式**: 完美适配桌面端、平板和移动设备
4. **可访问性**: 符合 WCAG 2.1 AA 标准
5. **性能优先**: 轻量级设计，确保快速加载

## 视觉设计系统

### 色彩方案

#### 主色调
```css
/* 深色模式 */
:root {
  --primary-color: #3b82f6;        /* 蓝色 - 主要交互元素 */
  --secondary-color: #64748b;      /* 灰蓝 - 次要信息 */
  --accent-color: #f59e0b;         /* 橙色 - 强调和链接 */
  --background-primary: #0f172a;   /* 深蓝黑 - 主背景 */
  --background-secondary: #1e293b; /* 深灰 - 次背景 */
  --text-primary: #f1f5f9;         /* 浅灰 - 主文字 */
  --text-secondary: #94a3b8;       /* 中灰 - 次文字 */
  --border-color: #334155;         /* 边框色 */
}

/* 浅色模式 */
:root {
  --primary-color: #2563eb;
  --secondary-color: #64748b;
  --accent-color: #ea580c;
  --background-primary: #ffffff;
  --background-secondary: #f8fafc;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --border-color: #e2e8f0;
}
```

#### 语义化颜色
```css
:root {
  --success-color: #10b981;    /* 成功状态 */
  --warning-color: #f59e0b;    /* 警告状态 */
  --error-color: #ef4444;      /* 错误状态 */
  --info-color: #3b82f6;       /* 信息状态 */
}
```

### 字体系统

#### 字体族
```css
/* 中文字体栈 */
--font-chinese: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;

/* 英文字体栈 */
--font-english: "Inter", "Helvetica Neue", "Arial", sans-serif;

/* 等宽字体 */
--font-mono: "JetBrains Mono", "Fira Code", "Consolas", monospace;

/* 系统字体 */
--font-system: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```

#### 字体大小层级
```css
/* 标题层级 */
--font-size-h1: 2.25rem;    /* 36px */
--font-size-h2: 1.875rem;   /* 30px */
--font-size-h3: 1.5rem;     /* 24px */
--font-size-h4: 1.25rem;    /* 20px */
--font-size-h5: 1.125rem;   /* 18px */
--font-size-h6: 1rem;       /* 16px */

/* 正文层级 */
--font-size-body-large: 1.125rem;  /* 18px */
--font-size-body: 1rem;            /* 16px */
--font-size-body-small: 0.875rem;  /* 14px */
--font-size-caption: 0.75rem;      /* 12px */

/* 代码字体 */
--font-size-code: 0.875rem;        /* 14px */
```

#### 行高和字重
```css
/* 行高 */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;

/* 字重 */
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### 间距系统

#### 基础间距单位
```css
--space-xs: 0.25rem;    /* 4px */
--space-sm: 0.5rem;     /* 8px */
--space-md: 1rem;       /* 16px */
--space-lg: 1.5rem;     /* 24px */
--space-xl: 2rem;       /* 32px */
--space-2xl: 3rem;      /* 48px */
--space-3xl: 4rem;      /* 64px */
```

#### 组件间距
```css
--component-padding-sm: 0.75rem;   /* 12px */
--component-padding-md: 1rem;      /* 16px */
--component-padding-lg: 1.5rem;    /* 24px */
--component-gap: 1.5rem;           /* 24px */
```

### 阴影系统

```css
/* 轻微阴影 */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

/* 标准阴影 */
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);

/* 较深阴影 */
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);

/* 导航栏阴影 */
--shadow-navbar: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
```

### 圆角系统

```css
--radius-sm: 0.25rem;   /* 4px - 小元素 */
--radius-md: 0.375rem;  /* 6px - 按钮、输入框 */
--radius-lg: 0.5rem;    /* 8px - 卡片 */
--radius-xl: 0.75rem;   /* 12px - 大卡片 */
--radius-full: 9999px;  /* 圆形元素 */
```

## 布局设计

### 网格系统

#### 桌面端布局 (1200px+)
```
┌─────────────────────────────────────────────────────────────┐
│                        导航栏                              │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────────────────────────────────────┐ │
│ │          │ │                                          │ │
│ │  侧边栏   │ │              主内容区                    │ │
│ │          │ │                                          │ │
│ │          │ │                                          │ │
│ └──────────┘ └──────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                        页脚                               │
└─────────────────────────────────────────────────────────────┘

最大宽度: 1200px
侧边栏宽度: 280px
内容间距: 32px
```

#### 平板端布局 (768px - 1199px)
```
┌─────────────────────────────────────────────────────┐
│                    导航栏                          │
├─────────────────────────────────────────────────────┤
│                                                    │
│                  主内容区                          │
│                                                    │
│                                                    │
├─────────────────────────────────────────────────────┤
│                    页脚                            │
└─────────────────────────────────────────────────────┘

内容内边距: 24px
```

#### 移动端布局 (< 768px)
```
┌─────────────────────────────────┐
│              导航栏             │
├─────────────────────────────────┤
│                                 │
│            主内容区             │
│                                 │
│                                 │
├─────────────────────────────────┤
│              页脚               │
└─────────────────────────────────┘

内容内边距: 16px
```

### 响应式断点

```css
/* 移动端 */
@media (max-width: 767px) { }

/* 平板端 */
@media (min-width: 768px) and (max-width: 1199px) { }

/* 桌面端 */
@media (min-width: 1200px) { }

/* 大屏幕 */
@media (min-width: 1440px) { }
```

## 组件设计规范

### 导航栏

#### 桌面端导航栏
```
┌─────────────────────────────────────────────────────────────┐
│ [Logo] 我的博客     [首页] [归档] [搜索] [主题切换] [GitHub] │
└─────────────────────────────────────────────────────────────┘

高度: 64px
背景: var(--background-primary)
边框: 底部 1px solid var(--border-color)
```

**设计要点:**
- Logo 放置在左侧，点击返回首页
- 导航菜单水平排列，间距均匀
- 右侧放置功能按钮和社交链接
- 支持粘性定位，滚动时保持可见

#### 移动端导航栏
```
┌─────────────────────────────────────┐
│ [☰] 我的博客           [🔍] [🌓]   │
└─────────────────────────────────────┘

高度: 56px
汉堡菜单: 左侧
功能按钮: 右侧
```

### 文章卡片

#### 文章列表项
```
┌─────────────────────────────────────────┐
│ 文章标题                               │
│ ─────────────────────────────────────   │
│ 文章摘要内容，显示前 150 字符...       │
│                                         │
│ 📅 2025-10-21  ⏱️ 5分钟阅读  🏷️ 标签1, 标签2 │
└─────────────────────────────────────────┘

内边距: 24px
圆角: 8px
背景: var(--background-secondary)
悬停: 轻微阴影 + 变换
```

**设计要点:**
- 标题使用较大字号，突出显示
- 摘要使用较小字号，颜色稍淡
- 元信息（日期、阅读时间、标签）使用图标
- 悬停效果要微妙，不影响阅读

### 文章详情页

#### 文章头部
```
┌─────────────────────────────────────────┐
│              文章标题                   │
│ ─────────────────────────────────────   │
│ 👤 作者名  📅 2025-10-21  ⏱️ 10分钟   │
│                                         │
│ 🏷️ 技术博客  🏷️ Hugo  🏷️ 教程         │
└─────────────────────────────────────────┘

最大宽度: 800px
居中对齐
标题下边距: 24px
```

#### 文章正文
```
段落间距: 1.5rem
行长: 45-75字符（最佳阅读体验）
图片: 最大宽度100%，居中显示
代码块: 带复制按钮，语法高亮
```

### 搜索界面

#### 搜索框
```
┌─────────────────────────────────────────┐
│ 🔍 搜索文章...                          │
└─────────────────────────────────────────┘

高度: 48px
圆角: 8px
内边距: 12px 16px
占位符颜色: var(--text-secondary)
```

#### 搜索结果
```
┌─────────────────────────────────────────┐
│ 搜索结果: 共 15 篇文章                 │
│ ─────────────────────────────────────   │
│ • Hugo 入门指南                        │
│   学习 Hugo 静态网站生成器...           │
│   📅 2025-10-20  🏷️ Hugo, 教程        │
│ ─────────────────────────────────────   │
│ • Obsidian 笔记管理技巧                │
│   高效使用 Obsidian 进行...             │
│   📅 2025-10-15  🏷️ 工具, 效率        │
└─────────────────────────────────────────┘
```

### 侧边栏组件

#### 个人信息卡片
```
┌─────────────────────────────────────────┐
│              👤 作者信息               │
│ ─────────────────────────────────────   │
│            [头像图片]                  │
│                                         │
│              作者名                    │
│            个人简介文字                │
│                                         │
│         [GitHub] [Twitter]             │
└─────────────────────────────────────────┘

头像: 120px x 120px
圆形
社交图标: 24px x 24px
```

#### 分类标签云
```
┌─────────────────────────────────────────┐
│              📁 分类标签                │
│ ─────────────────────────────────────   │
│    [Hugo] [技术] [教程] [生活]          │
│    [设计] [工具] [阅读] [思考]          │
│                                         │
│ 标签大小基于文章数量动态调整            │
└─────────────────────────────────────────┘
```

## 交互设计

### 按钮设计

#### 主要按钮
```css
.btn-primary {
  background: var(--primary-color);
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: var(--primary-color-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
```

#### 次要按钮
```css
.btn-secondary {
  background: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  padding: 10px 20px;
  border-radius: 6px;
}
```

### 链接设计

#### 内文链接
```css
a {
  color: var(--accent-color);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease;
}

a:hover {
  border-bottom-color: var(--accent-color);
}
```

### 表单设计

#### 输入框
```css
input[type="text"],
input[type="email"],
textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.2s ease;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

## 动效设计

### 页面转场

#### 淡入效果
```css
.page-enter {
  opacity: 0;
  transform: translateY(20px);
}

.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.3s ease;
}
```

### 微交互

#### 悬停效果
```css
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  transition: all 0.2s ease;
}
```

#### 加载动画
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading {
  animation: pulse 1.5s ease-in-out infinite;
}
```

## 可访问性设计

### 颜色对比度
- **正常文本**: 至少 4.5:1
- **大文本**: 至少 3:1
- **非文本元素**: 至少 3:1

### 焦点管理
```css
:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}
```

### 屏幕阅读器支持
- 语义化 HTML 标签
- ARIA 标签
- 图片 alt 文本
- 跳转到主内容链接

## 特殊状态设计

### 深色模式
```css
@media (prefers-color-scheme: dark) {
  :root {
    /* 深色模式变量 */
  }
}

/* 主题切换按钮动画 */
.theme-toggle {
  transition: transform 0.3s ease;
}

.theme-toggle:active {
  transform: rotate(180deg);
}
```

### 加载状态
```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--background-secondary) 25%,
    var(--border-color) 50%,
    var(--background-secondary) 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s ease-in-out infinite;
}
```

### 错误状态
```css
.error-message {
  color: var(--error-color);
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--error-color);
  border-radius: 6px;
  padding: 12px 16px;
}
```

## 设计交付物

### 设计文件要求
1. **设计稿格式**: Figma 或 Sketch
2. **设计系统**: 包含所有颜色、字体、间距定义
3. **组件库**: 所有 UI 组件的详细设计
4. **响应式设计**: 至少包含桌面端、平板端、移动端
5. **交互原型**: 关键交互流程的原型演示

### 图标资源
- 统一使用 [Feather Icons](https://feathericons.com/) 或 [Heroicons](https://heroicons.com/)
- 尺寸: 16px, 20px, 24px, 32px
- 格式: SVG (可缩放)
- 颜色: 支持当前主题色

### 图片规范
- **头像**: 400x400px，支持圆形裁剪
- **文章封面**: 1200x630px (16:9)，支持各种裁剪
- **插图**: 支持多种尺寸，保持清晰度
- **格式**: WebP (首选), PNG, JPEG
- **大小**: 单个图片不超过 500KB

## 设计审查清单

### 视觉设计
- [ ] 色彩系统完整且一致
- [ ] 字体层级清晰可读
- [ ] 间距系统合理应用
- [ ] 组件样式统一规范

### 响应式设计
- [ ] 移动端体验优化
- [ ] 平板端布局合理
- [ ] 桌面端充分利用空间
- [ ] 断点设置正确

### 交互设计
- [ ] 微交互自然流畅
- [ ] 加载状态明确反馈
- [ ] 错误处理友好清晰
- [ ] 导航直观易懂

### 可访问性
- [ ] 颜色对比度达标
- [ ] 键盘导航支持
- [ ] 屏幕阅读器友好
- [ ] 焦点管理清晰

### 性能考虑
- [ ] 图片优化合理
- [ ] 动画性能良好
- [ ] 字体加载策略
- [ ] 资源大小控制

---

**文档版本**: v1.0
**创建日期**: 2025-10-21
**设计系统**: Hugo 博客 UI Design System
**适配框架**: PaperMod Theme