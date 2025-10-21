#!/bin/bash

# 测试脚本：主题安装验证
# 功能: 验证PaperMod主题安装和配置
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

echo -e "${YELLOW}开始主题安装验证测试...${NC}"

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
echo -e "\n${YELLOW}=== 主题文件验证 ===${NC}"
test_function "检查主题目录存在" "test -d themes/PaperMod"
test_function "检查主题配置文件存在" "test -f themes/PaperMod/theme.toml"
test_function "检查主题布局文件存在" "test -d themes/PaperMod/layouts"
test_function "检查主题静态资源存在" "test -d themes/PaperMod/assets"

echo -e "\n${YELLOW}=== 配置文件验证 ===${NC}"
test_function "验证主题配置在hugo.yaml中" "grep -q 'theme: PaperMod' hugo.yaml"
test_function "检查自定义CSS文件存在" "test -f assets/css/extended/custom.css"
test_function "检查搜索页面存在" "test -f content/search/_index.md"
test_function "检查归档页面存在" "test -f content/archives/_index.md"

echo -e "\n${YELLOW}=== Hugo服务器测试 ===${NC}"
# 启动Hugo服务器并在后台运行
hugo server --port 1315 --bind 127.0.0.1 > /dev/null 2>&1 &
SERVER_PID=$!

# 等待服务器启动
sleep 5

test_function "Hugo服务器启动测试" "ps -p $SERVER_PID > /dev/null"

# 测试主页是否可访问（使用curl检查）
test_function "主页可访问性测试" "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:1315/ | grep -q '200'"

# 清理服务器进程
kill $SERVER_PID 2>/dev/null || true

# 测试结果汇总
print_summary() {
    echo -e "\n${YELLOW}测试结果汇总:${NC}"
    echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "失败: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 主题安装验证通过！${NC}"
        exit 0
    else
        echo -e "${RED}❌ 有测试失败，请检查配置。${NC}"
        exit 1
    fi
}

print_summary