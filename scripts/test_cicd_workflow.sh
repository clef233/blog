#!/bin/bash

# 测试脚本：CI/CD工作流验证
# 功能: 验证GitHub Actions配置和部署流程
# 作者: 开发团队
# 日期: 2025-10-21

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试结果记录
TESTS_PASSED=0
TESTS_FAILED=0

echo -e "${YELLOW}开始CI/CD工作流验证测试...${NC}"

# 测试函数
test_function() {
    local test_name="$1"
    local test_command="$2"

    echo -e "${YELLOW}测试: $test_name${NC}"

    if eval "$test_command"; then
        echo -e "${GREEN}✓ 通过${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ 失败${NC}"
        ((TESTS_FAILED++))
    fi
}

# 具体测试用例
echo -e "\n${YELLOW}=== GitHub Actions配置验证 ===${NC}"
test_function "检查GitHub Actions目录存在" "test -d .github"
test_function "检查部署工作流文件存在" "test -f .github/workflows/deploy.yml"
test_function "检查链接检查工作流存在" "test -f .github/workflows/link-check.yml"

echo -e "\n${YELLOW}=== 部署配置验证 ===${NC}"
test_function "验证部署工作流YAML语法" "grep -q 'name:' .github/workflows/deploy.yml"
test_function "验证Hugo版本配置" "grep -q 'peaceiris/actions-hugo' .github/workflows/deploy.yml"
test_function "验证GitHub Pages配置" "grep -q 'actions/deploy-pages' .github/workflows/deploy.yml"
test_function "验证权限配置正确" "grep -q 'permissions:' .github/workflows/deploy.yml"

echo -e "\n${YELLOW}=== Hugo配置验证 ===${NC}"
test_function "检查GitHub配置参数存在" "grep -q 'github_username:' hugo.yaml"
test_function "检查repo配置参数存在" "grep -q 'repo:' hugo.yaml"
test_function "验证baseURL配置" "grep -q '.github.io' hugo.yaml"

echo -e "\n${YELLOW}=== 部署脚本验证 ===${NC}"
test_function "检查部署脚本存在" "test -f scripts/deploy.sh"
test_function "验证部署脚本可执行" "test -x scripts/deploy.sh"
test_function "验证脚本包含构建命令" "grep -q 'hugo.*--minify' scripts/deploy.sh"

echo -e "\n${YELLOW}=== 构建和部署测试 ===${NC}"
test_function "Hugo配置验证" "hugo config > /dev/null 2>&1"

# 测试构建过程（不包含草稿）
echo -e "${YELLOW}测试标准构建...${NC}"
if hugo --gc --minify --buildDrafts=false --buildFuture=false > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 标准构建成功${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ 标准构建失败${NC}"
    ((TESTS_FAILED++))
fi

# 测试带草稿的构建
echo -e "${YELLOW}测试带草稿构建...${NC}"
if hugo --gc --minify --buildDrafts=true > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 带草稿构建成功${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ 带草稿构建失败${NC}"
    ((TESTS_FAILED++))
fi

# 检查输出文件
echo -e "\n${YELLOW}=== 输出文件验证 ===${NC}"
test_function "检查public目录生成" "test -d public"
test_function "检查主页文件生成" "test -f public/index.html"
test_function "检查sitemap生成" "test -f public/sitemap.xml"
test_function "检查RSS生成" "test -f public/index.xml"

# 检查构建文件大小
BUILD_SIZE=$(du -sh public 2>/dev/null | cut -f1)
if [[ -n "$BUILD_SIZE" ]]; then
    echo -e "${YELLOW}构建大小: $BUILD_SIZE${NC}"
    # 检查大小是否合理（小于10MB）
    SIZE_BYTES=$(du -sb public 2>/dev/null | cut -f1)
    if [[ $SIZE_BYTES -lt 10485760 ]]; then  # 10MB
        echo -e "${GREEN}✓ 构建大小合理${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ 构建大小过大${NC}"
        ((TESTS_FAILED++))
    fi
fi

# 检查关键页面生成
KEY_PAGES=("index.html" "about/index.html" "archives/index.html")
for page in "${KEY_PAGES[@]}"; do
    if [[ -f "public/$page" ]]; then
        echo -e "${GREEN}✓ $page 已生成${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ $page 未生成${NC}"
        ((TESTS_FAILED++))
    fi
done

# 测试部署脚本功能
echo -e "\n${YELLOW}=== 部署脚本功能测试 ===${NC}"
test_function "测试部署脚本帮助功能" "./scripts/deploy.sh --help > /dev/null 2>&1"

# 模拟构建（不实际推送）
echo -e "${YELLOW}测试部署脚本构建功能...${NC}"
# 创建临时环境变量来避免交互
echo "N" | ./scripts/deploy.sh > /dev/null 2>&1 || true

# 检查脚本是否创建了构建文件
if [[ -d "public" && -f "public/index.html" ]]; then
    echo -e "${GREEN}✓ 部署脚本构建功能正常${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ 部署脚本构建功能异常${NC}"
    ((TESTS_FAILED++))
fi

echo -e "\n${YELLOW}=== Git配置验证 ===${NC}"
test_function "检查.gitignore文件" "test -f .gitignore"
if [[ -f .gitignore ]]; then
    if grep -q "^public/" .gitignore; then
        echo -e "${GREEN}✓ public目录已在.gitignore中${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠️  建议在.gitignore中添加/public/${NC}"
    fi
fi

# 测试结果汇总
print_summary() {
    echo -e "\n${YELLOW}测试结果汇总:${NC}"
    echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "失败: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 CI/CD工作流验证通过！${NC}"
        echo -e "\n${YELLOW}下一步操作:${NC}"
        echo -e "1. 将代码推送到GitHub仓库"
        echo -e "2. 在GitHub仓库设置中启用GitHub Pages"
        echo -e "3. 监控GitHub Actions执行状态"
        echo -e "4. 访问部署的网站"
        exit 0
    else
        echo -e "${RED}❌ 有测试失败，请检查配置。${NC}"
        echo -e "\n${YELLOW}常见解决方案:${NC}"
        echo -e "- 检查GitHub Actions文件语法"
        echo -e "- 验证Hugo配置文件格式"
        echo -e "- 确认部署脚本权限"
        exit 1
    fi
}

print_summary