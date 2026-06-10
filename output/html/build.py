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


def parse_page(page_path: Path) -> Tuple[str, str, str, str]:
    """解析页面片段，返回 (styles, content, scripts, title)。"""
    text = page_path.read_text(encoding="utf-8-sig")

    # 提取 <style>...</style>
    styles = "\n".join(re.findall(r"<style>.*?</style>", text, re.DOTALL))

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

    return styles, content, scripts, title


def parse_chapter_key(filename: str) -> Tuple[int, int, Optional[int]]:
    """从文件名解析章节号。

    例如:
        ch1_1_components.html   -> (1, 1, None)
        ch1_2_1_lesson.html     -> (1, 2, 1)
        ch1_10_3_xxx.html       -> (1, 10, 3)
    """
    m = re.match(r"ch(\d+)_(\d+)(?:_(\d+))?_", filename)
    if not m:
        return (99, 99, 99)  # 未识别放到最后
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
        g_chapter, g_section, _ = parse_chapter_key(gk + "_.html")
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


def render_sidebar(nav_tree: List[dict], current_href: str) -> str:
    """渲染侧边栏 HTML，自动设置 active 与 collapsed。"""

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

    # 顶层固定为"第 1 章 软件操作"（可扩展为动态）
    # 自动推导章节标题：取所有叶子节点的 chapter 最小值
    top_level_html = "\n".join(
        render_group(n, 0) if n["type"] == "group" else render_leaf(n, 0)
        for n in nav_tree
    )

    sidebar_html = (
        '<aside class="sidebar">\n'
        '  <div class="sidebar-header">'
        '<h1>CAE IOS 教员台</h1><p>结构化整理与可视化手册</p></div>\n'
        '  <nav class="nav-tree">\n'
        '    <div class="nav-group">\n'
        '      <div class="nav-toggle" onclick="toggleNav(this)">'
        '<span class="arrow">▼</span><span>第 1 章 软件操作</span></div>\n'
        '      <div class="nav-children">\n'
        f'        {top_level_html}\n'
        '      </div>\n'
        '    </div>\n'
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

    parts = ['<a href="#">首页</a>']
    parts.append('<span class="breadcrumb-sep">/</span>')
    parts.append('<a href="#">第 1 章 软件操作</a>')
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
        styles, content, scripts, _ = parse_page(pf)

        sidebar = render_sidebar(nav_tree, filename)
        breadcrumb = render_breadcrumb(nav_tree, filename)

        page_html = (
            template.replace("{{TITLE}}", title)
            .replace("{{HEAD_EXTRA}}", styles)
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
