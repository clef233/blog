"""
博客管理后台 - Flask Web 应用
"""

import os
import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# 博客根目录
BLOG_ROOT = Path(__file__).parent.parent.parent
CONTENT_DIR = BLOG_ROOT / "content"
POSTS_DIR = CONTENT_DIR / "posts"


@dataclass
class Article:
    """文章数据类"""
    path: str
    title: str = ""
    date: Optional[str] = None
    draft: bool = False
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    description: str = ""
    content: str = ""
    word_count: int = 0


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
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


def format_frontmatter(fm: Dict[str, Any]) -> str:
    """格式化 front matter"""
    return yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False)


def load_article(path: Path) -> Optional[Article]:
    """加载文章"""
    try:
        content = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)

        date_str = None
        if fm.get("date"):
            if isinstance(fm["date"], datetime):
                date_str = fm["date"].strftime("%Y-%m-%d %H:%M")
            elif isinstance(fm["date"], str):
                date_str = fm["date"][:19].replace("T", " ")

        return Article(
            path=str(path.relative_to(BLOG_ROOT)).replace("\\", "/"),  # 统一使用正斜杠
            title=fm.get("title", path.stem),
            date=date_str,
            draft=fm.get("draft", False),
            tags=fm.get("tags", []),
            categories=fm.get("categories", []),
            description=fm.get("description", ""),
            content=body,
            word_count=len(body.replace("\n", "").replace(" ", ""))
        )
    except Exception as e:
        print(f"加载文章失败: {path} - {e}")
        return None


def get_articles() -> List[Dict]:
    """获取所有文章"""
    articles = []
    if POSTS_DIR.exists():
        for md_file in POSTS_DIR.rglob("*.md"):
            article = load_article(md_file)
            if article:
                articles.append(asdict(article))

    # 按日期排序
    articles.sort(key=lambda a: a.get('date') or '', reverse=True)
    return articles


def get_stats() -> Dict:
    """获取统计信息"""
    articles = get_articles()

    tag_counts: Dict[str, int] = {}
    for a in articles:
        for tag in a.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    return {
        "total": len(articles),
        "published": len([a for a in articles if not a.get('draft')]),
        "drafts": len([a for a in articles if a.get('draft')]),
        "total_words": sum(a.get('word_count', 0) for a in articles),
        "tags": dict(sorted(tag_counts.items(), key=lambda x: -x[1])[:10])
    }


# ========== 路由 ==========

@app.route('/')
def index():
    """管理后台首页"""
    return render_template('index.html')


@app.route('/api/articles')
def api_articles():
    """获取文章列表"""
    return jsonify(get_articles())


@app.route('/api/stats')
def api_stats():
    """获取统计信息"""
    return jsonify(get_stats())


@app.route('/api/article/<path:article_path>')
def api_article(article_path):
    """获取单篇文章"""
    path = BLOG_ROOT / article_path
    if not path.exists():
        return jsonify({"error": "文章不存在"}), 404

    article = load_article(path)
    if article:
        return jsonify(asdict(article))
    return jsonify({"error": "加载失败"}), 500


@app.route('/api/article', methods=['POST'])
def create_article():
    """创建文章"""
    data = request.json

    title = data.get('title', '未命名')
    now = datetime.now()
    year = now.year

    # 生成文件名
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s]+', '-', slug)

    # 确保目录存在
    year_dir = POSTS_DIR / str(year)
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
        "tags": data.get('tags', []),
        "categories": data.get('categories', ["未分类"]),
        "author": "clef233",
        "description": data.get('description', "")
    }

    content = f"---\n{format_frontmatter(fm)}---\n\n{data.get('content', '')}\n"
    file_path.write_text(content, encoding="utf-8")

    return jsonify({
        "success": True,
        "path": str(file_path.relative_to(BLOG_ROOT))
    })


@app.route('/api/article/<path:article_path>', methods=['PUT'])
def update_article(article_path):
    """更新文章"""
    path = BLOG_ROOT / article_path
    if not path.exists():
        return jsonify({"error": "文章不存在"}), 404

    data = request.json

    # 读取现有内容
    content = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    # 更新 front matter
    if 'title' in data:
        fm['title'] = data['title']
    if 'tags' in data:
        fm['tags'] = data['tags']
    if 'categories' in data:
        fm['categories'] = data['categories']
    if 'description' in data:
        fm['description'] = data['description']
    if 'draft' in data:
        fm['draft'] = data['draft']

    # 更新正文
    new_body = data.get('content', body)

    # 写回
    new_content = f"---\n{format_frontmatter(fm)}---\n{new_body}"
    path.write_text(new_content, encoding="utf-8")

    return jsonify({"success": True})


@app.route('/api/article/<path:article_path>', methods=['DELETE'])
def delete_article(article_path):
    """删除文章"""
    path = BLOG_ROOT / article_path
    if not path.exists():
        return jsonify({"error": "文章不存在"}), 404

    path.unlink()
    return jsonify({"success": True})


@app.route('/api/build', methods=['POST'])
def build_site():
    """构建站点"""
    import subprocess
    try:
        result = subprocess.run(
            ["hugo", "--minify"],
            cwd=BLOG_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return jsonify({"success": True, "message": "构建成功"})
        return jsonify({"success": False, "message": result.stderr})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/api/deploy', methods=['POST'])
def deploy_site():
    """部署到 GitHub"""
    import subprocess
    try:
        subprocess.run(["git", "add", "."], cwd=BLOG_ROOT)
        subprocess.run(["git", "commit", "-m", "update"], cwd=BLOG_ROOT)
        subprocess.run(["git", "push"], cwd=BLOG_ROOT)
        return jsonify({"success": True, "message": "部署成功"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)