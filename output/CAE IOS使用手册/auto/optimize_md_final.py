# -*- coding: utf-8 -*-
"""
CAE IOS使用手册 Markdown 优化脚本 - Final Version
功能：
1. 结构化：优化层次标题
2. 表格化：将参数列表、按钮功能、状态说明等转换为 Markdown 表格
3. 图文对照：让图片紧跟相关描述
4. 紧凑化：删除多余空行，合并过度分散的短段落

策略：
- 识别 "## X.Y.Z 名称" + "点击此按钮..." 的连续段落，批量转为表格
- 识别 "o 项目" 或 "- 项目" 列表，如果项目简短且数量多，转为表格
- 保留所有原始文字、图片引用、图注
"""

import re
from pathlib import Path

INPUT_PATH = Path(r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md")
OUTPUT_PATH = Path(r"D:\project\python_release\avation_doc\output\CAE IOS使用手册\auto\CAE IOS使用手册_zh_整理版.md")


def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


def write_file(path: Path, content: str):
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(content)


def compact_blank_lines(lines: list[str]) -> list[str]:
    """删除多余空行，段落之间最多保留一个空行"""
    result = []
    prev_blank = False
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if not prev_blank:
                result.append(line)
            prev_blank = True
        else:
            result.append(line)
            prev_blank = False
    return result


def merge_short_paragraphs(lines: list[str]) -> list[str]:
    """合并过度分散的短段落（非标题、非表格、非图片、非列表项的短行）"""
    result = []
    buffer = ""
    for line in lines:
        stripped = line.strip()
        # 如果是标题、表格、图片、列表项、空行、公式，则先flush buffer
        if (
            stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("![")
            or stripped.startswith("o ")
            or stripped.startswith("- ")
            or stripped.startswith("• ")
            or stripped == ""
            or stripped.startswith("$")
            or stripped.startswith("(")
            or stripped.startswith("> ")
        ):
            if buffer:
                result.append(buffer)
                buffer = ""
            result.append(line)
            continue

        # 如果当前行很短（< 60字符），尝试合并
        if len(stripped) < 60 and not buffer:
            buffer = stripped
        elif buffer:
            # 合并到前一行
            buffer = buffer + " " + stripped
            if len(buffer) > 120:
                result.append(buffer)
                buffer = ""
        else:
            result.append(line)
    if buffer:
        result.append(buffer)
    return result


def is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s+", line.strip()))


def is_image_line(line: str) -> bool:
    return line.strip().startswith("![")


def is_caption_line(line: str) -> bool:
    return bool(re.match(r"^图\s*\d+", line.strip()))


def is_table_line(line: str) -> bool:
    return line.strip().startswith("|")


def is_list_item(line: str) -> bool:
    s = line.strip()
    return s.startswith("o ") or s.startswith("- ") or s.startswith("• ") or re.match(r"^\d+\)", s)


def is_blank(line: str) -> bool:
    return line.strip() == ""


def try_convert_button_function_table(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    尝试将连续的 "## X.Y.Z 按钮名" + "点击此按钮..." 模式转换为表格
    返回 (新行列表, 消费行数)
    """
    i = start
    entries = []
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # 匹配标题行如 ## 5.5.1 自动运行 或 ### 7.2.3.1 无雾
        m = re.match(r"^(#{2,4}\s+)([\d.]+\s+)?(.+)$", stripped)
        if not m:
            break
        title = m.group(3).strip()
        # 收集描述，跨1-5行，直到遇到空行/标题/图片/表格/列表项
        desc_lines = []
        j = i + 1
        while j < len(lines) and j < i + 6:
            next_s = lines[j].strip()
            if next_s == "" or is_heading(lines[j]) or is_image_line(lines[j]) or is_table_line(lines[j]) or is_list_item(lines[j]):
                break
            desc_lines.append(next_s)
            j += 1
        if not desc_lines:
            break
        desc = " ".join(desc_lines)
        entries.append((title, desc))
        i = j
        # 跳过中间的空行
        while i < len(lines) and is_blank(lines[i]):
            i += 1

    if len(entries) >= 3:
        table_lines = ["| 项目 | 说明 |", "|------|------|"]
        for title, desc in entries:
            table_lines.append(f"| **{title}** | {desc} |")
        return table_lines, i - start
    return None, 0


def try_convert_simple_list_table(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    尝试将连续的 "o 项目" 或 "- 项目" 短列表转为表格
    例如：
    o 高度
    o 空速
    o 航向
    """
    i = start
    items = []
    while i < len(lines):
        s = lines[i].strip()
        m = re.match(r"^[o\-\•]\s+(.+)$", s)
        if not m:
            break
        items.append(m.group(1).strip())
        i += 1
        while i < len(lines) and is_blank(lines[i]):
            i += 1

    if len(items) >= 4 and all(len(x) < 40 for x in items):
        table_lines = ["| 项目 |", "|------|"]
        for it in items:
            table_lines.append(f"| {it} |")
        return table_lines, i - start
    return None, 0


def convert_list_to_table_if_possible(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    通用入口：尝试将连续的短标题+描述段落转换为表格
    """
    # 先尝试按钮/参数表格
    table_lines, consumed = try_convert_button_function_table(lines, start)
    if table_lines:
        return table_lines, consumed
    # 再尝试简单列表表格
    table_lines, consumed = try_convert_simple_list_table(lines, start)
    if table_lines:
        return table_lines, consumed
    return None, 0


def move_image_closer(lines: list[str]) -> list[str]:
    """
    图文对照：压缩图片与前面内容之间的多余空行
    """
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)
        if is_image_line(line):
            # 图片后面的图注行
            if i + 1 < len(lines) and is_caption_line(lines[i + 1]):
                result.append(lines[i + 1])
                i += 2
                continue
        i += 1
    return result


def optimize_markdown(content: str) -> str:
    lines = content.splitlines()

    # Step 1: 紧凑化空行
    lines = compact_blank_lines(lines)

    # Step 2: 合并短段落
    lines = merge_short_paragraphs(lines)

    # Step 3: 表格化连续短标题段落
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # 尝试匹配 "## 数字.数字... 名称" 这种深层标题
        if re.match(r"^#{2,4}\s+\d+(\.\d+)*\s+.+$", stripped):
            table_lines, consumed = convert_list_to_table_if_possible(lines, i)
            if table_lines and consumed > 0:
                # 在表格前保留一个空行（如果前面不是空行）
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append("")
                new_lines.extend(table_lines)
                new_lines.append("")
                i += consumed
                continue
        new_lines.append(line)
        i += 1
    lines = new_lines

    # Step 4: 再次紧凑化
    lines = compact_blank_lines(lines)

    # Step 5: 图文对照微调
    lines = move_image_closer(lines)

    return "\n".join(lines)


def main():
    print("读取原始文件...")
    content = read_file(INPUT_PATH)
    print(f"原始文件大小: {len(content)} 字符, {content.count(chr(10))} 行")

    print("开始优化...")
    optimized = optimize_markdown(content)

    print("写入优化后的文件...")
    write_file(OUTPUT_PATH, optimized)
    print(f"优化完成。输出文件: {OUTPUT_PATH}")
    print(f"优化后文件大小: {len(optimized)} 字符, {optimized.count(chr(10))} 行")


if __name__ == "__main__":
    main()
