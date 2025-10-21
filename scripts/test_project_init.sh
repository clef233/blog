#!/bin/bash

# 测试脚本：项目初始化验证
# 功能: 验证Hugo项目初始化是否成功
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

echo -e "${YELLOW}开始Hugo项目初始化验证测试...${NC}"

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
echo -e "\n${YELLOW}=== 目录结构验证 ===${NC}"
test_function "检查Hugo配置文件存在" "test -f hugo.yaml"
test_function "检查content目录存在" "test -d content"
test_function "检查static目录存在" "test -d static"
test_function "检查themes目录存在" "test -d themes"
test_function "检查layouts目录存在" "test -d layouts"
test_function "检查archetypes目录存在" "test -d archetypes"

echo -e "\n${YELLOW}=== 配置文件验证 ===${NC}"
test_function "验证YAML配置语法" "hugo config > /dev/null 2>&1"
test_function "检查主页文件存在" "test -f content/_index.md"
test_function "检查posts目录结构" "test -d content/posts"

echo -e "\n${YELLOW}=== Hugo服务器启动测试 ===${NC}"
# 启动Hugo服务器并在后台运行
hugo server --port 1314 --bind 127.0.0.1 > /dev/null 2>&1 &
SERVER_PID=$!

# 等待服务器启动
sleep 3

test_function "Hugo服务器是否启动" "ps -p $SERVER_PID > /dev/null"

# 清理服务器进程
kill $SERVER_PID 2>/dev/null || true

# 测试结果汇总
print_summary() {
    echo -e "\n${YELLOW}测试结果汇总:${NC}"
    echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "失败: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 项目初始化验证通过！${NC}"
        exit 0
    else
        echo -e "${RED}❌ 有测试失败，请检查配置。${NC}"
        exit 1
    fi
}

print_summary