#!/usr/bin/env python3
"""
博客管理 CLI 工具

使用方法:
    python blog_cli.py list              # 列出所有文章
    python blog_cli.py stats             # 显示统计
    python blog_cli.py new "文章标题"    # 创建新文章
    python blog_cli.py edit <path>       # 编辑文章
    python blog_cli.py delete <path>     # 删除文章
    python blog_cli.py preview           # 本地预览
    python blog_cli.py build             # 构建
    python blog_cli.py deploy            # 部署
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from cli.commands import cli

if __name__ == "__main__":
    cli()