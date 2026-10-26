---
name: math-pdf-translator
description: Translate formula-heavy academic papers, book chapters, or monographs into complete faithful Chinese LaTeX/PDF with mandatory nature-reader source routing, source-page mapping, equation and figure preservation, terminology control, ElegantBook/ElegantPaper template selection for new projects, staged model execution, compilation, and page-by-page visual QA. Use for 数学书籍翻译、最优控制教材翻译、公式密集论文全文翻译、章节重译或不准确译稿的系统重做；do not use for short sentence translation, summaries, or prose-only localization.
metadata:
  short-description: 公式密集文献的完整中文 LaTeX 翻译与逐页验收
---

# Math PDF Translator

把数学、控制、动力系统及其他公式密集型 PDF 忠实翻译为可编译、可追溯的中文 LaTeX。目标是完整译本，不是摘要、学习提纲或解释性改写。

## 发布包依赖定位

本发布包把 `nature-reader`、`nature-shared`、`elegantpaper-master`、`elegantbook-master` 和轻量 `pdf` 支持技能放在同一技能根目录。优先按宿主技能目录定位；没有目录索引时，在本技能的同级目录查找。已有宿主 `pdf` 技能可继续使用，记录实际加载文件的路径和指纹。缺少必需依赖时先指出缺失项，不得跳过约束加载或声称完成验收。

主文件默认按作者、年份与主题命名为 `AuthorYear_keyword_cn.tex`，生成同名 PDF；仅在用户或现有项目要求时使用 `main.tex`。参考文献的呈现遵从用户要求，正文引用必须保持可追溯。

## 首要约束

- 以用户指定的源 PDF 为唯一内容权威；已有译文只能用于发现问题，不能替代原文核对。
- 完整忠实直译：不删减、不合并实质段落、不补写总结；保留论证顺序、限定条件、例题、练习、脚注、图注和章末注记。
- 数学符号、变量、编号、转置、星号、导数、积分上下限、分段条件和 Hessian 分块必须逐项核对，不根据上下文猜测。
- 先确定授权修改范围；不顺带改主文件、模板类、参考文献库或其他章节，除非用户明确要求。
- 覆盖清单只有在源文、译文和最终渲染三重核对后才能标记为完成。

## 约束加载与任务级复用

本节所称“一个翻译任务”，是从确定同一源文与交付范围开始，到该范围完成最终验收为止。分节补丁、阶段切换、失败重试、续写、重新裁图、重新编译和验收修复都属于同一任务，不得据此重复加载整套约束。

每个翻译任务必须由协调主代理实际完整读取并应用一次 `nature-reader`，不得只凭记忆复述其原则：

1. 定位并完整读取 `nature-reader/SKILL.md`、同目录 `manifest.yaml` 及 `always_load` 中列出的全部文件。
2. 判定 `pdf-text`、`scanned-pdf`、`html`、`doi-arxiv` 或 `pasted-text`，只读取命中的源格式片段。DOI/arXiv 解析为另一种载体时，按解析链读取最终命中的片段。
3. 源文含公式时读取 `references/equation-handling.md`；涉及图表时读取 `references/figure-extraction.md`。
4. 输入为 PDF 时完整读取 `pdf` 技能，并在首次处理 PDF 前遵守其提取、渲染和验证要求。
5. 为实际加载的文件记录路径与 SHA-256 指纹，并生成一份紧凑、结构化的 `translation_constraint_packet`。字段与失效条件见 [references/workflow.md](references/workflow.md)。

Sol 规划代理、Luna 执行代理和主代理后续验收均复用该约束包。在同一任务内，只要文件指纹、源格式、文档类型、模板模式和交付形式未变化，下游代理不得重新读取 `nature-reader` 的入口、manifest、`always_load` 或已经纳入约束包的按需参考文件；阶段恢复时也只读取约束包、当前源页和工作文件。

仅在以下情况重新读取受影响的原始约束：用户改变交付形式，源格式或模板模式改变，文件指纹变化，约束包没有覆盖新出现的对象类型，或者 QA 表明错误可能来自约束遗漏。只重载受影响部分；不要无条件重载全部文件。

开始处理前只需一次性向用户报告 `source_format`。覆盖清单记录加载者、任务级加载范围、文件指纹、约束包字段、复用角色和任何失效事件；未完成首次加载和约束包构建不得进入规划或正文写入。

`nature-reader` 在本流程中负责源提取、源映射、术语账本、公式置信度和图表裁剪约束。其默认双语 Markdown 输出契约不覆盖本技能的主交付：除非用户明确要求双语 reader，否则主交付仍是完整中文 LaTeX/PDF、覆盖清单和翻译说明，不强制生成 `paper.md`。若用户明确要求双语 reader，则把 `paper.md`、`source_map.json` 等作为附加交付，并完整执行 `nature-reader` 的输出验证。

## 文档与模板路由

先判定 `document_kind`，再决定模板：

- 教材、专著、书籍章节、长篇讲义和学位论文式长文：新建项目必须由协调主代理完整读取并使用 `elegantbook-master`，采用 ElegantBook；其他角色复用约束包中的模板不变量。
- 期刊论文、会议论文、预印本、working paper 和短篇学术报告：新建项目必须由协调主代理完整读取并使用 `elegantpaper-master`，采用 ElegantPaper；其他角色复用约束包中的模板不变量。
- 类型不明确时，先根据封面、目录、章节层级、出版信息和篇幅判断；仍无法可靠判断时再询问用户。
- 已有 LaTeX 项目始终保留当前 `\documentclass`，不得自动迁移模板。先从实际入口文件、类文件、目录结构和一次基线编译提取模板不变量并写入约束包；若现有类是 ElegantBook 或 ElegantPaper，默认直接原地继续，不重复完整读取对应 Master。只有模板结构不完整、编译异常涉及模板、用户要求迁移，或约束包无法确定所需模板行为时，才读取对应 Master。其他模板保持原类且不复制 Elegant 模板文件。
- 用户明确指定模板或文档类时，以用户指令为准。

把 `document_kind`、模板模式（`new_elegantbook`、`new_elegantpaper` 或 `preserve_existing`）、现有项目判定、最终文档类、模板不变量来源和实际加载的 Master 技能记录到覆盖清单。

## 模型路由

用户指定模型时严格遵从。未指定且相应模型可用时，默认采用：

1. `gpt-5.6-sol` 只读规划：核准页码、结构、对象计数、风险公式、术语和分段边界，不修改交付文件。
2. `gpt-5.6-luna`、`max` 执行：作为唯一正文写入者，按分节补丁翻译、裁图和编译。
3. 主代理独立验收：不以执行代理的自报结果代替检查，独立核对计数、日志、页界和全部渲染页；发现问题交回同一 Luna 执行代理修复。

如果协作代理或指定模型不可用，由当前最强可用模型执行同一流程，并在开始前说明实际路由。不要让用户手动切换模型。一个阶段只能有一个正文写入者，避免并发覆盖。

## 工作入口

1. 完成首次任务级约束加载，生成 `translation_constraint_packet`，记录 `source_format`、文件指纹、按需参考文件、PDF 技能加载状态和复用角色。
2. 完整阅读项目的 `AGENTS.md` 及目标 LaTeX 文件，判定 `document_kind`、新建/已有项目和模板模式，确认现有术语、符号和环境。
3. 对 PDF 优先尝试文本抽取；仅在无文本层、乱码或扫描页时使用 OCR，并以渲染页复核版面。
4. 在编辑前建立源清单：印刷页与 PDF 物理页、章节层级、编号公式、图、表、例题、练习、定理、引理、脚注和文献键。
5. 旧译问题呈系统性时整段或整章重建；仅在问题局部且可证明边界清楚时做局部修补。
6. 先建立全部为 `pending` 的覆盖记录，再按自然小节分阶段执行。

协调主代理和 Sol 规划阶段读取 [references/workflow.md](references/workflow.md)。创建或更新覆盖文件的角色才读取 [references/coverage-schema.md](references/coverage-schema.md)。主代理最终验收时读取 [references/qa-checklist.md](references/qa-checklist.md)。Luna 已收到完整阶段计划和约束包时不重复读取这三个参考文件；只有信息缺失或失效条件触发时才读取相关文件。

## 分阶段执行规则

每个阶段必须形成闭环：

1. 对照该阶段所有源页翻译，不借用旧中文填空。
2. 保持公式编号和稳定标签；未经源文支持不新增标题或解释。
3. 图像复用前先检查；不合格时从源 PDF 紧裁，只保留图形和图内必要标记，中文图注留在 LaTeX。
4. 更新该阶段覆盖状态为 `translated_checked_pending_render`。
5. 运行一次快速 XeLaTeX 编译，修复本阶段新增错误后再进入下一阶段。

长章节应按 `section` 或连续 `subsection` 分补丁，避免一次性写入截断。跨页对象可在覆盖记录中暂记为 `partial_translated_checked_pending_render`，相邻阶段完成后必须消除所有 `partial`。

## 公式、图片与术语

- 编号公式使用项目稳定标签，例如 `eq:4.1`；多行单编号公式使用 `equation` 配合 `aligned` 或 `split`。
- 禁止遗留弃用结构，如可由 `pmatrix`、`cases` 或标准 AMS 环境替代的 `\atop`。
- 图片命名和目录遵循项目现状；重裁时记录源 PDF 页、裁剪状态及图注标签。
- 术语表优先于临时译法。新术语只在确有必要时补入，避免同义词漂移。
- 若源文自身存在矛盾，忠实保留原文并在翻译说明中记录，不静默“修正”。

## 最终交付

正文完成后：

1. 运行程序化结构审计；可使用 [scripts/audit_latex_chapter.ps1](scripts/audit_latex_chapter.ps1)。
2. 执行 `xelatex → biber → xelatex → xelatex`，审计日志并区分既有警告与本次新增警告。
3. 确定译文在最终 PDF 中的准确页范围，渲染并检查全部页面，而不是只抽查首页。
4. 检查公式、定理、脚注和图像是否截断，图片是否混入英文页眉、正文或图注，章节页界是否漂移。
5. 修复后重新编译和复查；仅在全部通过后将覆盖状态更新为 `complete_verified`。

至少交付：目标 `.tex`、最终 PDF、翻译说明、逐页覆盖清单，以及任务需要的图片和术语表更新。最终回复须说明源页范围、实际结构计数、最终 PDF 页范围、编译结果、视觉检查页数和任何仍未解决的不确定项。
