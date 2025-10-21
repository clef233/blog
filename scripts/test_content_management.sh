#!/bin/bash

# 测试脚本：内容管理系统验证
# 功能: 验证内容管理和Obsidian集成功能
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

echo -e "${YELLOW}开始内容管理系统验证测试...${NC}"

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
echo -e "\n${YELLOW}=== 文章模板验证 ===${NC}"
test_function "检查文章模板文件存在" "test -f archetypes/posts.md"
test_function "验证模板内容格式正确" "grep -q 'title:' archetypes/posts.md"
test_function "验证模板包含日期字段" "grep -q 'date:' archetypes/posts.md"
test_function "验证模板包含标签配置" "grep -q 'tags:' archetypes/posts.md"

echo -e "\n${YELLOW}=== 内容结构验证 ===${NC}"
test_function "检查关于页面存在" "test -f content/about/_index.md"
test_function "检查示例文章存在" "test -f content/posts/2025/getting-started-with-hugo.md"
test_function "检查文章目录结构" "test -d content/posts/2025"
test_function "验证文章front matter格式" "grep -q '^---.*---' content/posts/2025/getting-started-with-hugo.md"

echo -e "\n${YELLOW}=== 内容渲染验证 ===${NC}"
# 启动Hugo服务器进行测试
hugo server --port 1316 --bind 127.0.0.1 > /dev/null 2>&1 &
SERVER_PID=$!

# 等待服务器启动
sleep 5

test_function "Hugo服务器启动" "ps -p $SERVER_PID > /dev/null"
test_function "主页可访问" "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:1316/ | grep -q '200'"
test_function "文章页面可访问" "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:1316/posts/getting-started-with-hugo/ | grep -q '200'"
test_function "关于页面可访问" "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:1316/about/ | grep -q '200'"

# 清理服务器进程
kill $SERVER_PID 2>/dev/null || true

echo -e "\n${YELLOW}=== Hugo命令验证 ===${NC}"
test_function "测试hugo new命令" "hugo new posts/test-command.md --quiet"
test_function "验证新文件创建" "test -f content/posts/test-command.md"
test_function "清理测试文件" "rm content/posts/test-command.md"

echo -e "\n${YELLOW}=== Obsidian集成文档验证 ===${NC}"
test_function "检查Obsidian集成指南存在" "test -f docs/OBSIDIAN_INTEGRATION.md"
test_function "验证文档内容完整性" "grep -q 'Obsidian' docs/OBSIDIAN_INTEGRATION.md"
test_function "验证模板配置说明" "grep -q 'Templates' docs/OBSIDIAN_INTEGRATION.md"

# 测试结果汇总
print_summary() {
    echo -e "\n${YELLOW}测试结果汇总:${NC}"
    echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "失败: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 内容管理系统验证通过！${NC}"
        exit 0
    else
        echo -e "${RED}❌ 有测试失败，请检查配置。${NC}"
        exit 1
    fi
}

print_summary