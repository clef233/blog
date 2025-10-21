#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客文章同步和格式化脚本
功能：
1. 格式化现有的博客文章文件
2. 从Obsidian文件夹同步新的阅读笔记
3. 自动生成Hugo Front Matter
"""

import os
import sys
import argparse
import shutil
import re
from datetime import datetime
from pathlib import Path

class BlogSync:
    def __init__(self):
        # 配置路径
        self.blog_dir = Path(r"D:\Projects\blog")
        self.posts_dir = self.blog_dir / "content" / "posts" / "2025"
        self.obsidian_dir = Path(r"D:\iCloud\DATA\iCloudDrive\iCloud~md~obsidian\下水道\阅读笔记\扩展阅读")

        # 确保目录存在
        self.posts_dir.mkdir(parents=True, exist_ok=True)

        # 默认配置
        self.default_tags = ["学术笔记", "阅读笔记", "同步"]
        self.default_categories = ["学术笔记"]
        self.author = "clef233"

    def has_front_matter(self, file_path):
        """检查文件是否已有Front Matter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return content.startswith('---')
        except:
            return False

    def extract_title_from_content(self, content):
        """从内容中提取标题"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
            elif line.startswith('**') and line.endswith('**'):
                return line[2:-2].strip()
            elif line and not line.startswith('#') and not line.startswith('---'):
                # 如果第一行不是标题格式，就作为标题
                return line
        return "未命名文章"

    def extract_description(self, content, max_length=200):
        """从内容开头提取描述"""
        lines = content.split('\n')
        description_parts = []

        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('---') and not line.startswith('*'):
                if len(line) > 10:  # 过滤太短的行
                    description_parts.append(line)
                    if len(' '.join(description_parts)) > max_length:
                        break

        description = ' '.join(description_parts)
        return description[:max_length] + ('...' if len(description) > max_length else '')

    def generate_front_matter(self, file_path, content):
        """生成Front Matter"""
        file_name = file_path.stem
        title = self.extract_title_from_content(content)
        description = self.extract_description(content)

        # 尝试从文件名或内容中提取更具体的标签
        tags = self.default_tags.copy()
        categories = self.default_categories.copy()

        # 根据内容添加特定标签
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in ['政治', '国家', '民主', '权力']):
            tags.append("政治学")
        elif any(keyword in content_lower for keyword in ['社会', '文化', '结构', '制度']):
            tags.append("社会学")
        elif any(keyword in content_lower for keyword in ['哲学', '思想', '认识', '真理']):
            tags.append("哲学")
        elif any(keyword in content_lower for keyword in ['经济', '资本', '市场', '发展']):
            tags.append("经济学")

        front_matter = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
draft: false
description: "{description}"
tags: {tags}
categories: {categories}
author: "{self.author}"
showToc: true
TocOpen: false
---

"""
        return front_matter

    def format_existing_files(self, dry_run=False):
        """格式化现有文件"""
        print(f"[INFO] 正在扫描目录: {self.posts_dir}")

        md_files = list(self.posts_dir.glob("*.md"))
        if not md_files:
            print("[ERROR] 没有找到Markdown文件")
            return

        print(f"[INFO] 找到 {len(md_files)} 个Markdown文件")

        formatted_count = 0
        for file_path in md_files:
            print(f"\n[FILE] 处理文件: {file_path.name}")

            if self.has_front_matter(file_path):
                print(f"   [OK] 已有Front Matter，跳过")
                continue

            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
            except Exception as e:
                print(f"   [ERROR] 读取文件失败: {e}")
                continue

            # 生成新的内容
            front_matter = self.generate_front_matter(file_path, original_content)
            new_content = front_matter + original_content

            if dry_run:
                print(f"   [PREVIEW] 将添加Front Matter:")
                print(f"   标题: {self.extract_title_from_content(original_content)}")
                print(f"   描述: {self.extract_description(original_content)}")
            else:
                # 写入文件
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"   [SUCCESS] 格式化完成")
                    formatted_count += 1
                except Exception as e:
                    print(f"   [ERROR] 写入文件失败: {e}")

        if dry_run:
            print(f"\n[PREVIEW] 预览模式完成，共检查 {len(md_files)} 个文件")
        else:
            print(f"\n[SUCCESS] 格式化完成，共处理 {formatted_count} 个文件")

    def sync_from_obsidian(self, dry_run=False):
        """从Obsidian同步文件"""
        print(f"[INFO] 正在扫描Obsidian目录: {self.obsidian_dir}")

        if not self.obsidian_dir.exists():
            print(f"[ERROR] Obsidian目录不存在: {self.obsidian_dir}")
            return

        obsidian_files = list(self.obsidian_dir.glob("*.md"))
        if not obsidian_files:
            print("[ERROR] Obsidian目录中没有找到Markdown文件")
            return

        print(f"[INFO] 找到 {len(obsidian_files)} 个Obsidian文件")

        synced_count = 0
        for obsidian_file in obsidian_files:
            print(f"\n[FILE] 处理文件: {obsidian_file.name}")

            # 检查目标文件是否已存在
            target_file = self.posts_dir / obsidian_file.name
            if target_file.exists():
                print(f"   [SKIP] 目标文件已存在，跳过")
                continue

            if dry_run:
                print(f"   [PREVIEW] 将复制到: {target_file}")
                print(f"   然后进行格式化")
            else:
                try:
                    # 复制文件
                    shutil.copy2(obsidian_file, target_file)
                    print(f"   [COPY] 文件已复制")

                    # 读取并格式化
                    with open(target_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    front_matter = self.generate_front_matter(target_file, content)
                    new_content = front_matter + content

                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"   [SUCCESS] 同步并格式化完成")
                    synced_count += 1

                except Exception as e:
                    print(f"   [ERROR] 处理失败: {e}")

        if dry_run:
            print(f"\n[PREVIEW] 预览模式完成，共检查 {len(obsidian_files)} 个文件")
        else:
            print(f"\n[SUCCESS] 同步完成，共处理 {synced_count} 个文件")

    def run_all(self, dry_run=False):
        """执行完整流程"""
        print("[INFO] 开始执行完整同步流程")
        print("=" * 50)

        self.format_existing_files(dry_run)
        print("\n" + "=" * 50)
        self.sync_from_obsidian(dry_run)

        if not dry_run:
            print("\n" + "=" * 50)
            print("[SUCCESS] 完整流程执行完成！")
            print("[TIP] 运行 'git add . && git commit -m \"同步文章\" && git push' 来提交更改")

def main():
    parser = argparse.ArgumentParser(description='博客文章同步和格式化工具')
    parser.add_argument('--format', action='store_true', help='格式化现有文件')
    parser.add_argument('--sync', action='store_true', help='从Obsidian同步新文件')
    parser.add_argument('--all', action='store_true', help='执行完整流程')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际修改文件')

    args = parser.parse_args()

    if not any([args.format, args.sync, args.all]):
        parser.print_help()
        return

    sync = BlogSync()

    if args.dry_run:
        print("[PREVIEW] 预览模式 - 不会实际修改文件")
        print("=" * 50)

    if args.format:
        sync.format_existing_files(args.dry_run)

    if args.sync:
        sync.sync_from_obsidian(args.dry_run)

    if args.all:
        sync.run_all(args.dry_run)

if __name__ == "__main__":
    main()