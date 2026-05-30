# -*- coding: utf-8 -*-
"""
CAE IOS使用手册 Markdown 优化脚本
功能：
1. 结构化：优化层次标题
2. 表格化：将参数列表、按钮功能、状态说明等转换为 Markdown 表格
3. 图文对照：让图片紧跟相关描述
4. 紧凑化：删除多余空行，合并过度分散的短段落
"""

import re
import sys
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
        # 如果是标题、表格、图片、列表项、空行，则先flush buffer
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


def try_convert_button_function_table(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    尝试将连续的 "## X.Y.Z 按钮名" + "点击此按钮..." 模式转换为表格
    返回 (新行列表, 消费行数)
    """
    # 查找连续的 "按钮/字段/参数" 说明段落
    consumed = 0
    entries = []
    i = start
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # 匹配标题行如 ## 5.5.1 自动运行
        m = re.match(r"^(#{2,4}\s+)([\d.]+\s+)?(.+)$", stripped)
        if not m:
            break
        title = m.group(3).strip()
        # 下一行应该是描述
        if i + 1 >= len(lines):
            break
        desc_line = lines[i + 1].strip()
        if not desc_line or desc_line.startswith("#") or desc_line.startswith("|") or desc_line.startswith("!["):
            break
        # 允许描述跨1-3行
        desc = desc_line
        j = i + 2
        while j < len(lines) and j < i + 5:
            next_s = lines[j].strip()
            if next_s == "" or next_s.startswith("#") or next_s.startswith("|") or next_s.startswith("!["):
                break
            desc += " " + next_s
            j += 1
        entries.append((title, desc))
        i = j
        # 跳过中间的空行
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        consumed = i - start

    if len(entries) >= 3:
        table_lines = ["| 项目 | 说明 |", "|------|------|"]
        for title, desc in entries:
            table_lines.append(f"| **{title}** | {desc} |")
        return table_lines, consumed
    return None, 0


def try_convert_parameter_table(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    尝试识别 "参数名 + 调节方式 + 说明" 或 "参数名 + 说明" 的列表并转为表格
    """
    # 简单策略：如果连续多行是 "## 7.1.X 参数名" + 描述，且数量>=3，则表格化
    return try_convert_button_function_table(lines, start)


def convert_list_to_table_if_possible(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    通用入口：尝试将连续的短标题+描述段落转换为表格
    """
    return try_convert_button_function_table(lines, start)


def move_image_closer(lines: list[str]) -> list[str]:
    """
    图文对照：如果图片行后面紧跟图注，且与前面的内容相隔较远，
    尝试将图片+图注上移，紧跟在相关描述之后。
    这里采用保守策略：如果图片前面是空行，且再前面是标题或表格，则保持不动；
    否则，如果图片与前面的段落之间有超过2个空行，则压缩空行。
    """
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)
        if line.strip().startswith("!["):
            # 图片后面的图注行
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("图"):
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
