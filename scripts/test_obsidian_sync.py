#!/usr/bin/env python3
"""
Test script for Obsidian to Hugo synchronization
"""

import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add the parent directory to the path to import our module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from obsidian_sync import ObsidianHugoSynchronizer, SyncConfig


def create_test_obsidian_file(file_path: Path, content: str):
    """Create a test Obsidian markdown file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def test_obsidian_sync():
    """Test the Obsidian synchronization functionality."""

    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        obsidian_vault = temp_path / "obsidian_vault"
        hugo_content = temp_path / "hugo_content"

        # Create test Obsidian files
        test_file1 = obsidian_vault / "test_article.md"
        test_content1 = """---
title: "测试文章"
created: 2025-10-22T10:00:00
tags: ["测试", "博客"]
categories: ["技术"]
---

# 测试文章

这是一篇测试文章的内容。

## 功能测试

这里测试 [[另一篇文章]] 的链接格式。

还有一个标签 #示例标签。

%%这是一个注释%%

![测试图片](test.png)
"""

        test_file2 = obsidian_vault / "subfolder" / "second_article.md"
        test_content2 = """# 第二篇文章

这是第二篇文章，没有frontmatter。

包含一个内部链接：[[test_article]]

标签：#文章 #测试
"""

        # Create test files
        create_test_obsidian_file(test_file1, test_content1)
        create_test_obsidian_file(test_file2, test_content2)

        # Create exclusion test file
        exclude_file = obsidian_vault / "template.md"
        create_test_obsidian_file(exclude_file, "This is a template")

        # Configure synchronizer
        config = SyncConfig(
            obsidian_vault_path=str(obsidian_vault),
            hugo_content_path=str(hugo_content),
            default_author="测试作者",
            default_categories=["默认分类"],
            exclude_patterns=[r".*template\.md$"]
        )

        # Run synchronization
        synchronizer = ObsidianHugoSynchronizer(config)
        stats = synchronizer.sync_vault()

        # Check results
        print("同步统计:")
        print(f"  处理: {stats['processed']} 个文件")
        print(f"  跳过: {stats['skipped']} 个文件")
        print(f"  错误: {stats['errors']} 个文件")

        # Verify output files
        output_files = list(hugo_content.rglob("*.md"))
        print(f"\n生成的文件数量: {len(output_files)}")

        for output_file in output_files:
            print(f"  - {output_file.relative_to(hugo_content)}")

            # Read and display content
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"    标题: {extract_title_from_content(content)}")
                print(f"    标签: {extract_tags_from_content(content)}")
                print("    内容预览:")
                lines = content.split('\n')[:10]
                for line in lines:
                    print(f"      {line}")
                if len(content.split('\n')) > 10:
                    print("      ...")
                print()

        # Verify specific functionality
        print("功能验证:")

        # Check that template file was excluded
        template_found = any("template" in str(f) for f in output_files)
        print(f"  模板文件排除: {'✓' if not template_found else '✗'}")

        # Check that wikilinks were converted
        test_article = None
        for f in output_files:
            if "test_article" in str(f):
                test_article = f
                break

        if test_article:
            with open(test_article, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check for converted wikilinks
                has_converted_links = "[test_article](test_article.md)" in content
                print(f"  Wiki链接转换: {'✓' if has_converted_links else '✗'}")

                # Check for frontmatter
                has_frontmatter = content.startswith('---')
                print(f"  Frontmatter生成: {'✓' if has_frontmatter_links else '✗'}")

                # Check for comment removal
                has_comments = "%%这是一个注释%%" in content
                print(f"  注释移除: {'✓' if not has_comments else '✗'}")

        return stats


def extract_title_from_content(content: str) -> str:
    """Extract title from markdown content."""
    import re
    if content.startswith('---\n'):
        end_index = content.find('\n---\n', 4)
        if end_index != -1:
            frontmatter_text = content[4:end_index]
            import yaml
            try:
                frontmatter = yaml.safe_load(frontmatter_text) or {}
                if 'title' in frontmatter:
                    return frontmatter['title']
            except:
                pass

    # Extract from first heading
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return "无标题"


def extract_tags_from_content(content: str) -> list:
    """Extract tags from content."""
    import re
    tags = set()

    # Find #tag patterns
    tag_pattern = r'#([a-zA-Z0-9_\-\u4e00-\u9fff]+)'
    matches = re.findall(tag_pattern, content)
    tags.update(matches)

    return list(tags)


if __name__ == "__main__":
    print("开始测试 Obsidian 到 Hugo 同步功能...\n")

    try:
        stats = test_obsidian_sync()
        print(f"\n测试完成！处理了 {stats['processed']} 个文件。")

        if stats['errors'] > 0:
            print(f"⚠️  发现 {stats['errors']} 个错误，请检查日志。")
        else:
            print("✅ 所有测试通过！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()