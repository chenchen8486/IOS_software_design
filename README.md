# CAE IOS 教员台软件 — 结构化整理与可视化项目

> 项目路径：`D:\project\python_release\IOS_software_design`
> 核心目标：将 CAE A320 Neo IOS 教员台用户手册翻译、拆解、结构化为中文开发文档，并以 HTML 形式可视化输出。

---

## 1. 目录结构

```
IOS_software_design/
├── docs/                # 设计文档与开发规范
│   ├── A320_与_原始手册_章节映射表.md
│   ├── HTML生成规范与转换规则.md
│   └── 需求描述与工作计划.md
├── output/              # 最终产物输出目录
│   └── html/            # HTML 可视化页面与细化 MD
│       ├── ch2_2_1_lesson_plan_tab.html
│       ├── ch2_2_2_doc_tab.html
│       ├── ch2_2_3_current_conditions_tab.html
│       └── images/      # HTML 配图统一归集目录
├── reference/           # 原始参考文档、解析产物与中文主文档
│   ├── A320.md          # 中文主文档（用户整理，入口文档）
│   ├── CAE IOS使用手册.pdf
│   ├── CAE IOS使用手册.md
│   ├── CAE IOS使用手册_zh.md
│   └── images/          # 原始 PDF 解析配图
├── temp/                # 中间产物与缓存（按需使用）
├── CLAUDE.md            # AI 开发助手行为规范
└── README.md            # 本文件
```

---

## 2. 文档阅读顺序（Claude 新会话快速恢复）

每次开启新会话继续下一章节转换时，请按以下顺序阅读：

1. **`docs/需求描述与工作计划.md`**
   - 了解项目背景、原始资料位置、双文档对照逻辑、工作节奏。

2. **`docs/HTML生成规范与转换规则.md`**
   - 了解文件输出路径、图片处理规则、HTML 结构模板、内容红线、Checklist。

3. **`docs/A320_与_原始手册_章节映射表.md`**
   - 了解 A320.md 章节与原始手册章节的对应关系，确认目标章节的精确层级归属。

4. **`reference/A320.md`**
   - 定位到当前待处理的章节，提取已整理的功能描述作为内容锚点。

5. **`reference/CAE IOS使用手册.md`（或 `_zh.md`）**
   - 作为结构校验器，确认功能点的上级菜单、同级并列关系与嵌套逻辑。

---

## 3. 当前进度

### 已完成（第 2 章 — 控制面板工作区）

| 章节 | A320.md 标题 | 原始手册对应 | 状态 |
|------|-------------|-------------|------|
| 2.2.1 | 课程计划选项卡（LESSON PLAN） | ## 5. LESSON PLAN Tab | ✅ 已完成 |
| 2.2.2 | 文档选项卡（DOCS） | ## 6. DOCS Tab | ✅ 已完成 |
| 2.2.3 | 当前条件选项卡（CURRENT CONDITIONS） | ## 7. CURRENT CONDITIONS Tab | ✅ 已完成 |

### 待处理

| 章节 | A320.md 标题 | 原始手册对应 | 状态 |
|------|-------------|-------------|------|
| 2.2.4 | 飞机/航空器选项卡（AIRCRAFT） | ## 8. AIRCRAFT Tab | ⏳ 下一章 |
| 2.2.5 | 参考机场选项卡（REFERENCE AIRPORT） | ## 9. REFERENCE AIRPORT Tab | 🔜 待处理 |
| 2.2.6 | 教员台滑动面板（INSTRUCTOR STATION Sliding Panel） | ## 10. INSTRUCTOR STATION Sliding Panel | 🔜 待处理 |
| 2.2.7 | 控制面板底部（Footer） | ## 11. Control Board Footer | 🔜 待处理 |
| 2.3 | 维护页面（Maintenance Pages） | ## 12. Maintenance Pages | 🔜 待处理 |
| 2.4 | 仪表复示器工作区（INSTRUMENT REPEATER） | ## 13. INSTRUMENT REPEATER Workspace | 🔜 待处理 |
| 2.5 | 课程计划配置工作区（Lesson Plan Profile） | ## 14. Lesson Plan Profile Workspace | 🔜 待处理 |
| 2.6 | 地图工作区（Map） | ## 15. Map Workspace | 🔜 待处理 |
| 2.7 | 高级（Advanced） | ## 16. Advanced | 🔜 待处理 |
| 2.8 | 参考流程 | 无直接对应 | 🔜 待处理 |
| 4~10 | 开发设计章节 | 无直接对应 | 🔜 待填充 |

---

## 4. 快速启动指令模板

用户可以在新会话中直接使用以下指令：

> **"请阅读项目 docs 目录和 README.md，继续转换下一章节的 HTML。"**

Claude 将自动：
1. 阅读本 `README.md` 了解项目结构与当前进度。
2. 按顺序阅读 `docs/` 下的三份规范文档。
3. 读取 `reference/A320.md` 与 `reference/CAE IOS使用手册.md` 进行双文档对照。
4. 生成下一章节的细化 Markdown + HTML 文件。

---

## 5. 环境说明

- **虚拟环境**：`conda activate Chen`
- **Python 版本**：3.10+
- **关键依赖**：详见 `requirements.txt`（如有）
- **编码规范**：所有文本读写强制使用 `encoding='utf-8-sig'`

---

## 6. 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-05-30 | V0.1 | 项目初始化，完成 2.2.1、2.2.2 章节 |
| 2026-06-01 | V0.2 | 完成 2.2.3 章节；重构 Mermaid 图表交互（点击放大 / 滚轮缩放 / 拖拽平移） |
| 2026-06-01 | V0.3 | 迁移参考文件至 `reference/` 目录；创建根目录 `README.md`；统一文档路径引用 |
