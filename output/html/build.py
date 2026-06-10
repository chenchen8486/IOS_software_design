#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IOS 教员台手册 HTML 构建脚本

用法:
    python build.py

说明:
    1. 扫描 pages/ 目录下的所有页面片段文件
    2. 自动提取标题、正文、样式和脚本
    3. 根据文件名自动推导章节层级，生成导航侧边栏与面包屑
    4. 将结果写入 output/html/ 目录（覆盖原有 HTML）

新增页面流程:
    1. 在 pages/ 下新建页面片段（如 pages/ch2_1_intro.html）
    2. 运行 python build.py
    3. 自动在 output/html/ 生成完整页面（含导航）
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ──────────────────────────────────────────
# 可配置：虚拟分组标题（无独立文件的节）
# ──────────────────────────────────────────
NAV_GROUPS: Dict[str, str] = {
    "ch1_2": "1.2 控制面板工作区",
    # 未来如需更多分组，在此处添加，例如：
    # "ch2_1": "2.1 系统配置",
}

# 章节标题映射（根据 chapter 号自动生成顶层导航标题）
CHAPTER_TITLES: Dict[int, str] = {
    1: "第 1 章 CAE IOS功能详解",
    2: "第 2 章 软件架构与交互逆向设计",
}

# 无 <h1> 标签页面的标题兜底（优先从 <h1> 提取，无则回退到此处）
PAGE_TITLE_FALLBACKS: Dict[str, str] = {
    "ch1_1_components.html": "1.1 IOS组成部分与设计哲学",
}

# ──────────────────────────────────────────
# 路径常量
# ──────────────────────────────────────────
HTML_DIR = Path(__file__).parent.resolve()
PAGES_DIR = HTML_DIR / "pages"
TEMPLATE_FILE = HTML_DIR / "template.html"
GLOBAL_CSS_FILE = HTML_DIR / "static" / "global.css"


def parse_page(page_path: Path) -> Tuple[str, str, str, str]:
    """解析页面片段，返回 (page_styles, content, scripts, title)。"""
    text = page_path.read_text(encoding="utf-8-sig")

    # 提取 <style>...</style>（页面特有样式）
    page_styles = "\n".join(re.findall(r"<style>.*?</style>", text, re.DOTALL))

    # 提取 <script>...</script>
    scripts = "\n".join(re.findall(r"<script>.*?</script>", text, re.DOTALL))

    # 去掉 style 和 script 后的正文
    content = re.sub(r"<style>.*?</style>", "", text, flags=re.DOTALL)
    content = re.sub(r"<script>.*?</script>", "", content, flags=re.DOTALL)
    content = content.strip()

    # 从正文中提取 <h1> 作为标题（去除内部标签）
    h1_match = re.search(r"<h1>(.*?)</h1>", content, re.DOTALL)
    if h1_match:
        title = re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()
    else:
        # 无 <h1> 时回退到兜底配置或文件名
        title = PAGE_TITLE_FALLBACKS.get(page_path.name, page_path.stem)

    return page_styles, content, scripts, title


def parse_chapter_key(filename: str) -> Tuple[int, int, Optional[int]]:
    """从文件名解析章节号。

    例如:
        ch1_1_components.html   -> (1, 1, None)
        ch1_2_1_lesson.html     -> (1, 2, 1)
        ch1_10_3_xxx.html       -> (1, 10, 3)
    """
    m = re.match(r"ch(\d+)_(\d+)(?:_(\d+))?_(\w+)", filename)
    if not m:
        print(
            f"[警告] 文件名 '{filename}' 不符合 chX_Y_Z_xxx.html 规范，将被排在导航末尾",
            file=sys.stderr,
        )
        return (99, 99, 99)
    chapter = int(m.group(1))
    section = int(m.group(2))
    subsection = int(m.group(3)) if m.group(3) else None
    return chapter, section, subsection


def get_group_key(filename: str) -> Optional[str]:
    """返回该文件所属的分组键，若为一节条目则返回 None。"""
    chapter, section, subsection = parse_chapter_key(filename)
    if subsection is not None:
        return f"ch{chapter}_{section}"
    return None


def build_nav_tree(pages_info: List[Tuple[Path, str, str]]) -> List[dict]:
    """构建导航树结构。"""
    # pages_info: [(path, title, filename), ...]
    items = []
    for path, title, filename in pages_info:
        chapter, section, subsection = parse_chapter_key(filename)
        group_key = get_group_key(filename)
        items.append(
            {
                "path": path,
                "title": title,
                "filename": filename,
                "chapter": chapter,
                "section": section,
                "subsection": subsection,
                "group_key": group_key,
                "sort_key": (chapter, section, subsection or 0, filename),
            }
        )

    items.sort(key=lambda x: x["sort_key"])

    # 按 group 分组
    groups: Dict[Optional[str], List[dict]] = {}
    for item in items:
        gk = item["group_key"]
        groups.setdefault(gk, []).append(item)

    # 构建统一排序的树：一级叶子节点与分组节点混排
    tree_nodes = []

    # 一级条目（group_key 为 None）
    if None in groups:
        for item in groups[None]:
            tree_nodes.append(
                (
                    item["sort_key"],
                    {
                        "type": "leaf",
                        "title": item["title"],
                        "href": item["filename"],
                    },
                )
            )

    # 分组条目
    for gk in groups:
        if gk is None:
            continue
        children = groups[gk]
        group_title = NAV_GROUPS.get(gk, gk)
        # 分组的排序键：取该分组的章节号，小节设为 0
        g_chapter, g_section, _ = parse_chapter_key(gk + "_dummy.html")
        group_sort_key = (g_chapter, g_section, 0, "")
        tree_nodes.append(
            (
                group_sort_key,
                {
                    "type": "group",
                    "title": group_title,
                    "children": [
                        {
                            "type": "leaf",
                            "title": c["title"],
                            "href": c["filename"],
                        }
                        for c in children
                    ],
                },
            )
        )

    tree_nodes.sort(key=lambda x: x[0])
    return [node for _, node in tree_nodes]


def get_chapter_title(nav_tree: List[dict], current_href: str) -> str:
    """根据当前页面动态推导顶层章节标题。"""
    current_chapter, _, _ = parse_chapter_key(current_href)
    if current_chapter != 99:
        return CHAPTER_TITLES.get(current_chapter, f"第 {current_chapter} 章")

    # 兜底：从导航树中找最小章节号
    chapters = set()
    for node in nav_tree:
        if node["type"] == "leaf":
            chapter, _, _ = parse_chapter_key(node["href"])
            if chapter != 99:
                chapters.add(chapter)
        elif node["type"] == "group":
            for child in node["children"]:
                chapter, _, _ = parse_chapter_key(child["href"])
                if chapter != 99:
                    chapters.add(chapter)

    if not chapters:
        return "文档导航"

    min_chapter = min(chapters)
    return CHAPTER_TITLES.get(min_chapter, f"第 {min_chapter} 章")


def render_sidebar(nav_tree: List[dict], current_href: str) -> str:
    """渲染侧边栏 HTML，按章节分组，自动设置 active 与 collapsed。"""

    def render_leaf(node: dict, level: int = 0) -> str:
        cls = "nav-link"
        if node["href"] == current_href:
            cls += " active"
        return f'<a class="{cls}" href="{node["href"]}">{node["title"]}</a>'

    def render_group(node: dict, level: int = 0) -> str:
        # 判断当前页面是否在该分组内
        has_active = any(
            child.get("href") == current_href for child in node["children"]
        )
        toggle_cls = "nav-toggle"
        children_cls = "nav-children"
        if not has_active:
            toggle_cls += " collapsed"
            children_cls += " collapsed"

        children_html = "\n".join(render_leaf(c, level + 1) for c in node["children"])

        return (
            f'<div class="nav-group">\n'
            f'  <div class="{toggle_cls}" onclick="toggleNav(this)">'
            f'<span class="arrow">▼</span><span>{node["title"]}</span></div>\n'
            f'  <div class="{children_cls}">\n    {children_html}\n  </div>\n'
            f'</div>'
        )

    def get_node_chapter(node: dict) -> int:
        """从导航节点解析所属章节号。"""
        if node["type"] == "leaf":
            chapter, _, _ = parse_chapter_key(node["href"])
            return chapter
        elif node["type"] == "group" and node.get("children"):
            chapter, _, _ = parse_chapter_key(node["children"][0]["href"])
            return chapter
        return 99

    # 按章节号对导航节点分组
    chapter_nodes: Dict[int, List[dict]] = {}
    for node in nav_tree:
        ch = get_node_chapter(node)
        chapter_nodes.setdefault(ch, []).append(node)

    current_chapter, _, _ = parse_chapter_key(current_href)

    # 渲染每个章节的独立折叠组
    chapter_htmls = []
    for ch in sorted(chapter_nodes.keys()):
        nodes = chapter_nodes[ch]
        inner_html = "\n".join(
            render_group(n, 0) if n["type"] == "group" else render_leaf(n, 0)
            for n in nodes
        )

        chapter_title = CHAPTER_TITLES.get(ch, f"第 {ch} 章")
        is_current = ch == current_chapter

        toggle_cls = "nav-toggle"
        children_cls = "nav-children"
        if not is_current:
            toggle_cls += " collapsed"
            children_cls += " collapsed"

        chapter_htmls.append(
            f'<div class="nav-group">\n'
            f'  <div class="{toggle_cls}" onclick="toggleNav(this)">'
            f'<span class="arrow">▼</span><span>{chapter_title}</span></div>\n'
            f'  <div class="{children_cls}">\n    {inner_html}\n  </div>\n'
            f'</div>'
        )

    top_level_html = "\n".join(chapter_htmls)

    sidebar_html = (
        '<aside class="sidebar">\n'
        '  <div class="sidebar-header">'
        '<h1>CAE IOS 教员台</h1><p>结构化整理与可视化手册</p></div>\n'
        '  <nav class="nav-tree">\n'
        f'    {top_level_html}\n'
        '  </nav>\n'
        '</aside>'
    )
    return sidebar_html


def render_breadcrumb(nav_tree: List[dict], current_href: str) -> str:
    """渲染面包屑。"""
    # 在导航树中查找当前页面
    current_title = current_href
    parent_title = None

    for node in nav_tree:
        if node["type"] == "leaf" and node["href"] == current_href:
            current_title = node["title"]
            break
        elif node["type"] == "group":
            for child in node["children"]:
                if child["href"] == current_href:
                    current_title = child["title"]
                    parent_title = node["title"]
                    break
            if parent_title:
                break

    # 动态推导面包屑中的章节标题
    chapter_title = get_chapter_title(nav_tree, current_href)

    parts = ['<a href="#">首页</a>']
    parts.append('<span class="breadcrumb-sep">/</span>')
    parts.append(f'<a href="#">{chapter_title}</a>')
    if parent_title:
        parts.append('<span class="breadcrumb-sep">/</span>')
        parts.append(f'<a href="#">{parent_title}</a>')
    parts.append('<span class="breadcrumb-sep">/</span>')
    parts.append(f'<span>{current_title}</span>')

    return '<div class="breadcrumb">\n    ' + "\n    ".join(parts) + "\n  </div>"


def build() -> None:
    if not TEMPLATE_FILE.exists():
        print(f"[错误] 模板文件不存在: {TEMPLATE_FILE}", file=sys.stderr)
        sys.exit(1)

    if not PAGES_DIR.exists():
        print(f"[错误] 页面目录不存在: {PAGES_DIR}", file=sys.stderr)
        sys.exit(1)

    template = TEMPLATE_FILE.read_text(encoding="utf-8-sig")

    # 读取全局 CSS
    global_styles = ""
    if GLOBAL_CSS_FILE.exists():
        global_css = GLOBAL_CSS_FILE.read_text(encoding="utf-8-sig")
        global_styles = f"<style>\n{global_css}\n</style>"
    else:
        print(f"[警告] 全局 CSS 文件不存在: {GLOBAL_CSS_FILE}", file=sys.stderr)

    # 扫描页面
    page_files = sorted(PAGES_DIR.glob("*.html"))
    if not page_files:
        print("[警告] pages/ 目录下未找到任何 HTML 文件", file=sys.stderr)
        sys.exit(0)

    pages_info = []
    for pf in page_files:
        _, _, _, title = parse_page(pf)
        pages_info.append((pf, title, pf.name))

    # 构建导航树（基于所有页面）
    nav_tree = build_nav_tree(pages_info)

    built_count = 0
    for pf, title, filename in pages_info:
        page_styles, content, scripts, _ = parse_page(pf)

        sidebar = render_sidebar(nav_tree, filename)
        breadcrumb = render_breadcrumb(nav_tree, filename)

        page_html = (
            template.replace("{{TITLE}}", title)
            .replace("{{GLOBAL_STYLES}}", global_styles)
            .replace("{{PAGE_STYLES}}", page_styles)
            .replace("{{SIDEBAR}}", sidebar)
            .replace("{{BREADCRUMB}}", breadcrumb)
            .replace("{{CONTENT}}", content)
            .replace("{{BODY_SCRIPT}}", scripts)
        )

        out_path = HTML_DIR / filename
        out_path.write_text(page_html, encoding="utf-8-sig")
        built_count += 1
        print(f"  [生成] {filename}")

    print(f"\n完成！共生成 {built_count} 个页面。")


if __name__ == "__main__":
    build()
