#!/bin/bash

# 简单的Hugo网站测试脚本
# 功能: 检测Hugo网站状态和基本功能

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
BASE_URL="http://127.0.0.1:1316"
TIMEOUT=5

echo -e "${BLUE}🔍 Hugo博客网站检测${NC}"
echo -e "${BLUE}================================${NC}"

# 检测函数
check_status() {
    local url="$1"
    local name="$2"
    local expected="$3"

    echo -e "${YELLOW}检查: $name${NC}"

    # 添加-v参数看详细curl信息
    local response=$(curl -s -w "%{http_code}\n" -m "$TIMEOUT" --silent "$url" 2>&1)
    local status_code=$(echo "$response" | grep -o "HTTP Status:" | cut -d' ' -f2)

    if [[ $status_code == "200" ]]; then
        echo -e "${GREEN}✅ $name - HTTP $status_code${NC}"
        if [[ -n "$expected" ]]; then
            if curl -s --max-time "$TIMEOUT" --silent "$url" 2>&1 | grep -q "$expected"; then
                echo -e "${GREEN}  ✓ 包含预期内容${NC}"
            else
                echo -e "${YELLOW} ⚠️ 缺少预期内容: $expected${NC}"
            fi
        else
            echo -e "${GREEN} ✅ 页面正常访问${NC}"
        fi
        return 0
    else
        echo -e "${RED}❌ $name - HTTP $status_code${NC}"
        return 1
    fi
}

# 检测结果
FAILED=0
PASSED=0

echo -e "${BLUE}1. 📄 首页状态${NC}"
check_status "首页" "/"
PASSED=$((PASSED + (check_status "首页" "/")))

echo -e "\n${BLUE}2. 🔍 搜索功能${NC}"
check_status "搜索页面" "/search/"
PASSED=$((PASSED + (check_status "搜索页面" "/search/")))

echo -e "\n${BLUE}3. 📝 文章页面${NC}"
check_status "文章页面" "/posts/2025/getting-started-with-hugo/"
PASSED=$((PASSED + (check_status "文章页面" "/posts/2025/getting-started-with-hugo/")))

echo -e "\n${BLUE}4. 📊 静态资源${NC}"

# 检查CSS
echo -e "  检查CSS资源..."
CSS_RESOURCES_OK=true

css_files=("assets/css/stylesheet.css" "assets/css/")
for css in "${css_files[@]}"; do
    check_status "CSS ($css)" "$BASE_URL$css"
    if [[ $? -ne 0 ]]; then
        CSS_RESOURCES_OK=false
    fi
done

# 检查图标
echo -e "  检查图标文件..."
ICONS_OK=true
icon_files=("favicon.ico" "favicon-16x16.png" "favicon-32x32.png" "apple-touch-icon.png")
for icon in "${icon_files[@]}"; do
    check_status "图标 ($icon)" "$BASE_URL$icon"
    if [[ $? -ne 0 ]]; then
        ICONS_OK=false
    fi
done

# 检查PWA文件
echo -e "  检查PWA文件..."
check_status "Web App Manifest" "/site.webmanifest"
PWA_OK=$?

if [[ $CSS_RESOURCES_OK && $ICONS_OK && $PWA_OK -eq 0 ]]; then
    echo -e "${GREEN}✅ 静态资源检查通过${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ 部分静态资源检查失败${NC}"
    FAILED=$((FAILED + 1))
fi

# 性能测试
echo -e "\n${BLUE}5. ⚡ 性能测试${NC}"

# 检查响应时间
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}\n" "$BASE_URL/" 2>&1 | tail -1)
TIME_VALUE=$(echo "$RESPONSE_TIME" | cut -d' -f1)

if (( $(echo "$TIME_VALUE" | cut -d' -f1) -lt 3000 )); then
    echo -e "${GREEN}✅ 响应时间优秀: ${TIME_VALUE}ms (< 3s)${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${YELLOW}⚠️  响应时间较慢: ${TIME_VALUE}ms (> 3s)${NC}"
fi

# 检查页面大小
PAGE_SIZE=$(curl -s -o /dev/null -w "Content-Length: %{size_download}\n" "$BASE_URL/" 2>&1 | tail -1)
echo -e "  首页大小: ${PAGE_SIZE}字节${NC}"

if [[ $PAGE_SIZE -lt 524288 ]]; then
    echo -e "${GREEN}✅ 页面大小合理 (< 512KB)${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${YELLOW}⚠️ 页面大小较大 (≥ 512KB)${NC}"
fi

# 检查HTML压缩
if curl -s "$BASE_URL/" 2>&1 | grep -q "compress" > /dev/null; then
    echo -e "${GREEN}✅ HTML已压缩${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${YELLOW}⚠️ HTML未压缩${NC}"
fi

# 结果汇总
echo -e "\n${BLUE}6. 📊 测试结果汇总${NC}"
echo -e "${YELLOW}================================${NC}"

echo -e "${GREEN}✅ 通过测试: $PASSED${NC}"
echo -e "${RED}❌ 失败测试: $FAILED${NC}"
echo -e "${BLUE}成功率: $((PASSED * 100 / (PASSED + FAILED)))%${NC}"

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}🎉 恭喜！Hugo博客系统检测通过！${NC}"
    echo -e "\n${BLUE}🌐 网站运行正常，功能完整${NC}"
    echo -e "\n${BLUE}📍 访问地址: $BASE_URL${NC}"
else
    echo -e "${RED}❌ 有功能需要修复，请检查上述失败项目${NC}"
fi

echo -e "\n${YELLOW}💡 建议:${NC}"
echo -e "1. 检查Hugo服务器是否正常运行"
echo -e "2. 确认端口1316未被其他程序占用"
echo -e "3. 在浏览器中测试各项功能"
echo -e "4. 检查控制台错误日志"

echo -e "\n${BLUE}================================${NC}"