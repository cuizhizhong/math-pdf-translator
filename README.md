# math-pdf-translator

将公式密集型论文、书籍章节或专著翻译为**完整、可编辑、可编译、可追溯的中文 LaTeX/PDF** 的 Codex 技能。

适合数学、动力系统、最优控制与生物数学文献。全文翻译保留实质段落、公式、编号、图表及图注；交付覆盖清单，编译后逐页检查。它是工作流程与工具资源，不是独立的机器翻译软件，也不保证模型自动生成的译文正确。

## 安装

需要 Python 3.10+、Git，以及能够加载本地技能的 Codex 环境。下载 [v0.1.0 ZIP](https://github.com/cuizhizhong/math-pdf-translator/archive/refs/tags/v0.1.0.zip) 并解压，或运行：

```sh
git clone https://github.com/cuizhizhong/math-pdf-translator.git
cd math-pdf-translator
python scripts/install.py --dry-run
python scripts/install.py
python -m pip install -r requirements.txt
python scripts/check_environment.py
```

Windows 可根据 Python 的实际命令将 `python` 替换为 `py`；macOS/Linux 通常使用 `python3`。

安装器将以下六个目录复制到 `~/.agents/skills/`，保留同级依赖关系。该路径是 Codex 的用户级技能目录；如需兼容使用 `~/.codex/skills/` 的旧环境，可以显式指定 `--dest`。参见 [Codex 官方技能说明](https://learn.chatgpt.com/docs/build-skills)。安装后若未显示，重启 Codex。

| 目录 | 用途 |
| --- | --- |
| `math-pdf-translator` | 翻译流程、覆盖清单、质量验收 |
| `nature-reader` | 源文提取、公式核对、源页映射 |
| `nature-shared` | `nature-reader` 所需共享规则 |
| `elegantpaper-master` | 新建论文的 ElegantPaper 模板 |
| `elegantbook-master` | 新建书籍或章节的 ElegantBook 模板 |
| `pdf` | 本包提供的轻量 PDF 提取与渲染规则 |

已有任一同名技能时，默认在写入前退出。确认已有版本兼容后，可用 `python scripts/install.py --skip-existing` 保留已有技能，只安装缺失项；该选项不会检查已有版本是否满足翻译流程。不要用安装器覆盖宿主自带的 PDF 技能。可用 `--dest 路径` 指定其他技能根目录；它不修改 Codex 设置。

也可以让 Codex 的 `$skill-installer` 从本仓库安装上述 `skills/<目录名>` 路径。必须同时提供缺失的依赖；只安装主技能会缺少工作流程需要的资源。

## 外部环境

以下工具须另外安装并加入 `PATH`：

- TeX Live 或 MiKTeX：`xelatex`、`biber`，以及模板所需的中文字体与宏包。
- Poppler：`pdftotext`、`pdftoppm`、`pdfinfo`。
- Python 包见 `requirements.txt`，用于提取与检查。
- 扫描 PDF 需要额外 OCR 工具，按文档选择；数学公式仍须对照原页复核。

`check_environment.py` 输出 JSON；缺少任一基础依赖时退出码为 1。它只检查命令、Python 包与技能入口，**不能替代中文字体检查、完整 TeX 编译和逐页验收**。检查其他安装目录时使用 `--skills-root 路径`。

## 使用

在 Codex 中输入：

```text
$math-pdf-translator 将 /path/to/paper.pdf 全文翻译为中文 LaTeX 和 PDF，
新建项目，保留全部公式、图表和编号，并生成覆盖清单与逐页检查记录。
```

Windows 路径含空格时可加引号。已有项目可指定原 `.tex` 文件；技能会保留其文档类。新建论文默认 ElegantPaper，书籍或章节默认 ElegantBook。主文件默认采用 `AuthorYear_keyword_cn.tex` 等有意义的名称。

典型交付包括：

- 中文 `.tex`、同名 PDF、必要模板与图片资源；
- `translation_coverage.json` 或 CSV，记录原文段落、公式、图表和图注；
- 源页映射、术语记录和任务级约束包；
- 编译日志及全部最终 PDF 页面的检查结果。

参考文献是否在主文中完整排印遵从用户要求；原文引用和追溯信息必须保留。可编辑、可搜索的文字/矢量 PDF 与图片 PDF 不可混同。

技能保留分阶段规划、单一正文写入者和独立验收流程。默认模型不可用时使用当前可用模型，并说明实际路由；不要求用户购买或手动切换到某个特定模型。长文可能需要多轮处理。`complete_verified` 仅用于完成源文覆盖、编译和全部最终页面人工式视觉核验的交付。

## 验证与开发

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -v
python scripts/smoke_templates.py --output build/smoke
```

最后一条需要本机具备 TeX 与 Poppler，实际编译两份原创微型样例，检查引用解析和中文文本，并生成供视觉检查的页面 PNG。自动检查通过不代表视觉检查完成，更不代表任何实际论文已翻译完成。样例仅用于安装与模板验证。

`skills/math-pdf-translator/scripts/audit_latex_chapter.ps1` 是原有章节辅助审计工具，匹配特定章节标签格式，不能代替通用论文的覆盖或数学核对。

GitHub Actions 在 Ubuntu 和 Windows 上运行包完整性及安装器测试；不宣称自动完成真实文献翻译或逐页验收。

## 来源与许可证

本项目自编内容使用 MIT；随包第三方内容保留 Apache-2.0 或 LPPL-1.3c-or-later，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。第三方资源固定到公开上游提交，文件来源见 `provenance.json`，发布完整性见 `manifest.json`。

发布包不包含用户论文、私人译稿、个人前言、账号凭据或本机专用路径。处理他人论文时，请确保有权访问和使用源文件。
