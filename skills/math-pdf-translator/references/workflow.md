# 完整翻译工作流

## 1. 任务级加载约束并判定输入

由协调主代理在任何规划或翻译前完成以下只读步骤，每个翻译任务只执行一次：

1. 完整读取 `nature-reader/SKILL.md` 和 `manifest.yaml`，再读取清单中 `always_load` 的全部核心文件。
2. 判定并记录 `source_format`：`pdf-text`、`scanned-pdf`、`html`、`doi-arxiv` 或 `pasted-text`；只加载命中的格式片段。复合来源按解析链依次加载。
3. 只要源文含公式，就读取 `nature-reader/references/equation-handling.md`；只要涉及图表，就读取 `nature-reader/references/figure-extraction.md`。
4. PDF 输入还必须完整读取 `pdf` 技能，并在首次处理前遵守其提取、渲染与验证规则。
5. 对实际读取的文件计算 SHA-256，记录技能入口、核心文件、格式片段、按需参考文件和加载者。不得写成“已吸收原则”或依靠先前任务记忆代替本次读取。

向用户简短报告一次判定的 `source_format`，使其可在处理开始前纠正。同一任务的分节、续写、重试、编译或验收修复不得再次执行整套加载。

### 1.1 构建执行约束包

首次加载完成后，协调主代理生成紧凑的 `translation_constraint_packet`，至少包含：

```yaml
version: 1
source_format: pdf-text
document_kind: book_chapter
delivery: complete_chinese_latex_pdf
template_mode: preserve_existing
fidelity:
  no_omission: true
  no_paragraph_merging: true
  no_summary_substitution: true
  preserve_argument_order: true
equations:
  preserve_numbering: true
  verify_against_rendered_source: true
  unnumbered_display_environment: "\\[...\\]"
figures:
  crop_from_source_pdf: true
  exclude_headers_and_english_captions: true
  preserve_internal_math_labels: true
terminology:
  use_project_glossary: true
verification:
  structural_audit: true
  full_compile_chain: true
  page_by_page_render_qa: true
```

约束包还必须列出实际加载文件及其 SHA-256、模板不变量、项目允许/禁止修改范围、符号约定和当前任务特有的低置信度规则。它是下游代理的执行接口，不替代覆盖清单，也不得省略影响译文完整性、公式保真、图片裁剪或最终验收的约束。

Sol、Luna 和主代理后续步骤均复用同一约束包。阶段恢复只重新读取约束包、当前源页、目标文件和术语表。仅当用户改变交付形式、源格式或模板模式发生变化、文件指纹变化、出现约束包未覆盖的新对象类型，或 QA 指向约束遗漏时，重新读取受影响的原始文件并更新约束包；不得无条件全部重载。

## 2. 判定文档类型与模板

记录 `document_kind`、项目状态和模板模式：

- 新建教材、专著、书籍章节、长篇讲义或学位论文式项目：由协调主代理读取 `elegantbook-master/SKILL.md`，复制其必需模板资源并采用 ElegantBook；其他角色复用约束包。
- 新建期刊论文、会议论文、预印本、working paper 或短篇学术报告：由协调主代理读取 `elegantpaper-master/SKILL.md`，复制其必需模板资源并采用 ElegantPaper；其他角色复用约束包。
- 已有 LaTeX 项目：读取实际入口 `.tex` 的 `\documentclass`，从入口文件、类文件、目录结构和基线编译提取模板不变量。已有 ElegantBook/ElegantPaper 项目默认原地继续，不完整加载 Master；只有模板信息不足、模板相关编译异常或用户要求迁移时才读取对应 Master。其他模板保持原类，不复制或迁移 Elegant 模板。
- 用户明确指定其他模板时覆盖以上默认值。

不要仅凭文件名判断文档类型。类型不明时结合出版信息、目录、章/节结构和篇幅判断；仍有实质歧义才询问用户。

## 3. 范围与源文件盘点

开始编辑前执行只读检查：

- 确认源 PDF、目标 `.tex`、主文件、图片目录、术语表、参考文献库和编译入口。
- 记录目标章节的印刷页、PDF 物理页及二者映射。
- 从原书目录和正文标题分别核对 `chapter`、`section`、`subsection`；发现总数与逐项列表矛盾时，以原书标题逐项计数为准并记录纠正依据。
- 清点编号公式、未编号显示公式、图、表、例题、练习、定理、引理、脚注和文献键。
- 检查现有译稿中的短语断行、乱码、错译、漏译、额外层级、重复块、弃用数学命令和失真覆盖状态。

不要在这个阶段修改文件。先输出可执行的分段计划和硬性验收计数。

## 4. PDF 提取与源页核对

优先使用 `pdftotext -layout` 获取文本层，同时渲染高风险页检查：

- 分式、根号、上下标和积分上下限；
- 点导数、撇号、星号、转置和负号；
- 向量、矩阵、Hessian 分块与分段函数；
- 公式跨页、脚注跨页和图注位置。

文本抽取与渲染冲突时，以页面图像为准。符号仍不确定时，在说明和覆盖记录中标记低置信度，返回原页核查；禁止猜测。

## 5. 源映射与覆盖初始状态

在正文写入前创建覆盖文件：

- 每个源页一条记录，包含印刷页和 PDF 物理页。
- 记录该页涉及的章节锚点、公式、图片、例题、练习、脚注和文献键。
- 顶层和全部页面状态初始化为 `pending`。
- 跨阶段页面或对象可暂时标记 `partial_*`，但最终不允许残留。

翻译说明应记录：范围、对象总数、模型路由、术语与符号约定、阶段边界、图片复用/重裁计划和验收门槛。

## 6. Sol 只读规划

规划代理接收 `translation_constraint_packet`、项目边界和源文件，只做源文核准，不重新加载上游约束，也不写译文：

- 判断旧译是局部可修还是需要重建。
- 给出按自然结构划分的阶段及每段页码、公式和图片范围。
- 标出高风险证明、公式和术语。
- 给出必须复用、必须重裁和需要再次检查的图片。
- 给出允许修改和禁止修改的文件范围。

规划结果必须列出可机器验证的最终计数。总数与逐项列表冲突时应立即重新核算。

## 7. Luna max 唯一写入

执行代理接收 `translation_constraint_packet`、Sol 计划、当前源页和工作文件，按阶段工作；不因阶段切换、续写、重试或编译重新加载上游约束。每完成一段就停止并回报：

1. 逐页对照源文，完整忠实翻译指定范围。
2. 使用 `apply_patch` 修改正文和说明文件。
3. 保留原书章节层级；原书段内粗体提示不得擅自升格为编号标题。
4. 按源文恢复全部公式、例题、练习、脚注、图注和文献键。
5. 重裁指定图片并视觉检查裁界。
6. 更新覆盖状态，但不得提前标记整章完成。
7. 运行一次快速 XeLaTeX；只修复本阶段引入的问题。

主代理在阶段之间执行独立只读检查：目标文件边界、公式标签范围、坏译残留、覆盖状态和编译结果。不得直接把 Luna 的自报计数当作验收证据；发现问题时把修复交回同一 Luna 执行代理。

## 8. 术语和符号一致性

先读取已有术语表及相邻章节。对于最优控制文本，尤其检查：

- maximum principle、Hamiltonian、adjoint、costate；
- transversality condition、target set、terminal cone；
- switching function、bang-bang control、singular arc；
- reachable set、state-transition matrix、control-affine system；
- 正常/异常乘子、极大化/极小化符号约定和终端条件。

相邻章节已确定的 Hamiltonian 符号和协态终端条件不得无故改变。若项目采用与其他教材相反的符号约定，应在说明中明确并全章一致。

## 9. 图片工作流

对每幅现有图片先判断 `reuse` 或 `recrop`：

- `reuse` 仅适用于图形完整、清晰且没有页眉、页码、正文或英文图注残片的图片。
- `recrop` 从指定 PDF 物理页高分辨率渲染后紧裁；保留图内数学标记，不把中文图注写入位图。
- 图片尺寸过小、边缘截断或主体缺失时必须重裁。
- 最终制作图片联系表，检查所有图片裁界和清晰度。

## 10. 输出优先级

本技能的默认主交付是完整中文 LaTeX/PDF、翻译说明和覆盖清单。`nature-reader` 的双语 `paper.md`、`source_map.json`、`translation_notes.md` 和 `assets/` 契约只在用户明确要求双语 reader 时作为附加交付启用；不得因加载 `nature-reader` 而把中文 LaTeX 主交付替换成 Markdown。

即使不生成 `paper.md`，仍须把 `nature-reader` 的源映射、术语账本、公式置信度、低置信度不猜测和图表紧裁规则落实到 LaTeX 工作流、翻译说明和覆盖清单中。

## 11. 最终编译与视觉复核

完整执行：

```text
xelatex
biber
xelatex
xelatex
```

四步均需记录退出码。若项目使用原书方括号文献键而没有 BibTeX 引用，Biber 的无 citekeys 提示可以记录为预期提示，但不得把真实的未定义引用混同为正常情况。

使用 PDF 文本定位译文章节首页、末页和下一章首页，渲染译文全部页面。检查：

- 公式、定理框、练习和脚注是否截断；
- 图像是否清晰且裁剪正确；
- 标题层级、页眉、页码和下一章起始是否正常；
- 是否存在由 `\clearpage`、浮动体或过大图片造成的不必要稀疏页；
- 日志中的 Overfull、float、数学命令、缺字、未定义引用和重复标签是否来自本次译文。

发现问题后最小修复，重新执行完整编译，并复核受影响页面及章节边界。
