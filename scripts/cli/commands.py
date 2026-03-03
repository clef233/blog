"""
CLI 命令定义
"""

import os
import sys
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

from .manager import BlogManager

# Windows 控制台兼容
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

console = Console(force_terminal=True)


def get_manager():
    """获取博客管理器"""
    return BlogManager()


# ========== 主命令组 ==========
@click.group(help="博客管理 CLI 工具")
def cli():
    pass


# ========== list 命令 ==========
@cli.command("list", help="列出所有文章")
@click.option("--tag", "-t", help="按标签筛选")
@click.option("--category", "-c", help="按分类筛选")
@click.option("--draft", "-d", is_flag=True, help="仅显示草稿")
@click.option("--published", "-p", is_flag=True, help="仅显示已发布")
def list_articles(tag, category, draft, published):
    manager = get_manager()

    # 处理互斥选项
    draft_filter = None
    if draft and not published:
        draft_filter = True
    elif published and not draft:
        draft_filter = False

    articles = manager.list_articles(tag=tag, category=category, draft=draft_filter)

    if not articles:
        console.print("[yellow]没有找到文章[/yellow]")
        return

    table = Table(title=f"文章列表 (共 {len(articles)} 篇)")
    table.add_column("标题", style="cyan", max_width=40)
    table.add_column("日期", style="green", width=12)
    table.add_column("状态", style="magenta", width=8)
    table.add_column("标签", style="yellow", max_width=25)
    table.add_column("字数", justify="right", width=6)

    for article in articles:
        status = "[red]草稿[/red]" if article.draft else "[green]发布[/green]"
        date_str = article.date.strftime("%Y-%m-%d") if article.date else "-"
        tags_str = ", ".join(article.tags[:3])
        if len(article.tags) > 3:
            tags_str += "..."

        table.add_row(
            article.title[:40] + ("..." if len(article.title) > 40 else ""),
            date_str,
            status,
            tags_str,
            str(article.word_count)
        )

    console.print(table)


# ========== stats 命令 ==========
@cli.command("stats", help="显示博客统计")
def stats():
    manager = get_manager()
    stats = manager.get_stats()

    # 总览面板
    overview = Panel(
        f"[bold]总文章数:[/bold] {stats['total']}\n"
        f"[bold]已发布:[/bold] [green]{stats['published']}[/green]\n"
        f"[bold]草稿:[/bold] [red]{stats['drafts']}[/red]\n"
        f"[bold]总字数:[/bold] {stats['total_words']:,}",
        title="[博客统计]",
        border_style="blue"
    )
    console.print(overview)

    # 标签云
    if stats['tags']:
        console.print("\n[bold][标签分布][/bold]")
        tags_table = Table(show_header=False)
        tags_table.add_column("标签", style="cyan")
        tags_table.add_column("数量", justify="right")
        for tag, count in list(stats['tags'].items())[:10]:
            tags_table.add_row(tag, str(count))
        console.print(tags_table)

    # 分类分布
    if stats['categories']:
        console.print("\n[bold][分类分布][/bold]")
        for cat, count in stats['categories'].items():
            console.print(f"  {cat}: {count}")

    # 年份分布
    if stats['years']:
        console.print("\n[bold][年份分布][/bold]")
        for year, count in stats['years'].items():
            console.print(f"  {year}: {count} 篇")


# ========== new 命令 ==========
@cli.command("new", help="创建新文章")
@click.argument("title")
@click.option("--tag", "-t", multiple=True, help="添加标签")
@click.option("--category", "-c", default="未分类", help="设置分类")
def new_article(title, tag, category):
    manager = get_manager()

    path = manager.create_article(
        title=title,
        categories=[category] if category else None,
        tags=list(tag) if tag else None
    )

    console.print(f"[green]OK[/green] 创建成功: {path}")
    console.print(f"[dim]提示: 使用 'blog edit {path.relative_to(manager.root)}' 编辑文章[/dim]")


# ========== edit 命令 ==========
@cli.command("edit", help="编辑文章")
@click.argument("path")
@click.option("--meta", "-m", is_flag=True, help="仅编辑 front matter（暂不支持）")
def edit_article(path, meta):
    manager = get_manager()

    console.print(f"[dim]打开编辑器: {path}[/dim]")
    success = manager.edit_article(path)

    if success:
        console.print("[green]OK[/green] 编辑完成")
    else:
        console.print("[red]FAIL[/red] 编辑失败")


# ========== delete 命令 ==========
@cli.command("delete", help="删除文章")
@click.argument("path")
@click.option("--yes", "-y", is_flag=True, help="跳过确认")
def delete_article(path, yes):
    manager = get_manager()

    if not yes:
        if not click.confirm(f"确定要删除 {path}?"):
            console.print("[yellow]已取消[/yellow]")
            return

    success = manager.delete_article(path)

    if success:
        console.print(f"[green]OK[/green] 已删除: {path}")
    else:
        console.print(f"[red]FAIL[/red] 删除失败: 文件不存在或不是 .md 文件")


# ========== preview 命令 ==========
@cli.command("preview", help="启动本地预览服务器")
def preview():
    manager = get_manager()
    console.print("[cyan]启动 Hugo 服务器...[/cyan]")
    console.print("[dim]访问 http://localhost:1313[/dim]")
    console.print("[dim]按 Ctrl+C 停止[/dim]\n")
    manager.preview()


# ========== build 命令 ==========
@cli.command("build", help="构建静态站点")
def build():
    manager = get_manager()
    console.print("[cyan]构建中...[/cyan]")
    manager.build()


# ========== deploy 命令 ==========
@cli.command("deploy", help="部署到 GitHub")
@click.option("--message", "-m", default="update", help="提交信息")
def deploy(message):
    manager = get_manager()
    console.print("[cyan]部署中...[/cyan]")
    manager.deploy(message=message)


if __name__ == "__main__":
    cli()