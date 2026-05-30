#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

html = '<td rowspan=1 colspan=1>标签页</td>'

# 旧正则
cells = re.findall(r'<[tdh][^>]*>(.*?)</[tdh]>', html, re.DOTALL | re.IGNORECASE)
print('old regex cells:', cells)

# 新正则
cells = re.findall(r'<[tdh][^>]*>(.*?)</t[dh]>', html, re.DOTALL | re.IGNORECASE)
print('new regex cells:', cells)

# 完整表格测试
html3 = '<table><tr><td rowspan=1 colspan=1>标签页</td><td rowspan=1 colspan=1>区域</td></tr><tr><td>当前条件</td><td></td></tr></table>'
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html3, re.DOTALL | re.IGNORECASE)
print('rows:', len(rows))
for tr in rows:
    cells = re.findall(r'<[tdh][^>]*>(.*?)</t[dh]>', tr, re.DOTALL | re.IGNORECASE)
    print('cells:', cells)
