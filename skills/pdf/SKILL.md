---
name: pdf
description: Extract, render, and inspect PDFs for the math-pdf-translator bundle. Use for source-page reading, formula and figure verification, and final rendered-page QA; use OCR only when the text layer is absent or unusable.
---

# PDF 提取、渲染与核对

本目录是本发布包提供的轻量 PDF 支持技能。已有宿主 PDF 技能可继续使用；记录实际加载路径和指纹，不要覆盖宿主配置。

## 读取源文

1. 用 `pdfinfo` 确认物理页数、页面尺寸和文档信息；记录 PDF 的 SHA-256。物理页从 1 计数，印刷页另设字段。
2. 先运行 `pdftotext -layout source.pdf source.txt`。也可用 `pypdf` 或 `pdfplumber` 提取文本和页内位置。保留分页边界；禁止凭提取顺序猜测多栏段落顺序。
3. 用 `pdftoppm -png -r 150 source.pdf source-page` 渲染源页。公式、上下标、矩阵、图表和脚注必须结合图像检查；文本抽取成功不能替代查看页面。
4. 无文本层、严重乱码或扫描页才使用可用 OCR。OCR 只生成候选文本；逐项对照源页核准数学符号、数字和引用，无法辨认处记录待核对，禁止补猜。
5. 原图可用时保留其内容；裁剪仅去除图外正文和多余留白，保留坐标轴、图例、比例尺、子图编号。图注在 LaTeX 中翻译并与原图映射。

## 编译后验收

1. 检查编译日志中的错误、缺字、未解析引用和溢出版心。完整编译链由主翻译技能和实际项目决定。
2. 对最终 PDF 再运行 `pdfinfo` 和 `pdftotext -layout`，核查完整性、公式编号、图表引用及中文可搜索性。
3. 渲染并实际查看最终 PDF 的每一页，核查公式断行、图表裁切、图注归属、页边界和缺字；记录逐页结果。修改后重查受影响页，最终页数变化时更新覆盖记录。
4. 只有源文覆盖、编译、引用和全部最终页面检查通过，才允许主流程标记 `complete_verified`。缺少工具或未查看页面时明确记录未完成项。

Python 包仅辅助提取；Poppler 与 TeX 需单独安装。扫描 OCR 工具按源文需要选择，本发布包不自动下载或执行 OCR 服务。
