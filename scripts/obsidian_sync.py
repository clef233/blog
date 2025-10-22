#!/usr/bin/env python3
"""
Obsidian to Hugo Synchronizer

This script automatically synchronizes markdown files from an Obsidian vault
to a Hugo blog, converting metadata and formatting as needed.

Author: Claude AI Assistant
Date: 2025-10-22
"""

import os
import re
import shutil
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging
from dataclasses import dataclass
from zoneinfo import ZoneInfo


@dataclass
class SyncConfig:
    """Configuration class for the synchronization process."""
    obsidian_vault_path: str
    hugo_content_path: str
    default_author: str = "clef233"
    default_categories: List[str] = None
    default_tags: List[str] = None
    timezone: str = "Asia/Shanghai"
    log_level: str = "INFO"
    exclude_patterns: List[str] = None

    def __post_init__(self):
        if self.default_categories is None:
            self.default_categories = ["博客文章"]
        if self.default_tags is None:
            self.default_tags = []
        if self.exclude_patterns is None:
            self.exclude_patterns = [
                r'.*\.excalidraw$',
                r'.*\.canvas$',
                r'.*\.sticker$',
                r'.*/_templates/.*',
                r'.*/\.obsidian/.*',
                r'.*/\.trash/.*'
            ]


class ObsidianParser:
    """Parser for Obsidian markdown files."""

    def __init__(self, config: SyncConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def extract_frontmatter(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter from markdown content."""
        if not content.startswith('---\n'):
            return {}, content

        try:
            end_index = content.find('\n---\n', 4)
            if end_index == -1:
                return {}, content

            frontmatter_text = content[4:end_index]
            frontmatter = yaml.safe_load(frontmatter_text) or {}
            body_content = content[end_index + 5:]

            return frontmatter, body_content
        except Exception as e:
            self.logger.warning(f"Failed to parse frontmatter: {e}")
            return {}, content

    def extract_title_from_content(self, content: str) -> Optional[str]:
        """Extract title from the first heading in content."""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        return None

    def extract_tags_from_content(self, content: str) -> List[str]:
        """Extract tags from content using Obsidian tag format."""
        tags = set()

        # Find #tag patterns
        tag_pattern = r'#([a-zA-Z0-9_\-\u4e00-\u9fff]+)'
        matches = re.findall(tag_pattern, content)
        tags.update(matches)

        # Find tags from frontmatter
        frontmatter, _ = self.extract_frontmatter(content)
        if 'tags' in frontmatter:
            if isinstance(frontmatter['tags'], list):
                tags.update(frontmatter['tags'])
            elif isinstance(frontmatter['tags'], str):
                tags.add(frontmatter['tags'])

        return list(tags)

    def convert_wikilinks_to_markdown(self, content: str) -> str:
        """Convert Obsidian wikilinks to standard markdown links."""
        # Convert [[filename]] to [filename](filename.md)
        content = re.sub(
            r'\[\[([^\]|]+)(\|([^\]]+))?\]\]',
            lambda m: f"[{m.group(3) or m.group(1)}]({m.group(1)}.md)",
            content
        )
        return content

    def convert_obsidian_links(self, content: str) -> str:
        """Convert various Obsidian link formats to standard markdown."""
        # Convert wikilinks
        content = self.convert_wikilinks_to_markdown(content)

        # Convert ![[image.png]] to ![image.png](image.png)
        content = re.sub(
            r'!\[\[([^\]|]+)(\|([^\]]+))?\]\]',
            lambda m: f"![{m.group(3) or m.group(1)}]({m.group(1)})",
            content
        )

        return content

    def remove_obsidian_comments(self, content: str) -> str:
        """Remove Obsidian-style comments."""
        # Remove inline comments %%comment%%
        content = re.sub(r'%%[^%]*%%', '', content)

        # Remove block comments %% ... %%
        content = re.sub(r'%%.*?%%', '', content, flags=re.DOTALL)

        return content


class HugoFrontmatterGenerator:
    """Generate Hugo-compatible frontmatter."""

    def __init__(self, config: SyncConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def generate_frontmatter(self,
                           title: str,
                           file_path: Path,
                           obsidian_frontmatter: Dict[str, Any],
                           content: str) -> Dict[str, Any]:
        """Generate Hugo frontmatter from Obsidian data."""
        hugo_frontmatter = {}

        # Basic required fields
        hugo_frontmatter['title'] = title
        hugo_frontmatter['date'] = self._get_date_from_file(file_path, obsidian_frontmatter)
        hugo_frontmatter['draft'] = False
        hugo_frontmatter['author'] = self.config.default_author

        # Extract description from content or obsidian metadata
        description = self._extract_description(content, obsidian_frontmatter)
        if description:
            hugo_frontmatter['description'] = description
            hugo_frontmatter['summary'] = description

        # Handle categories
        categories = self._process_categories(obsidian_frontmatter)
        if categories:
            hugo_frontmatter['categories'] = categories

        # Handle tags
        tags = self._process_tags(content, obsidian_frontmatter)
        if tags:
            hugo_frontmatter['tags'] = tags

        # Copy additional metadata
        for key, value in obsidian_frontmatter.items():
            if key not in ['date', 'title', 'author', 'tags', 'categories', 'description']:
                hugo_frontmatter[key] = value

        # Add Hugo-specific settings
        hugo_frontmatter['showToc'] = True
        hugo_frontmatter['TocOpen'] = False

        return hugo_frontmatter

    def _get_date_from_file(self, file_path: Path, obsidian_frontmatter: Dict[str, Any]) -> str:
        """Get date from file metadata or frontmatter."""
        # Try to get date from Obsidian frontmatter
        if 'date' in obsidian_frontmatter:
            return obsidian_frontmatter['date']

        if 'created' in obsidian_frontmatter:
            return obsidian_frontmatter['created']

        # Use file modification time
        file_stat = file_path.stat()
        dt = datetime.fromtimestamp(file_stat.st_mtime, tz=ZoneInfo(self.config.timezone))
        return dt.strftime('%Y-%m-%dT%H:%M:%S%z')

    def _extract_description(self, content: str, obsidian_frontmatter: Dict[str, Any]) -> Optional[str]:
        """Extract description from content or frontmatter."""
        # Check frontmatter first
        if 'description' in obsidian_frontmatter:
            return obsidian_frontmatter['description']

        if 'summary' in obsidian_frontmatter:
            return obsidian_frontmatter['summary']

        # Extract first paragraph from content
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('!'):
                # Truncate if too long
                if len(line) > 200:
                    return line[:197] + '...'
                return line

        return None

    def _process_categories(self, obsidian_frontmatter: Dict[str, Any]) -> List[str]:
        """Process categories from Obsidian metadata."""
        if 'categories' in obsidian_frontmatter:
            categories = obsidian_frontmatter['categories']
            if isinstance(categories, list):
                return categories
            elif isinstance(categories, str):
                return [categories]

        # Use default categories
        return self.config.default_categories.copy()

    def _process_tags(self, content: str, obsidian_frontmatter: Dict[str, Any]) -> List[str]:
        """Process tags from content and frontmatter."""
        parser = ObsidianParser(self.config)
        content_tags = parser.extract_tags_from_content(content)

        frontmatter_tags = []
        if 'tags' in obsidian_frontmatter:
            tags = obsidian_frontmatter['tags']
            if isinstance(tags, list):
                frontmatter_tags = tags
            elif isinstance(tags, str):
                frontmatter_tags = [tags]

        # Combine and deduplicate
        all_tags = list(set(content_tags + frontmatter_tags + self.config.default_tags))
        return all_tags


class ObsidianHugoSynchronizer:
    """Main synchronizer class."""

    def __init__(self, config: SyncConfig):
        self.config = config
        self.setup_logging()
        self.parser = ObsidianParser(config)
        self.frontmatter_generator = HugoFrontmatterGenerator(config)
        self.logger = logging.getLogger(__name__)

    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('obsidian_sync.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded based on patterns."""
        relative_path = file_path.relative_to(self.config.obsidian_vault_path)

        for pattern in self.config.exclude_patterns:
            if re.match(pattern, str(relative_path)):
                return True
        return False

    def get_hugo_file_path(self, obsidian_file: Path) -> Path:
        """Generate Hugo file path from Obsidian file path."""
        # Use year-based organization
        file_stat = obsidian_file.stat()
        year = datetime.fromtimestamp(file_stat.st_mtime).year

        # Generate filename
        filename = obsidian_file.stem
        # Sanitize filename
        filename = re.sub(r'[^\w\s\-\.]', '', filename).strip()
        filename = re.sub(r'[-\s]+', '-', filename)

        hugo_path = Path(self.config.hugo_content_path) / "posts" / str(year) / f"{filename}.md"
        return hugo_path

    def process_markdown_file(self, obsidian_file: Path) -> bool:
        """Process a single markdown file."""
        try:
            self.logger.info(f"Processing file: {obsidian_file}")

            # Read original content
            with open(obsidian_file, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Parse Obsidian content
            obsidian_frontmatter, body_content = self.parser.extract_frontmatter(original_content)

            # Extract title
            title = obsidian_frontmatter.get('title')
            if not title:
                title = self.parser.extract_title_from_content(body_content)
            if not title:
                title = obsidian_file.stem

            # Process content
            processed_content = self.parser.convert_obsidian_links(body_content)
            processed_content = self.parser.remove_obsidian_comments(processed_content)

            # Generate Hugo frontmatter
            hugo_frontmatter = self.frontmatter_generator.generate_frontmatter(
                title, obsidian_file, obsidian_frontmatter, processed_content
            )

            # Generate final content
            final_content = self._generate_final_content(hugo_frontmatter, processed_content)

            # Write to Hugo destination
            hugo_file = self.get_hugo_file_path(obsidian_file)
            hugo_file.parent.mkdir(parents=True, exist_ok=True)

            with open(hugo_file, 'w', encoding='utf-8') as f:
                f.write(final_content)

            self.logger.info(f"Successfully synced to: {hugo_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to process {obsidian_file}: {e}")
            return False

    def _generate_final_content(self, frontmatter: Dict[str, Any], content: str) -> str:
        """Generate final markdown content with YAML frontmatter."""
        frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False,
                                   allow_unicode=True, sort_keys=False)
        return f"---\n{frontmatter_yaml}---\n\n{content}"

    def copy_attachments(self, obsidian_file: Path):
        """Copy attachment files (images, etc.) to Hugo static directory."""
        # This is a placeholder for future implementation
        # Could copy images to static/ or assets/ directory
        pass

    def sync_vault(self) -> Dict[str, int]:
        """Sync the entire Obsidian vault to Hugo."""
        self.logger.info("Starting Obsidian to Hugo synchronization")

        stats = {
            'processed': 0,
            'skipped': 0,
            'errors': 0
        }

        obsidian_path = Path(self.config.obsidian_vault_path)
        if not obsidian_path.exists():
            self.logger.error(f"Obsidian vault path does not exist: {obsidian_path}")
            return stats

        # Find all markdown files
        markdown_files = list(obsidian_path.rglob("*.md"))

        for file_path in markdown_files:
            if self.should_exclude_file(file_path):
                self.logger.debug(f"Excluding file: {file_path}")
                stats['skipped'] += 1
                continue

            if self.process_markdown_file(file_path):
                stats['processed'] += 1
            else:
                stats['errors'] += 1

        self.logger.info(f"Sync completed. Processed: {stats['processed']}, "
                        f"Skipped: {stats['skipped']}, Errors: {stats['errors']}")
        return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Sync Obsidian vault to Hugo blog')
    parser.add_argument('--obsidian-vault', required=True,
                       help='Path to Obsidian vault directory')
    parser.add_argument('--hugo-content', required=True,
                       help='Path to Hugo content directory')
    parser.add_argument('--author', default='clef233',
                       help='Default author name')
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be synced without actually doing it')

    args = parser.parse_args()

    # Create configuration
    config = SyncConfig(
        obsidian_vault_path=args.obsidian_vault,
        hugo_content_path=args.hugo_content,
        default_author=args.author,
        log_level=args.log_level
    )

    # Create synchronizer
    synchronizer = ObsidianHugoSynchronizer(config)

    if args.dry_run:
        print("Dry run mode - showing what would be processed:")
        # Add dry run logic here if needed
        return

    # Run synchronization
    stats = synchronizer.sync_vault()

    print(f"\nSynchronization completed:")
    print(f"  Processed: {stats['processed']} files")
    print(f"  Skipped: {stats['skipped']} files")
    print(f"  Errors: {stats['errors']} files")


if __name__ == "__main__":
    main()