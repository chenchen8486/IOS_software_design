# HTML 生成规范与转换规则

> 基于 2.2.1（LESSON PLAN Tab）和 2.2.2（DOC Tab）的生成实践整理。
> 目标：确保后续所有章节的 HTML 输出在结构、风格、准确性上保持一致。
> 整理时间：2026-05-30

---

## 1. 文件输出路径规则

| 文件类型 | 输出路径 | 说明 |
|----------|----------|------|
| HTML 页面 | `output/html/ch{章}_{节}_{小节}_{english_title}.html` | 与细化 MD 同目录、同名 |
| 细化 MD | `output/html/ch{章}_{节}_{小节}_{english_title}.md` | 与 HTML 同目录输出，不再使用 `docs/refined/` |
| 配图资源 | `output/html/images/` | 所有配图统一归集到此处，HTML 内引用 `./images/xxx.jpg` |

**禁止事项：**
- 禁止在根目录创建分散的图片或缓存目录
- 禁止把细化 MD 单独放到 `docs/refined/` 等中间目录
- 禁止把 HTML 和 MD 分开放

---

## 2. 图片处理规则

### 2.1 自动查找，禁止手动占位
- HTML 中**不允许**出现 `[图片占位]` 提示
- 自动从以下两个来源查找配图：
  1. 版面分析 MD（`reference/CAE IOS使用手册.md`）中的图片引用
  2. 图片库（`reference/images/`）
- 找到后自动复制到 `output/html/images/`，并生成正确的相对路径引用

### 2.2 格式与命名
- **保留原始扩展名**（通常是 `.jpg`），不要强行改为 `.png`
- HTML 中引用格式：`<img src="./images/xxx.jpg" alt="描述">`
- 图片命名规范：`ch{章}_{节}_{小节}_{描述}.jpg`

### 2.3 onerror 占位处理
- 生成 HTML 时直接写入本地图片路径
- 删除所有 `onerror="this.parentElement.innerHTML='...'"` 的占位回退代码

---

## 3. HTML 页面结构模板

每个 HTML 页面必须包含以下九大章节（根据章节内容适当取舍）：

```
一、功能总览
  ├─ 1.1 功能层级结构（Mermaid graph TD）
  └─ 1.2 核心操作流程（Mermaid flowchart LR）

二、界面结构
  └─ 表格：区域/控件 | 位置 | 功能说明

三、核心功能详解
  └─ 3.x 各功能点（每个功能点配原始截图 + 属性表格）

四、状态机/流程图（Mermaid stateDiagram-v2 或流程图）

五、关联依赖与异常边界
  ├─ 5.1 关联依赖表格
  └─ 5.2 异常边界表格

六、数据流与开发流程推导
  ├─ 6.1 数据流（代码块或流程图）
  └─ 6.2 API 接口契约建议表格

七、测试要点
  └─ 测试场景表格

八、变更记录
  └─ 日期 | 版本 | 变更内容
```

**页面框架（head + nav + main + footer）：**
- 标题：`<title>章节号 中文标题（英文标题）— CAE IOS 教员台</title>`
- 面包屑：首页 / 第 X 章 / X.X 节 / 当前小节
- 侧边栏导航：完整第2章层级树，当前页面 `active`
- 页脚导航：`prev` ← 上一小节 | 下一小节 → `next`

---

## 4. 内容准确性红线

### 4.1 禁止编造
- **严禁**在表格中写入原始文档（A320.md / CAE IOS使用手册.md）没有明确提及的信息
- 例如：界面分区位置、按钮的具体像素坐标、未在原文中出现的控件名称
- 如果原始文档没有描述某个信息，**宁可写"待确认"或删除该行，也不要猜测**

### 4.2 位置描述必须基于截图
- "二、界面结构"表格中的**位置列**必须基于实际截图分析
- 生成前先用浏览器打开 HTML 或原图，**逐按钮核对后再填写位置**
- 禁止凭"通用文档阅读器布局"脑补位置（如"底部导航栏""右下角缩放"）

### 4.3 互斥功能不要独立成章
- 如果两个功能只是按钮互斥（如缩略图视图 vs 列表视图），**不要为"切换逻辑"单独创建章节**
- 互斥关系在各自功能的属性表格中用一句话说明即可：
  - `与列表视图**互斥**，两者只能激活其一`
- 不要画独立的 Mermaid 图来讲"切换逻辑"

### 4.4 Mermaid 图禁用 Emoji 图标
- Mermaid 节点内**只使用纯文字**，禁止放入 Emoji（如 🔍、🖼️、⛶）
- Emoji 容易与实际 UI 图标不一致，造成误导
- 允许使用文字描述 + 颜色填充（`style`）来区分节点类型

---

## 5. 导航与层级规范

### 5.1 侧边栏结构
- 有子章节的父节点必须用 `nav-group` + `nav-toggle` + `nav-children` 包裹
- 确保同级子章节（如 2.1.1 和 2.2.1）的缩进层级完全一致
- 默认状态：当前章节展开，其他同级章节折叠（`collapsed`）

### 5.2 当前页面标记
- 当前页面对应的 `nav-link` 必须有 `class="nav-link active"`
- 面包屑最后一项为纯文本（不加链接）

### 5.3 页脚导航
- `prev`：指向上一小节 HTML（如 2.2.2 的 prev 是 2.2.1）
- `next`：指向下一小节 HTML（如 2.2.2 的 next 是 2.2.3，若未生成为 `#` 占位）

---

## 6. 表格样式规范

### 6.1 "二、界面结构"表格
| 列 | 要求 |
|----|------|
| 区域/控件 | 中文名称 + 英文名称（br换行） |
| 位置 | 必须基于截图，如"顶部工具栏（最左侧）" |
| 功能说明 | 简明扼要，一句话概括 |

### 6.2 "核心功能详解"属性表格
| 属性 | 说明 |
|------|------|
| 功能定义 | 一句话定义 |
| 呈现方式/交互方式 | 如何展示、如何操作 |
| 边界行为/边界条件 | 极限状态下的行为 |
| 与其他功能关系 | **互斥/依赖/联动关系一句话说明** |

---

## 7. 测试要点定位

- 测试要点是**给后续开发和测试验收准备的验收标准（Acceptance Criteria）**
- 包含：正向路径、异常路径、边界条件、联动测试、性能测试
- 如果用户希望更"纯粹"（只保留面向教员的内容），可折叠或移至独立测试文档

---

## 8. Git 提交规范

```
[新增]: 生成2.2.x xxx细化MD与HTML，自动匹配图片资源
[修正]: 对照图1实际截图校正2.2.x界面结构位置描述
[修复]: 修正侧边栏导航层级对齐问题
```

- Commit 使用中文
- 正文列出具体变更点
- 结尾固定格式：`Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

---

## 9. 执行 Checklist（每次生成前自检）

- [ ] 已读取 A320.md 对应章节原始内容
- [ ] 已读取 `CAE IOS使用手册.md` 对应章节的图片引用
- [ ] 图片已自动从图片库复制到 `output/html/images/`
- [ ] HTML 中无 `[图片占位]`，图片路径为 `./images/xxx.jpg`
- [ ] "二、界面结构"的位置描述基于实际截图，非脑补
- [ ] Mermaid 图中无 Emoji 图标
- [ ] 互斥功能未独立成章，仅在表格中一句话说明
- [ ] 侧边栏层级对齐，当前页面 `active`
- [ ] 页脚 prev/next 链接正确
- [ ] 细化 MD 与 HTML 同目录输出

---

## 十、Mermaid 图表交互规范（点击放大 / 滚轮缩放 / 拖拽平移）

### 10.1 需求背景

Mermaid.js 在 HTML 中渲染的 SVG 流程图尺寸受限于正文容器宽度，复杂结构图（如功能层级结构、核心操作流程）在页面上显示过小，无法看清节点文字与连线细节。因此所有 HTML 页面的 Mermaid 图表必须支持**点击放大、滚轮缩放、按住拖拽**的交互能力。

**核心约束**：本项目 HTML 文件通常在 `file://` 协议下直接双击打开（本地离线浏览），**严禁触发浏览器的同源安全（CORS）错误**。

### 10.2 方案演进与踩坑记录

| 轮次 | 方案 | 结果 | 失败原因 |
|------|------|------|----------|
| 1 | 模态框 + `innerHTML` 复制 SVG | ❌ 报错 | `file://` 协议下，`innerHTML` 序列化含 `<foreignObject>` 的 SVG 会触发 `Unsafe attempt to load URL` frame 同源阻断 |
| 2 | 模态框 + `cloneNode(true)` 克隆 SVG | ❌ 报错 | 同上，Mermaid SVG 内部包含 `<foreignObject>` 元素，DOM 克隆后仍触发 frame 安全限制 |
| 3 | 模态框 + `Blob URL` + `<img>` 加载 | ❌ 显示小方块 | `URL.createObjectURL()` 生成的 blob URL 在 `file://` 协议下被浏览器阻止加载，图片无法渲染 |
| **4** | **CSS 直接放大原始 `.mermaid` 元素** | ✅ 通过 | **不创建新 DOM 节点、不克隆 SVG、不生成任何 URL**，仅给现有元素添加 CSS 类切换 `position: fixed` + `transform` |

**结论**：在 `file://` 协议下，任何涉及"创建新 DOM 节点并复制/引用 SVG 内容"的方案都会踩到同源安全限制。**唯一可行路线是纯粹 CSS 状态切换**。

### 10.3 最终实现（定稿，所有 HTML 统一复用）

**交互行为**：
1. **点击图表** → 原始 `.mermaid` 元素切换为 `position: fixed`，居中放大至 `90vw × 90vh`
2. **滚轮滚动** → 图表内部 SVG 通过 `transform: scale()` 平滑缩放（范围 `0.3x ~ 5x`）
3. **按住鼠标左键拖动** → SVG 通过 `transform: translate()` 平移，实现 Pan 浏览
4. **点击黑色遮罩层** 或按 **ESC** → 移除放大状态，恢复原状

**CSS 核心**：

```css
/* 遮罩层 */
.mermaid-zoom-overlay {
  position: fixed; inset: 0;
  background: rgba(15,23,42,0.85);
  z-index: 999; backdrop-filter: blur(4px);
  cursor: zoom-out;
}

/* 放大状态：直接作用于原始 .mermaid 容器 */
.mermaid.is-zoomed {
  position: fixed !important;
  top: 50% !important; left: 50% !important;
  transform: translate(-50%,-50%) !important;
  z-index: 1000 !important;
  width: 90vw !important; height: 90vh !important;
  max-width: none !important;
  background: var(--surface) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25) !important;
  padding: 0 !important;
  overflow: hidden !important;
  cursor: grab !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  user-select: none;
}
.mermaid.is-zoomed:active { cursor: grabbing !important; }
.mermaid.is-zoomed svg {
  transition: transform .1s ease-out;
  transform-origin: center center;
  max-width: none !important;
}
```

**JavaScript 核心**：

```javascript
// Mermaid 图表点击放大与交互功能 (缩放/拖拽)
(function(){
  let currentScale=1;
  let isDragging=false;
  let startX, startY, translateX=0, translateY=0;

  function closeZoom(el){
    el.classList.remove('is-zoomed');
    const svg=el.querySelector('svg');
    if(svg){svg.style.transform='';svg.style.transition='';}
    const overlay=document.querySelector('.mermaid-zoom-overlay');
    if(overlay) overlay.remove();
  }

  function updateTransform(svg){
    if(svg) svg.style.transform=`translate(${translateX}px,${translateY}px) scale(${currentScale})`;
  }

  // 1. 点击放大 / 点击遮罩关闭
  document.addEventListener('click', function(e){
    const zoomed = document.querySelector('.mermaid.is-zoomed');
    if(zoomed && e.target.classList.contains('mermaid-zoom-overlay')){
      closeZoom(zoomed);
      return;
    }
    const mermaidEl = e.target.closest('.mermaid:not(.is-zoomed)');
    if(mermaidEl){
      const overlay = document.createElement('div');
      overlay.className = 'mermaid-zoom-overlay';
      document.body.appendChild(overlay);
      mermaidEl.classList.add('is-zoomed');
      currentScale = 1;
      translateX = 0;
      translateY = 0;
      updateTransform(mermaidEl.querySelector('svg'));
    }
  });

  // 2. ESC 关闭
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){
      const zoomed = document.querySelector('.mermaid.is-zoomed');
      if(zoomed) closeZoom(zoomed);
    }
  });

  // 3. 滚轮缩放（必须 {passive:false} 才能 preventDefault）
  document.addEventListener('wheel', function(e){
    const zoomed = document.querySelector('.mermaid.is-zoomed');
    if(!zoomed) return;
    e.preventDefault();
    const svg = zoomed.querySelector('svg');
    if(!svg) return;
    const delta = e.deltaY < 0 ? 0.1 : -0.1;
    currentScale += delta;
    currentScale = Math.max(0.3, Math.min(currentScale, 5));
    updateTransform(svg);
  }, {passive: false});

  // 4. 鼠标拖拽平移
  document.addEventListener('mousedown', function(e){
    const zoomed = document.querySelector('.mermaid.is-zoomed');
    if(zoomed && e.target.closest('.mermaid.is-zoomed')){
      isDragging = true;
      startX = e.clientX - translateX;
      startY = e.clientY - translateY;
    }
  });

  document.addEventListener('mousemove', function(e){
    if(!isDragging) return;
    const zoomed = document.querySelector('.mermaid.is-zoomed');
    if(zoomed){
      translateX = e.clientX - startX;
      translateY = e.clientY - startY;
      const svg = zoomed.querySelector('svg');
      if(svg){svg.style.transition = 'none'; updateTransform(svg);}
    }
  });

  document.addEventListener('mouseup', function(){
    isDragging = false;
    const zoomed = document.querySelector('.mermaid.is-zoomed');
    if(zoomed){
      const svg = zoomed.querySelector('svg');
      if(svg) svg.style.transition = 'transform .1s ease-out';
    }
  });
})();
```

**关键实现要点**：
- **事件委托**：使用 `document.addEventListener('click', ...)` 而非逐个元素绑定，规避 Mermaid 异步渲染时机问题
- **passive: false**：滚轮事件必须显式声明，否则 `preventDefault()` 无效，页面会随滚轮一起滚动
- **不创建新节点**：全程只操作现有 `.mermaid` 元素和遮罩层 `div`，不触碰 SVG 内部结构
- **transform 叠加**：通过 `translate(x,y) scale(s)` 矩阵实现 Pan + Zoom 的组合变换

### 10.4 已应用文件

- `output/html/ch2_2_1_lesson_plan_tab.html`
- `output/html/ch2_2_2_doc_tab.html`
- `output/html/ch2_2_3_current_conditions_tab.html`

**后续生成的所有 HTML 文件必须复用上述同一套 CSS + JS**，保持交互体验一致。

---

## 十一、变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-05-30 | V1.0 | 基于 2.2.1、2.2.2 生成实践，整理 HTML 生成规范与转换规则 |
| 2026-06-01 | V1.1 | 新增第 10 章：Mermaid 图表交互规范（点击放大 / 滚轮缩放 / 拖拽平移），记录方案演进与踩坑指南 |
