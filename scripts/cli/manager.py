"""
博客管理 CLI 工具
"""

import os
import re
import yaml
import subprocess
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Article:
    """文章数据类"""
    path: Path
    title: str = ""
    date: Optional[datetime] = None
    draft: bool = False
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    description: str = ""
    word_count: int = 0


class BlogManager:
    """博客管理器"""

    def __init__(self, blog_root: str = None):
        if blog_root:
            self.root = Path(blog_root)
        else:
            # 自动检测项目根目录
            self.root = self._find_blog_root()

        self.content_dir = self.root / "content"
        self.posts_dir = self.content_dir / "posts"

    def _find_blog_root(self) -> Path:
        """查找博客根目录"""
        current = Path.cwd()
        while current != current.parent:
            if (current / "hugo.yaml").exists() or (current / "config.yaml").exists():
                return current
            current = current.parent
        return Path.cwd()

    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """解析 YAML front matter"""
        if not content.startswith("---\n"):
            return {}, content

        try:
            end = content.find("\n---\n", 4)
            if end == -1:
                return {}, content

            fm_text = content[4:end]
            body = content[end + 5:]
            fm = yaml.safe_load(fm_text) or {}
            return fm, body
        except Exception:
            return {}, content

    def _format_frontmatter(self, fm: Dict[str, Any]) -> str:
        """格式化 front matter"""
        return yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def list_articles(self, tag: str = None, category: str = None, draft: bool = None) -> List[Article]:
        """列出所有文章"""
        articles = []

        if not self.posts_dir.exists():
            return articles

        for md_file in self.posts_dir.rglob("*.md"):
            article = self._load_article(md_file)
            if article:
                # 过滤
                if tag and tag not in article.tags:
                    continue
                if category and category not in article.categories:
                    continue
                if draft is not None and article.draft != draft:
                    continue
                articles.append(article)

        # 按日期排序 - 处理时区问题
        def get_sort_key(a: Article):
            if a.date is None:
                return datetime.min
            # 如果有时区信息，转换为 UTC 并去除时区
            if a.date.tzinfo is not None:
                from datetime import timezone
                return a.date.astimezone(timezone.utc).replace(tzinfo=None)
            return a.date

        articles.sort(key=get_sort_key, reverse=True)
        return articles

    def _load_article(self, path: Path) -> Optional[Article]:
        """加载文章"""
        try:
            content = path.read_text(encoding="utf-8")
            fm, body = self._parse_frontmatter(content)

            # 解析日期
            date = None
            if fm.get("date"):
                if isinstance(fm["date"], datetime):
                    date = fm["date"]
                elif isinstance(fm["date"], str):
                    for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                        try:
                            date = datetime.strptime(fm["date"][:19], fmt)
                            break
                        except ValueError:
                            continue

            return Article(
                path=path,
                title=fm.get("title", path.stem),
                date=date,
                draft=fm.get("draft", False),
                tags=fm.get("tags", []),
                categories=fm.get("categories", []),
                description=fm.get("description", ""),
                word_count=len(body.replace("\n", "").replace(" ", ""))
            )
        except Exception as e:
            print(f"加载文章失败: {path} - {e}")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        articles = self.list_articles()

        # 标签统计
        tag_counts: Dict[str, int] = {}
        for article in articles:
            for tag in article.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 分类统计
        category_counts: Dict[str, int] = {}
        for article in articles:
            for cat in article.categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1

        # 时间分布
        year_counts: Dict[int, int] = {}
        for article in articles:
            if article.date:
                year = article.date.year
                year_counts[year] = year_counts.get(year, 0) + 1

        return {
            "total": len(articles),
            "published": len([a for a in articles if not a.draft]),
            "drafts": len([a for a in articles if a.draft]),
            "total_words": sum(a.word_count for a in articles),
            "tags": dict(sorted(tag_counts.items(), key=lambda x: -x[1])),
            "categories": dict(sorted(category_counts.items(), key=lambda x: -x[1])),
            "years": dict(sorted(year_counts.items(), reverse=True))
        }

    def create_article(self, title: str, categories: List[str] = None, tags: List[str] = None) -> Path:
        """创建新文章"""
        now = datetime.now()
        year = now.year

        # 生成文件名
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[\s]+', '-', slug)

        # 确保目录存在
        year_dir = self.posts_dir / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)

        # 生成路径
        file_path = year_dir / f"{slug}.md"
        counter = 1
        while file_path.exists():
            file_path = year_dir / f"{slug}-{counter}.md"
            counter += 1

        # 生成 front matter
        fm = {
            "title": title,
            "date": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "draft": True,
            "tags": tags or [],
            "categories": categories or ["未分类"],
            "author": "clef233",
            "description": "",
            "keywords": []
        }

        content = f"---\n{self._format_frontmatter(fm)}---\n\n# {title}\n\n"
        file_path.write_text(content, encoding="utf-8")

        return file_path

    def delete_article(self, path: str) -> bool:
        """删除文章"""
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = self.root / path

        if file_path.exists() and file_path.suffix == ".md":
            file_path.unlink()
            return True
        return False

    def edit_article(self, path: str, meta_only: bool = False) -> bool:
        """编辑文章（调用系统编辑器）"""
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = self.root / path

        if not file_path.exists():
            print(f"文件不存在: {file_path}")
            return False

        # 选择编辑器
        system = platform.system()
        if system == "Windows":
            editor = os.environ.get("EDITOR", "notepad")
        elif system == "Darwin":
            editor = os.environ.get("EDITOR", "open -a TextEdit")
        else:
            editor = os.environ.get("EDITOR", "nano")

        try:
            subprocess.run([editor, str(file_path)], shell=system == "Windows")
            return True
        except Exception as e:
            print(f"打开编辑器失败: {e}")
            return False

    def update_frontmatter(self, path: str, updates: Dict[str, Any]) -> bool:
        """更新 front matter"""
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = self.root / path

        if not file_path.exists():
            return False

        content = file_path.read_text(encoding="utf-8")
        fm, body = self._parse_frontmatter(content)

        # 更新
        fm.update(updates)

        # 写回
        new_content = f"---\n{self._format_frontmatter(fm)}---\n{body}"
        file_path.write_text(new_content, encoding="utf-8")
        return True

    def preview(self) -> bool:
        """启动本地预览"""
        try:
            subprocess.run(["hugo", "server", "-D"], cwd=self.root)
            return True
        except KeyboardInterrupt:
            return True
        except Exception as e:
            print(f"启动预览失败: {e}")
            return False

    def build(self) -> bool:
        """构建站点"""
        try:
            result = subprocess.run(
                ["hugo", "--minify"],
                cwd=self.root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("构建成功")
                return True
            else:
                print(f"构建失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"构建失败: {e}")
            return False

    def deploy(self, message: str = "update") -> bool:
        """部署到 GitHub"""
        try:
            # 检查是否有更改
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.root,
                capture_output=True,
                text=True
            )

            if not result.stdout.strip():
                print("没有需要提交的更改")
                return True

            # 添加、提交、推送
            subprocess.run(["git", "add", "."], cwd=self.root)
            subprocess.run(["git", "commit", "-m", message], cwd=self.root)
            subprocess.run(["git", "push"], cwd=self.root)

            print("部署成功")
            return True
        except Exception as e:
            print(f"部署失败: {e}")
            return False