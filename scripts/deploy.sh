#!/bin/bash

# Hugo 部署脚本
# 功能: 本地构建和部署到 GitHub Pages
# 作者: 开发团队
# 日期: 2025-10-21

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
BUILD_DIR="public"
DRAFTS=false
FUTURE=false

echo -e "${BLUE}🚀 Hugo 博客部署脚本${NC}"
echo -e "${YELLOW}===============================${NC}"

# 显示帮助信息
show_help() {
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -d, --drafts    包含草稿文章"
    echo "  -f, --future    包含未来日期的文章"
    echo "  -h, --help      显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0              # 标准部署"
    echo "  $0 --drafts     # 包含草稿部署"
    echo "  $0 --future     # 包含未来文章部署"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--drafts)
            DRAFTS=true
            shift
            ;;
        -f|--future)
            FUTURE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 检查 Hugo 是否安装
echo -e "${YELLOW}检查环境...${NC}"
if ! command -v hugo &> /dev/null; then
    echo -e "${RED}❌ Hugo 未安装，请先安装 Hugo${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Hugo 已安装: $(hugo version)${NC}"

# 检查 Git 状态
echo -e "${YELLOW}检查 Git 状态...${NC}"
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠️  检测到未提交的更改:${NC}"
    git status --short
    echo -e "${YELLOW}是否继续构建? (y/N): ${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ 部署已取消${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ 工作目录干净${NC}"
fi

# 构建 Hugo 网站
echo -e "${YELLOW}构建 Hugo 网站...${NC}"

# 清理之前的构建
if [[ -d "$BUILD_DIR" ]]; then
    echo -e "${YELLOW}清理之前的构建...${NC}"
    rm -rf "$BUILD_DIR"
fi

# 构建命令
BUILD_CMD="hugo --gc --minify"

if [[ "$DRAFTS" == "true" ]]; then
    BUILD_CMD="$BUILD_CMD --buildDrafts"
    echo -e "${YELLOW}✓ 包含草稿文章${NC}"
fi

if [[ "$FUTURE" == "true" ]]; then
    BUILD_CMD="$BUILD_CMD --buildFuture"
    echo -e "${YELLOW}✓ 包含未来文章${NC}"
fi

echo -e "${BLUE}执行构建命令: $BUILD_CMD${NC}"
eval "$BUILD_CMD"

# 检查构建结果
if [[ ! -d "$BUILD_DIR" ]]; then
    echo -e "${RED}❌ 构建失败：未找到 $BUILD_DIR 目录${NC}"
    exit 1
fi

# 显示构建统计
echo -e "${GREEN}✓ 构建完成！${NC}"
echo -e "${YELLOW}构建统计:${NC}"
echo -e "  📁 输出目录: $BUILD_DIR"
echo -e "  📊 文件数量: $(find "$BUILD_DIR" -type f | wc -l)"
echo -e "  📦 目录大小: $(du -sh "$BUILD_DIR" | cut -f1)"

# 检查关键文件
KEY_FILES=("index.html" "sitemap.xml")
for file in "${KEY_FILES[@]}"; do
    if [[ -f "$BUILD_DIR/$file" ]]; then
        echo -e "${GREEN}✓ $file 已生成${NC}"
    else
        echo -e "${RED}❌ $file 未生成${NC}"
    fi
done

# Git 相关操作
echo -e "${YELLOW}Git 操作...${NC}"

# 添加构建文件到 Git（如果它们还没有被忽略）
if git check-ignore "$BUILD_DIR" &> /dev/null; then
    echo -e "${YELLOW}⚠️  $BUILD_DIR 已被 .gitignore 忽略${NC}"
    echo -e "${YELLOW}⚠️  请使用 GitHub Actions 进行自动部署${NC}"
else
    echo -e "${YELLOW}检测到未忽略的构建文件，建议添加到 .gitignore${NC}"
    echo -e "${YELLOW}echo '/public/' >> .gitignore${NC}"
fi

# 显示部署信息
echo -e "${BLUE}📋 部署信息${NC}"
echo -e "${YELLOW}===============================${NC}"
echo -e "1. 推送代码到 GitHub:"
echo -e "   git add ."
echo -e "   git commit -m 'feat: 更新内容'"
echo -e "   git push origin main"
echo -e ""
echo -e "2. GitHub Actions 将自动构建和部署"
echo -e "   监控: https://github.com/username/blog/actions"
echo -e "   访问: https://username.github.io"
echo -e ""
echo -e "3. 本地预览:"
echo -e "   hugo server -D"

# 可选：自动推送到远程仓库
echo -e "${YELLOW}是否自动推送到远程仓库? (y/N): ${NC}"
read -r auto_push
if [[ "$auto_push" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}推送到远程仓库...${NC}"

    # 添加所有更改
    git add .

    # 提交
    echo -e "${YELLOW}输入提交信息: ${NC}"
    read -r commit_msg
    if [[ -z "$commit_msg" ]]; then
        commit_msg="feat: 更新博客内容"
    fi

    git commit -m "$commit_msg"

    # 推送
    git push origin main

    echo -e "${GREEN}✓ 已推送到远程仓库${NC}"
    echo -e "${BLUE}🌐 部署将在几分钟后完成，请访问: https://username.github.io${NC}"
else
    echo -e "${YELLOW}跳过自动推送${NC}"
fi

echo -e "${GREEN}🎉 部署脚本执行完成！${NC}"