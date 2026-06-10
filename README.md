# CAE IOS 教员台软件 — 结构化整理与可视化项目

> 项目路径：`D:\project\python_release\IOS_software_design`
> 核心目标：将 CAE A320 Neo IOS 教员台用户手册翻译、拆解、结构化为中文开发文档，并以 HTML 形式可视化输出。

---

## 1. 目录结构

```
IOS_software_design/
├── docs/                # 设计文档与开发规范（已按阅读顺序编号）
│   ├── 1_需求描述与工作计划.md
│   ├── 2_A320_与_原始手册_章节映射表.md
│   ├── 3_HTML生成规范与转换规则.md
│   ├── 4_第2章设计草案.md
│   └── 5_IOS工作区架构抽象逻辑分析.html
├── output/              # 最终产物输出目录
│   └── html/            # HTML 可视化页面
│       ├── build.py     # HTML 构建脚本（自动生成导航、面包屑、active 高亮）
│       ├── template.html # 公共骨架模板（head + sidebar 占位 + content 占位）
│       ├── pages/       # 页面片段（源文件）：style + 正文 + script
│       │   ├── ch1_1_components.html
│       │   ├── ch1_2_1_lesson_plan_tab.html
│       │   └── ...      # （新增页面只需在此创建片段，运行 build.py 即可）
│       ├── ch1_1_components.html   # 生成产物（由 build.py 自动产出，禁止手动修改）
│       ├── ch1_2_1_lesson_plan_tab.html
│       ├── ch1_2_2_doc_tab.html
│       ├── ch1_2_3_current_conditions_tab.html
│       ├── ch1_2_4_aircraft_tab.html
│       ├── ch1_2_5_reference_airport_tab.html
│       ├── ch1_2_6_instructor_station_panel.html
│       ├── ch1_2_7_control_board_footer.html
│       ├── ch1_3_maintenance_pages.html
│       ├── ch1_4_instrument_repeater.html
│       ├── ch1_5_lesson_plan_profile.html
│       ├── ch1_6_map_workspace.html
│       ├── ch1_7_advanced.html
│       ├── ch1_8_reference_flows.html
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

1. **`docs/1_需求描述与工作计划.md`**
   - 了解项目背景、原始资料位置、双文档对照逻辑、工作节奏。

2. **`docs/3_HTML生成规范与转换规则.md`** ⭐ **必读（构建机制已变更）**
   - **第 2 章「HTML 构建架构」**：理解 `pages/` + `template.html` + `build.py` 的新工作流，严禁回到旧的内联硬编码 sidebar 模式
   - 了解文件输出路径、图片处理规则、HTML 结构模板、内容红线、Checklist

3. **`docs/2_A320_与_原始手册_章节映射表.md`**
   - 了解 A320.md 章节与原始手册章节的对应关系，确认目标章节的精确层级归属。

4. **`output/html/ch1_1_components.html`**（⭐ 架构设计与领域建模必读）
   - **1.1.1 ~ 1.1.3**：理解 IOS 六大工作区的组成定义、UI 控件体系与参数输入范式。
   - **1.1.4 ~ 1.1.11**：理解六大工作区背后的架构抽象逻辑——关注点分离、领域建模、认知心理学逻辑、数据流与单一事实来源约束、状态一致性设计原则。
   - 在进行第 2 章软件架构设计、接口拆分、状态管理设计前，必须优先阅读，确保新增模块与现有架构一致。

5. **`docs/4_第2章设计草案.md`**
   - 在开始第 2 章（软件架构与交互设计）前阅读，了解已确定的架构方向、模块边界与待决策点。

6. **`reference/A320.md`**
   - 定位到当前待处理的章节，提取已整理的功能描述作为内容锚点。

5. **`reference/CAE IOS使用手册.md`（或 `_zh.md`）**
   - 作为结构校验器，确认功能点的上级菜单、同级并列关系与嵌套逻辑。

---

## 3. 当前进度

### 已完成（第 1 章 — 软件操作）

| 章节 | A320.md 标题 | 原始手册对应 | 状态 |
|------|-------------|-------------|------|
| 1.1 | 组成部分（含架构分析） | ## 3.1 IOS Workspaces + ## 3.2 UI Controls + docs/5 架构推演 | ✅ V2.0 已完成（组成部分 + 架构抽象逻辑分析合并） |
| 1.2.1 | 课程计划选项卡（LESSON PLAN） | ## 5. LESSON PLAN Tab | ✅ 已完成 |
| 1.2.2 | 文档选项卡（DOCS） | ## 6. DOCS Tab | ✅ 已完成 |
| 1.2.3 | 当前条件选项卡（CURRENT CONDITIONS） | ## 7. CURRENT CONDITIONS Tab | ✅ 已完成 |
| 1.2.4 | 飞机/航空器选项卡（AIRCRAFT） | ## 8. AIRCRAFT Tab | ✅ 已完成 |
| 1.2.5 | 参考机场选项卡（REFERENCE AIRPORT） | ## 9. REFERENCE AIRPORT Tab | ✅ 已完成 |
| 1.2.6 | 教员台滑动面板（INSTRUCTOR STATION Sliding Panel） | ## 10. INSTRUCTOR STATION Sliding Panel | ✅ 已完成 |
| 1.2.7 | 控制面板底部（Footer） | ## 11. Control Board Footer | ✅ 已完成 |
| 1.3 | 维护页面（Maintenance Pages） | ## 12. Maintenance Pages | ✅ 已完成 |
| 1.4 | 仪表复示器工作区（INSTRUMENT REPEATER） | ## 13. INSTRUMENT REPEATER Workspace | ✅ 已完成 |
| 1.5 | 课程计划配置工作区（Lesson Plan Profile） | ## 14. Lesson Plan Profile Workspace | ✅ 已完成 |
| 1.6 | 地图工作区（Map） | ## 15. Map Workspace | ✅ 已完成 |
| 1.7 | 高级（Advanced） | ## 16. Advanced | ⚠️ 初版已完成，内容待优化 |
| 1.8 | 参考流程（Reference Flows） | 无直接对应（基于 1.1~1.7 整合创作） | ✅ 内容已合并至 1.1（ch1_1_components.html） |

### 已完成设计文档

| 文档 | 说明 | 状态 |
|------|------|------|
| `docs/4_第2章设计草案.md` | 第 2 章软件架构与交互设计的设计草案 | ✅ 已创建 |
| `docs/5_IOS工作区架构抽象逻辑分析.html` | 基于原始手册的六大工作区架构推演与领域建模分析 | ✅ 已创建（内容已合并至 ch1_1） |

### 待处理

| 章节 | A320.md 标题 | 原始手册对应 | 状态 |
|------|-------------|-------------|------|
| 2 | 软件架构与交互设计（逆向推导） | 无直接对应 | 🔜 待启动（设计草案阶段） |
| 4~10 | 开发设计章节 | 无直接对应 | 🔜 待填充 |

---

## 4. 快速启动指令模板

用户可以在新会话中直接使用以下指令：

> **"请阅读项目 docs 目录和 README.md，继续转换下一章节的 HTML。"**

Claude 将自动：
1. 阅读本 `README.md` 了解项目结构与当前进度。
2. 按顺序阅读 `docs/` 下的三份规范文档：`1_需求描述与工作计划.md` → `2_A320_与_原始手册_章节映射表.md` → `3_HTML生成规范与转换规则.md`。
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
| 2026-06-03 | V0.4 | 完成 2.2.5 章节（参考机场选项卡），涵盖 14 组参数字段、机场与重新定位滑动面板（4 选项卡）、时刻/地面风/能见度/降水/云层/温度/ISA/QNH/风切变/跑道状况等全部子面板，配套 27 张截图，含 Redline Review |
| 2026-06-05 | V0.5 | 完成 2.3 章节（维护页面），生成 `ch1_3_maintenance_pages.html`，配套原始手册 Figure 108 截图；同步更新 README 进度与所有历史 HTML 的侧边栏导航 |
| 2026-06-05 | V0.6 | 完成 2.5 章节（课程计划配置工作区），生成 `ch1_5_lesson_plan_profile.html`，配套原始手册 Figure 110~116 共 10 张截图；包含画布视图、列表视图、时间线/时间区域、6 组按钮的完整功能详解；附课程执行通用状态机与数据流推导；Redline Review 修复 Mermaid 语法违规 2 处；回溯更新 9 个历史 HTML 文件的侧边栏导航与页脚链接 |
| 2026-06-05 | V0.7 | 完成 2.6 章节（地图工作区），生成 `ch1_6_map_workspace.html`，完整覆盖地图标题栏、主区域（图标/径向菜单）、右侧工具栏（7 项功能）、地图页脚（左/中/右三段）；包含风暴属性滑动面板详述、子流程图、状态机、测试要点；配套原始手册 Figure 111~143 共 35 张截图；回溯更新 10 个历史 HTML 文件的侧边栏导航与页脚链接 |
| 2026-06-05 | V0.8 | 完成 2.7 章节（高级）初版，生成 `ch1_7_advanced.html`。涵盖飞机、位置、环境（天气区域/灯光/机场视觉效果）、入侵者（TCAS/随机/进近/ITP）、通信（ATIS/ATC）、故障、UPRT、重置/冻结、录制共 10 大子模块；复用章节采用引用而非重复详述；配套原始手册 Figure 144~183 共 36 张截图；含参数设置通用状态机、六分支操作流程图、数据流与 API 契约推导；Redline Review 修复 flowchart transition label 斜杠违规；回溯更新 11 个历史 HTML 文件的侧边栏导航。<br><br>**⚠️ 注意：2.7 章节 HTML 内容仅为初版生成，尚未经过深度内容优化（如字段解释精确化、交互逻辑补全、截图标注对齐等），后续需专门迭代。** |
