#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将文档中的 HTML 表格转换为 Markdown 表格"""

import re

input_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"
output_path = r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md"

with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()


def parse_html_table(html: str) -> list[list[str]]:
    """解析简单的 HTML 表格，返回二维字符串列表"""
    rows = []
    # 提取所有 tr 标签之间的内容
    tr_blocks = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL | re.IGNORECASE)
    for tr in tr_blocks:
        # 提取 td 或 th
        cells = re.findall(r"<[tdh][^>]*>(.*?)</t[dh]>", tr, re.DOTALL | re.IGNORECASE)
        # 去除 HTML 标签并清理空白
        cleaned_cells = []
        for cell in cells:
            # 去除内部 HTML 标签
            text = re.sub(r"<[^>]+>", "", cell)
            text = text.strip()
            cleaned_cells.append(text)
        if cleaned_cells:
            rows.append(cleaned_cells)
    return rows


def rows_to_markdown(rows: list[list[str]]) -> str:
    """将二维列表转换为 Markdown 表格字符串"""
    if not rows:
        return ""

    # 计算最大列数
    max_cols = max(len(r) for r in rows)

    # 补齐每行的列数
    for r in rows:
        while len(r) < max_cols:
            r.append("")

    # 计算每列的最大宽度（用于对齐）
    col_widths = [0] * max_cols
    for r in rows:
        for i, cell in enumerate(r):
            # 中文字符宽度按2计算
            width = sum(2 if ord(c) > 127 else 1 for c in cell)
            col_widths[i] = max(col_widths[i], width)

    def pad_cell(cell: str, width: int) -> str:
        cell_width = sum(2 if ord(c) > 127 else 1 for c in cell)
        pad = width - cell_width
        return cell + " " * max(0, pad)

    lines = []
    for i, r in enumerate(rows):
        line = "| " + " | ".join(pad_cell(c, col_widths[j]) for j, c in enumerate(r)) + " |"
        lines.append(line)
        if i == 0:
            # 分隔行
            sep = "|" + "|".join("-" * (col_widths[j] + 2) for j in range(max_cols)) + "|"
            lines.append(sep)

    return "\n".join(lines)


def replace_html_tables(text: str) -> str:
    """查找所有 HTML 表格并替换为 Markdown 表格"""
    pattern = re.compile(r"<table[^>]*>.*?</table>", re.DOTALL | re.IGNORECASE)

    def replacer(match):
        html = match.group(0)
        rows = parse_html_table(html)
        if not rows:
            return ""
        md = rows_to_markdown(rows)
        return "\n" + md + "\n"

    return pattern.sub(replacer, text)


new_content = replace_html_tables(content)

with open(output_path, "w", encoding="utf-8-sig") as f:
    f.write(new_content)

# 统计转换数量
table_count = len(re.findall(r"<table[^>]*>.*?</table>", content, re.DOTALL | re.IGNORECASE))
remaining = len(re.findall(r"<table[^>]*>.*?</table>", new_content, re.DOTALL | re.IGNORECASE))

print(f"原始 HTML 表格数: {table_count}")
print(f"剩余 HTML 表格数: {remaining}")
print(f"转换完成，已保存至: {output_path}")
