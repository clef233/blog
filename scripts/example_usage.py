#!/usr/bin/env python3
"""
Example usage of the Obsidian to Hugo synchronizer
"""

import sys
import os
from pathlib import Path

# Add current directory to path to import our module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from obsidian_sync import ObsidianHugoSynchronizer, SyncConfig


def main():
    """Example of how to use the Obsidian synchronizer."""

    # Configuration - UPDATE THESE PATHS
    config = SyncConfig(
        obsidian_vault_path="D:/iCloud/DATA/iCloudDrive/iCloud~md~obsidian/下水道/阅读笔记/扩展阅读",
        hugo_content_path="D:/Projects/blog/content",
        default_author="clef233",
        default_categories=["学术笔记", "阅读笔记"],
        default_tags=["同步", "Obsidian"],
        timezone="Asia/Shanghai",
        log_level="INFO"
    )

    print("Obsidian 到 Hugo 同步示例")
    print("=" * 50)
    print(f"Obsidian 路径: {config.obsidian_vault_path}")
    print(f"Hugo 内容路径: {config.hugo_content_path}")
    print(f"默认作者: {config.default_author}")
    print("=" * 50)

    # Check if paths exist
    obsidian_path = Path(config.obsidian_vault_path)
    hugo_path = Path(config.hugo_content_path)

    if not obsidian_path.exists():
        print(f"错误: Obsidian 路径不存在: {obsidian_path}")
        print("请修改配置文件中的路径设置")
        return

    if not hugo_path.exists():
        print(f"错误: Hugo 内容路径不存在: {hugo_path}")
        print("请修改配置文件中的路径设置")
        return

    # Create synchronizer
    synchronizer = ObsidianHugoSynchronizer(config)

    # Run synchronization
    try:
        stats = synchronizer.sync_vault()

        print("\n同步完成!")
        print(f"处理的文件: {stats['processed']}")
        print(f"跳过的文件: {stats['skipped']}")
        print(f"错误的文件: {stats['errors']}")

        if stats['processed'] > 0:
            print("\n同步成功! 你现在可以:")
            print("1. 检查生成的文件")
            print("2. 运行 Hugo 本地服务器: hugo server -D")
            print("3. 提交更改到 Git: git add . && git commit -m '同步 Obsidian 文章'")

    except Exception as e:
        print(f"同步失败: {e}")
        print("请检查日志文件 obsidian_sync.log 获取详细信息")


if __name__ == "__main__":
    main()